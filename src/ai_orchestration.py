from dotenv import load_dotenv
import os
import json
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker
from src.db_schema import (
    Problem, SelfAssessment, Suggestion, 
    FeedbackPrompt, NextAction, FinetuningExample, Feedback
)

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import HumanMessage, SystemMessage

# Sentiment analysis prompt template
SENTIMENT_ANALYSIS_PROMPT = """Analyze the sentiment of the following feedback text. 
Return a JSON object with these fields:
- sentiment: 'positive', 'negative', or 'neutral'
- confidence: float between 0 and 1
- key_phrases: list of key phrases that influenced the sentiment

Feedback: {feedback}

JSON Response: """

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

class MentalHealthAIOrchestrator:
    def __init__(self, config: Dict[str, Any]):
        self.config = config

        # Initialize components
        self.db_engine = create_engine(self.config['db_connection_string'])
        self.Session = sessionmaker(bind=self.db_engine)

        # Initialize embeddings and vector database
        # For OpenAIEmbeddings, ensure OPENAI_API_KEY is set in your environment variables
        # Use HuggingFaceEmbeddings with a model that produces 384 dimensions
        from langchain_huggingface import HuggingFaceEmbeddings
        
        embedding_model_name = "all-MiniLM-L6-v2"
        print(f"Attempting to initialize HuggingFaceEmbeddings with model: {embedding_model_name} on device: cpu")
        try:
            # Explicitly set device to 'cpu' to avoid meta tensor issues with sentence-transformers
            self.embeddings = HuggingFaceEmbeddings(
                model_name=embedding_model_name,
                model_kwargs={'device': 'cpu'},
                # encode_kwargs={'normalize_embeddings': True} # Optional: if you want normalized embeddings
            )
            # Attempt a dummy embedding to ensure the model is loaded correctly
            _ = self.embeddings.embed_query("Test query")
            print(f"HuggingFaceEmbeddings ({embedding_model_name}) initialized and tested successfully on CPU.")
        except Exception as e:
            print(f"CRITICAL ERROR: Failed to initialize or test HuggingFaceEmbeddings ({embedding_model_name}): {e}")
            # This is a critical failure, as embedding dimensions must match the vector store.
            raise RuntimeError(f"Failed to initialize required embedding model ({embedding_model_name}). Application cannot proceed.") from e

        # Initialize LLM
        self.llm = ChatOpenAI(temperature=0.7, model_name=self.config['model_name'], openai_api_key=openai_api_key)

        # Initialize conversation memory
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        # Load existing vector database from the configured path
        try:
            print(f"Loading vector database from {self.config['vector_db_path']}")
            # Use direct_client to avoid embedding function issues
            from langchain_community.vectorstores.chroma import Chroma
            self.vector_db = Chroma(
                persist_directory=self.config['vector_db_path'],
                embedding_function=self.embeddings,
                collection_name="langchain"
            )
            print(f"Vector database loaded successfully")
        except Exception as e:
            print(f"Error loading vector database: {e}")
            # Fallback to a simple vector database with minimal content if loading fails
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            texts = text_splitter.split_text("No documents loaded for vector database. The AI will rely on its general knowledge.")
            self.vector_db = Chroma.from_texts(texts, self.embeddings)


        # Initialize retrieval chain with explicit configuration to return source documents
        # Configure memory with explicit output key to avoid ValueError
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, output_key="answer")

        # Define a custom prompt for the document combination part of the chain
        from langchain.prompts import PromptTemplate
        _template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, in its original language.
        If you do not know the answer, just say that you do not know, do not try to make up an answer.
        Provide a concise, empathetic, and helpful answer based on the chat history.
        Do not directly quote any previous messages unless it's a definition or a specific instruction that needs to be precise.
        Always respond in English.

        Chat History:
        {chat_history}
        Follow Up Input: {question}
        Standalone question:"""
        CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)

        # More detailed prompt for the QA part
        qa_template = """
You are a helpful and empathetic AI assistant for mental well-being. Your goal is to support users by providing information and guidance based on the context provided.
Use the following pieces of context to answer the question at the end. If you don't know the answer from the context, politely say that you don't have specific information on that topic but can discuss general well-being.
Do not make up information. Strive to be understanding and supportive in your responses. Always respond in English.

Context:
{context}

Question: {question}

Helpful Answer:"""
        QA_PROMPT = PromptTemplate(template=qa_template, input_variables=["context", "question"])

        self.retrieval_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vector_db.as_retriever(search_kwargs={"k": 5}),
            memory=self.memory,
            return_source_documents=True,
            verbose=True,
            condense_question_prompt=CONDENSE_QUESTION_PROMPT, # Added to rephrase the follow-up question
            combine_docs_chain_kwargs={"prompt": QA_PROMPT} # This prompt guides the LLM on how to use the documents
        )

        print("AI components initialized with custom prompts")

    def get_problem_list(self) -> List[Dict[str, str]]:
        """Get list of available mental health problems"""
        session = self.Session()
        problems = session.query(Problem).all()
        session.close()
        return [{'id': p.problem_id, 'name': p.problem_name} for p in problems]

    def get_self_assessment(self, problem_id: str) -> List[Dict[str, Any]]:
        """Get self-assessment questions for a specific problem"""
        session = self.Session()
        questions = session.query(SelfAssessment).filter_by(problem_id=problem_id).all()
        session.close()
        return [{'id': q.question_id, 'text': q.question_text, 'type': q.response_type} for q in questions]

    def get_suggestions(self, problem_id: str) -> List[Dict[str, Any]]:
        """Get suggestions for a specific problem"""
        session = self.Session()
        suggestions = session.query(Suggestion).filter_by(problem_id=problem_id).all()
        session.close()
        return [{'id': s.suggestion_id, 'text': s.suggestion_text, 'resource': s.resource_link} for s in suggestions]

    def process_user_message(self, user_id: str, message: str) -> Dict[str, Any]:
        """Process a user message and generate a response using RAG"""
        # Add instruction to respond in English
        english_prompt = f"Please respond in English. {message}"
        
        # Use the retrieval chain to get a response
        response = self.retrieval_chain.invoke({"question": english_prompt})

        # Extract source documents if available
        source_documents = []
        if 'source_documents' in response:
            print(f"Found {len(response['source_documents'])} source documents")
            for doc in response['source_documents']:
                source_documents.append({
                    'content': doc.page_content,
                    'metadata': doc.metadata
                })
        else:
            print("No source documents found in response")
            # Debug what's in the response
            print(f"Response keys: {response.keys()}")

        # The response structure from ConversationalRetrievalChain is different
        # It typically returns a dictionary with 'answer' and 'chat_history'
        return {
            'text': response['answer'],
            'next_action': 'continue_same',
            'suggestions': [],
            'source_documents': source_documents
        }

    def get_feedback_prompt(self, stage: str) -> Dict[str, str]:
        """Get appropriate feedback prompt for the current conversation stage"""
        session = self.Session()
        prompt = session.query(FeedbackPrompt).filter_by(stage=stage).first()
        session.close()
        if prompt:
            return {'id': prompt.prompt_id, 'text': prompt.prompt_text, 'next_action': prompt.next_action}
        else:
            # Fallback if no specific prompt found for the stage
            return {'id': 'FP000', 'text': 'Thank you for your feedback!', 'next_action': 'A03'} # A03 for end_session

    def _analyze_sentiment(self, feedback: str) -> Dict[str, Any]:
        """Analyze sentiment of feedback using LLM"""
        try:
            messages = [
                SystemMessage(content="You are a sentiment analysis assistant. Analyze the sentiment and extract key phrases."),
                HumanMessage(content=SENTIMENT_ANALYSIS_PROMPT.format(feedback=feedback))
            ]
            
            response = self.llm.invoke(messages)
            result = json.loads(response.content)
            
            # Convert sentiment to numerical score (-1 to 1)
            sentiment_score = 0
            if result.get('sentiment') == 'positive':
                sentiment_score = min(1.0, max(0.0, result.get('confidence', 0.7)))
            elif result.get('sentiment') == 'negative':
                sentiment_score = -min(1.0, max(0.0, result.get('confidence', 0.7)))
                
            return {
                'sentiment': result.get('sentiment', 'neutral'),
                'confidence': result.get('confidence', 0.5),
                'key_phrases': result.get('key_phrases', []),
                'sentiment_score': sentiment_score
            }
            
        except Exception as e:
            print(f"Error in sentiment analysis: {e}")
            return {
                'sentiment': 'neutral',
                'confidence': 0.5,
                'key_phrases': [],
                'sentiment_score': 0,
                'error': str(e)
            }

    def store_feedback(
        self,
        user_id: str,
        user_feedback: str,
        user_message: Optional[str] = None,
        ai_response: Optional[str] = None,
        problem_id: Optional[str] = None,
        suggestion_id: Optional[str] = None,
        context: Optional[Dict] = None
    ) -> str:
        """Store feedback in the database"""
        session = self.Session()
        try:
            # Analyze sentiment
            sentiment = self._analyze_sentiment(user_feedback)
            
            # Create feedback record
            feedback_id = str(uuid.uuid4())
            feedback = Feedback(
                id=feedback_id,
                user_id=user_id,  # Changed from session_id to user_id
                user_message=user_message,
                ai_response=ai_response,
                user_feedback=user_feedback,
                feedback_sentiment=sentiment['sentiment_score'],
                context=context or {},
                problem_id=problem_id,
                suggestion_id=suggestion_id,
                created_at=datetime.utcnow()
            )
            
            session.add(feedback)
            session.commit()
            return feedback_id
            
        except Exception as e:
            session.rollback()
            print(f"Error storing feedback: {e}")
            raise
        finally:
            session.close()

    def process_feedback(
        self, 
        feedback: str, 
        context: Dict[str, Any],
        user_id: Optional[str] = None,
        user_message: Optional[str] = None,
        ai_response: Optional[str] = None,
        problem_id: Optional[str] = None,
        suggestion_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Process user feedback and determine next action"""
        try:
            # Store the feedback
            feedback_id = self.store_feedback(
                user_id=user_id or 'unknown',
                user_feedback=feedback,
                user_message=user_message,
                ai_response=ai_response,
                problem_id=problem_id,
                suggestion_id=suggestion_id,
                context=context
            )
            
            # Analyze sentiment for response generation
            sentiment = self._analyze_sentiment(feedback)
            
            # Determine response based on sentiment
            if sentiment['sentiment_score'] > 0.3:  # Positive
                response = {
                    'text': "I'm glad that was helpful! Would you like to explore more about this or try something else?",
                    'next_action': 'A01',  # Continue same
                    'sentiment': 'positive',
                    'feedback_id': feedback_id
                }
            elif sentiment['sentiment_score'] < -0.3:  # Negative
                response = {
                    'text': "I'm sorry to hear that. Would you like to try a different approach or talk about something else?",
                    'next_action': 'A02',  # Show problem menu
                    'sentiment': 'negative',
                    'feedback_id': feedback_id
                }
            else:  # Neutral
                response = {
                    'text': "Thank you for your feedback. Is there anything specific you'd like to discuss further?",
                    'next_action': 'A03',  # Ask follow-up
                    'sentiment': 'neutral',
                    'feedback_id': feedback_id
                }
                
            # Add key phrases to context for future reference
            if sentiment.get('key_phrases'):
                response['key_phrases'] = sentiment['key_phrases']
                
            return response
            
        except Exception as e:
            print(f"Error processing feedback: {e}")
            return {
                'text': "Thank you for your feedback. I'll use this to improve.",
                'next_action': 'A01',
                'error': str(e)
            }

# Example configuration - replace with your actual OpenAI API key
config = {
    'db_connection_string': 'sqlite:///mental_health_kb.db',
    'vector_db_path': './data/vector_db_documents.json', # This is now the path to the JSON file
    'openai_api_key': openai_api_key, # Recommended to use environment variable
    'model_name': 'ft:gpt-4o-mini-2024-07-18:personal::BgSR6SI0'
}

# Example usage
if __name__ == "__main__":
    # Ensure OPENAI_API_KEY is set in your environment
    if config['openai_api_key'] is None:
        print("Error: OPENAI_API_KEY environment variable not set. Please set it before running.")
        print("You can set it like this: export OPENAI_API_KEY='your_api_key_here' (Linux/macOS) or $env:OPENAI_API_KEY='your_api_key_here' (Windows PowerShell)")
        exit(1)

    orchestrator = MentalHealthAIOrchestrator(config)

    # Example conversation flow
    print("\nAvailable Problems:")
    problems = orchestrator.get_problem_list()
    for problem in problems:
        print(f"- {problem['name']} (ID: {problem['id']})")

    print("\nSelf-Assessment Questions:")
    selected_problem = 'P001' # Example selection
    questions = orchestrator.get_self_assessment(selected_problem)
    for question in questions:
        print(f"- {question['text']}")

    print("\nUser message: 'I've been feeling very anxious lately'")
    response = orchestrator.process_user_message('user123', "I've been feeling very anxious lately")
    print(f"AI: {response['text']}")

    # print("\nSuggestions:") # Suggestions are now part of LLM response or follow-up logic
    # for suggestion in response['suggestions']:
    #     print(f"- {suggestion['text']}")

    print("\nFeedback prompt:")
    # We need to refine how feedback is handled after LLM integration
    # For now, let's use a simplified feedback flow
    feedback_prompt = orchestrator.get_feedback_prompt('post_suggestion') # Using a stage that exists in Feedback Prompts
    print(f"AI: {feedback_prompt['text']}")

    print("\nUser feedback: 'Yes, that was helpful'")
    feedback_response = orchestrator.process_feedback("Yes, that was helpful", {'current_problem': selected_problem})
    print(f"AI: {feedback_response['text']}")
    print(f"Next action: {feedback_response['next_action']}")


# Implement Caching for Responses
    
    # Add caching decorator for expensive operations
    @lru_cache(maxsize=100)
    def _get_cached_embedding(self, text):
        """Cache embeddings to avoid recomputing them"""
        return self.embedding_function.embed_query(text)
    
    def _get_cache_key(self, user_id, message):
        """Generate a cache key for a user message"""
        cache_str = f"{user_id}:{message}"
        return hashlib.md5(cache_str.encode()).hexdigest()
    
    def _check_cache(self, cache_key):
        """Check if a response is cached"""
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                return json.load(f)
        return None
    
    def _save_to_cache(self, cache_key, response):
        """Save a response to cache"""
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        with open(cache_file, 'w') as f:
            json.dump(response, f)
    
    def process_user_message(self, user_id, message):
        """Process a user message with caching"""
        # Check cache first
        cache_key = self._get_cache_key(user_id, message)
        cached_response = self._check_cache(cache_key)
        
        if cached_response:
            print("Using cached response")
            return cached_response
        
        # If not cached, process normally
        # The response structure from ConversationalRetrievalChain is different
        # It typically returns a dictionary with 'answer' and 'chat_history'
        return {
            'text': response['answer'],
            'next_action': 'continue_same',
            'suggestions': [],
            'source_documents': source_documents
        }

    def get_feedback_prompt(self, stage: str) -> Dict[str, str]:
        """Get appropriate feedback prompt for the current conversation stage"""
        session = self.Session()
        prompt = session.query(FeedbackPrompt).filter_by(stage=stage).first()
        session.close()
        if prompt:
            return {'id': prompt.prompt_id, 'text': prompt.prompt_text, 'next_action': prompt.next_action}
        else:
            # Fallback if no specific prompt found for the stage
            return {'id': 'FP000', 'text': 'Thank you for your feedback!', 'next_action': 'A03'} # A03 for end_session

    def _analyze_sentiment(self, feedback: str) -> Dict[str, Any]:
        """Analyze sentiment of feedback using LLM"""
        try:
            messages = [
                SystemMessage(content="You are a sentiment analysis assistant. Analyze the sentiment and extract key phrases."),
                HumanMessage(content=SENTIMENT_ANALYSIS_PROMPT.format(feedback=feedback))
            ]
            
            response = self.llm.invoke(messages)
            result = json.loads(response.content)
            
            # Convert sentiment to numerical score (-1 to 1)
            sentiment_score = 0
            if result.get('sentiment') == 'positive':
                sentiment_score = min(1.0, max(0.0, result.get('confidence', 0.7)))
            elif result.get('sentiment') == 'negative':
                sentiment_score = -min(1.0, max(0.0, result.get('confidence', 0.7)))
                
            return {
                'sentiment': result.get('sentiment', 'neutral'),
                'confidence': result.get('confidence', 0.5),
                'key_phrases': result.get('key_phrases', []),
                'sentiment_score': sentiment_score
            }
            
        except Exception as e:
            print(f"Error in sentiment analysis: {e}")
            return {
                'sentiment': 'neutral',
                'confidence': 0.5,
                'key_phrases': [],
                'sentiment_score': 0,
                'error': str(e)
            }