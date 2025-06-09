from dotenv import load_dotenv
import os
from typing import Dict, List, Any
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db_schema import Problem, SelfAssessment, Suggestion, FeedbackPrompt, NextAction, FinetuningExample

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

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
        self.embeddings = OpenAIEmbeddings(api_key=openai_api_key)

        # Initialize LLM
        self.llm = ChatOpenAI(temperature=0.7, model_name=self.config['model_name'], openai_api_key=openai_api_key)

        # Initialize conversation memory
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        # Load existing vector database or create a new one
        vector_db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'vector_db_documents.json')

        # For a real ChromaDB, you would load it like this:
        # self.vector_db = Chroma(persist_directory=self.config['vector_db_path'], embedding_function=self.embeddings)

        # For now, we will use the JSON data to build the retriever if the file exists
        documents = []
        if os.path.exists(vector_db_path):
            import json
            with open(vector_db_path, 'r') as f:
                loaded_docs = json.load(f)
                # Reconstruct Document objects for LangChain
                for doc_data in loaded_docs:
                    # For simplicity, we are creating a basic document structure.
                    # In a full RAG implementation, you'd map your loaded data to LangChain's Document class.
                    # This might require some adjustments based on how `vector_db_documents.json` was structured.
                    documents.append({"page_content": doc_data['text'], "metadata": doc_data['metadata']})

        # A dummy retriever if documents are empty or for initial setup
        if not documents:
            # If there are no documents, we can create a simple retriever with dummy content
            # or handle this scenario appropriately (e.g., raise an error, use a different LLM strategy)
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            texts = text_splitter.split_text("No documents loaded for vector database. The AI will rely on its general knowledge.")
            self.vector_db = Chroma.from_texts(texts, self.embeddings)
        else:
            # Assuming documents are already in a format usable by Chroma.from_documents
            # This part might need adjustment based on the actual format of `vector_db_documents.json`
            # For example, if it contains embeddings, you might use Chroma.from_embeddings
            # For now, let's assume it has text content that can be embedded by Chroma.
            # You might need to convert your loaded JSON data into LangChain's Document format:
            from langchain_core.documents import Document
            langchain_documents = [Document(page_content=doc["page_content"], metadata=doc["metadata"]) for doc in documents]
            self.vector_db = Chroma.from_documents(langchain_documents, self.embeddings)


        # Initialize retrieval chain
        self.retrieval_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vector_db.as_retriever(),
            memory=self.memory
        )

        print("AI components initialized")

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
        # Use the retrieval chain to get a response
        response = self.retrieval_chain.invoke({"question": message})

        # The response structure from ConversationalRetrievalChain is different
        # It typically returns a dictionary with 'answer' and 'chat_history'
        return {
            'text': response['answer'],
            'next_action': 'continue_same', # This needs to be determined by the LLM or a more complex logic
            'suggestions': [] # Suggestions would need to be retrieved based on the LLM's response
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

    def process_feedback(self, feedback: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process user feedback and determine next action"""
        # This part could also be handled by the LLM for more nuanced responses
        if 'yes' in feedback.lower():
            return {
                'text': "I'm glad that was helpful. Would you like another suggestion?",
                'next_action': 'A01' # A01 for continue_same
            }
        else:
            return {
                'text': "I'm sorry that wasn't helpful. Let's try a different approach.",
                'next_action': 'A02' # A02 for show_problem_menu
            }

# Example configuration - replace with your actual OpenAI API key
config = {
    'db_connection_string': 'sqlite:///mental_health_kb.db',
    'vector_db_path': './data/vector_db_documents.json', # This is now the path to the JSON file
    'openai_api_key': openai_api_key, # Recommended to use environment variable
    'model_name': 'gpt-4o-mini-2024-07-18'
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