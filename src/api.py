from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import os
import uuid
from datetime import datetime
from dotenv import load_dotenv
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Load environment variables
load_dotenv()

# Import your data loader and AI orchestration logic
from src.data_loader import DataLoader
from src.ai_orchestration import MentalHealthAIOrchestrator
from src.db_schema import init_db, get_db_session, Problem, Suggestion, SelfAssessment, FeedbackPrompt, NextAction, Feedback, FinetuningExample
from sqlalchemy import func

# Initialize database
init_db('sqlite:///mental_health_kb.db')

# Initialize FastAPI app
app = FastAPI(
    title="Mental Health AI Assistant API",
    description="API for the Mental Health AI Assistant with feedback and conversation tracking",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js frontend URL
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Initialize database connection pool on startup
@app.on_event("startup")
async def startup_event():
    # Initialize database connection pool
    db_connection_string = f"sqlite:///{os.path.join(project_root, 'mental_health_kb.db')}"
    init_db(db_connection_string)

# Update dependency to use connection pool
def get_ai_orchestrator():
    # Initialize AI orchestrator with config
    config = {
        "openai_api_key": os.getenv("OPENAI_API_KEY"),
        "db_connection_string": f"sqlite:///{os.path.join(project_root, 'mental_health_kb.db')}",
        "model_name": "ft:gpt-4o-mini-2024-07-18:personal::BgSR6SI0",
        "vector_db_path": os.path.join(project_root, 'data', 'vector_db')
    }
    return MentalHealthAIOrchestrator(config)

# Load the knowledge base at startup
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

# In-memory session storage (in production, use a proper database)
conversation_sessions = {}

# Pydantic models for requests and responses
class ProblemResponse(BaseModel):
    problem_id: str = Field(..., description="Unique identifier for the problem")
    problem_name: str = Field(..., description="Name of the problem")
    description: Optional[str] = Field(None, description="Description of the problem")

class Suggestion(BaseModel):
    suggestion_id: str = Field(..., description="Unique identifier for the suggestion")
    suggestion_text: str = Field(..., description="The suggestion text")
    problem_id: Optional[str] = Field(None, description="ID of the related problem")

class ChatRequest(BaseModel):
    message: str = Field(..., description="User's message")
    session_id: Optional[str] = Field(None, description="Session ID for conversation tracking")
    context: Optional[Dict[str, Any]] = Field(
        None, 
        description="Additional context for the conversation"
    )

class ChatResponse(BaseModel):
    response: str = Field(..., description="AI's response")
    session_id: str = Field(..., description="Session ID for conversation tracking")
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional metadata about the response"
    )

class FeedbackRequest(BaseModel):
    feedback: str = Field(..., description="User's feedback text")
    session_id: str = Field(..., description="Session ID for conversation tracking")
    user_message: Optional[str] = Field(None, description="Original user message that this feedback is about")
    ai_response: Optional[str] = Field(None, description="AI's response that this feedback is about")
    problem_id: Optional[str] = Field(None, description="Related problem ID if applicable")
    suggestion_id: Optional[str] = Field(None, description="Related suggestion ID if applicable")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context for the feedback")

class FeedbackResponse(BaseModel):
    message: str = Field(..., description="Response message")
    feedback_id: str = Field(..., description="Unique identifier for the stored feedback")
    sentiment: str = Field(..., description="Detected sentiment of the feedback")
    next_action: str = Field(..., description="Suggested next action code")

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint for health check and API information"""
    return {
        "name": "Mental Health AI Assistant API",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/kb-stats", tags=["Knowledge Base"])
async def get_kb_stats(ai: MentalHealthAIOrchestrator = Depends(get_ai_orchestrator)):
    """Get knowledge base statistics"""
    try:
        with get_db_session() as session:
            stats = {
                "last_updated": datetime.utcnow().isoformat(),
                "problems_count": session.query(func.count(Problem.problem_id)).scalar() or 0,
                "suggestions_count": session.query(func.count(Suggestion.suggestion_id)).scalar() or 0,
                "assessments_count": session.query(func.count(SelfAssessment.question_id)).scalar() or 0,
                "feedback_prompts_count": session.query(func.count(FeedbackPrompt.prompt_id)).scalar() or 0,
                "next_actions_count": session.query(func.count(NextAction.action_id)).scalar() or 0,
                "finetuning_examples_count": session.query(func.count(FinetuningExample.id)).scalar() or 0
            }
            return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/kb-usage-report", tags=["Knowledge Base"])
async def get_kb_usage_report(ai: MentalHealthAIOrchestrator = Depends(get_ai_orchestrator)):
    """Get knowledge base usage statistics and analysis"""
    try:
        with get_db_session() as session:
            # Get problem usage statistics based on feedback
            problem_usage = session.query(
                Problem.problem_id,
                Problem.problem_name,
                func.count(Feedback.id).label('usage_count')
            ).outerjoin(
                Feedback,
                Problem.problem_id == Feedback.problem_id
            ).group_by(
                Problem.problem_id,
                Problem.problem_name
            ).all()

            # Get suggestion effectiveness
            suggestion_effectiveness = session.query(
                Suggestion.suggestion_id,
                Suggestion.suggestion_text,
                func.avg(Feedback.feedback_sentiment).label('average_rating'),
                func.count(Feedback.id).label('total_uses')
            ).outerjoin(
                Feedback,
                Suggestion.suggestion_id == Feedback.suggestion_id
            ).group_by(
                Suggestion.suggestion_id,
                Suggestion.suggestion_text
            ).all()

            # Get feedback sentiment distribution
            total_feedback = session.query(func.count(Feedback.id)).scalar() or 1
            feedback_sentiment = session.query(
                Feedback.sentiment,
                func.count(Feedback.id).label('count')
            ).group_by(
                Feedback.sentiment
            ).all()

            # Format the response
            report = {
                "problem_usage": [
                    {
                        "problem_id": str(p_id),
                        "problem_name": p_name,
                        "usage_count": int(p_count)
                    }
                    for p_id, p_name, p_count in problem_usage
                ],
                "suggestion_effectiveness": [
                    {
                        "suggestion_id": str(s_id),
                        "suggestion_text": s_text,
                        "average_rating": float(s_rating) if s_rating else 0.0,
                        "total_uses": int(s_uses)
                    }
                    for s_id, s_text, s_rating, s_uses in suggestion_effectiveness
                ],
                "feedback_sentiment": [
                    {
                        "sentiment": sentiment or "neutral",
                        "count": int(count),
                        "percentage": float(count) / total_feedback
                    }
                    for sentiment, count in feedback_sentiment
                ],
                "sync_history": [
                    {
                        "timestamp": datetime.utcnow().isoformat(),
                        "description": "Initial knowledge base statistics"
                    }
                ]
            }
            return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/problems", response_model=List[ProblemResponse], tags=["Knowledge Base"])
async def get_problems(ai: MentalHealthAIOrchestrator = Depends(get_ai_orchestrator)):
    """Get list of all available mental health problems"""
    try:
        problems = ai.get_problem_list()
        return [
            ProblemResponse(
                problem_id=p['id'], # Assuming 'id' from ai.get_problem_list() maps to problem_id
                problem_name=p['name'],
                description=p.get('description') # Use .get() for optional fields
            ) for p in problems
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/suggestions", response_model=List[Suggestion], tags=["Knowledge Base"])
async def get_suggestions(problem_id: Optional[str] = None, ai: MentalHealthAIOrchestrator = Depends(get_ai_orchestrator)):
    """Get suggestions, optionally filtered by problem ID"""
    try:
        if problem_id:
            suggestions = ai.get_suggestions(problem_id)
        else:
            # Get all suggestions if no problem_id is provided
            problems = ai.get_problem_list()
            all_suggestions = []
            for problem in problems:
                all_suggestions.extend(ai.get_suggestions(problem['id']))
            suggestions = all_suggestions
            
        return [
            Suggestion(
                suggestion_id=s['id'],
                suggestion_text=s['text'],
                problem_id=s.get('problem_id')
            ) for s in suggestions
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Thread pool for CPU-bound tasks
thread_pool = ThreadPoolExecutor(max_workers=4)

@app.post("/chat", response_model=ChatResponse, tags=["Conversation"])
async def chat(request: ChatRequest, ai: MentalHealthAIOrchestrator = Depends(get_ai_orchestrator)):
    """Process a user message and return an AI response asynchronously."""
    try:
        # Generate or validate session ID
        session_id = request.session_id or f"sess_{uuid.uuid4().hex}"
        
        # Get or create conversation context
        if session_id not in conversation_sessions:
            conversation_sessions[session_id] = {
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow(),
                'message_count': 0,
                'context': request.context or {}
            }
        
        # Update session metadata
        session = conversation_sessions[session_id]
        session['updated_at'] = datetime.utcnow()
        session['message_count'] += 1
        
        # Process the message in a thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            thread_pool,
            lambda: ai.process_user_message(
                user_id=session_id,
                message=request.message
            )
        )
        
        # Update context with any new information
        if 'context' in response:
            session['context'].update(response['context'])
        
        return ChatResponse(
            response=response['text'],
            session_id=session_id,
            metadata={
                'next_action': response.get('next_action'),
                'sentiment': response.get('sentiment'),
                'key_phrases': response.get('key_phrases', []),
                'source_documents': response.get('source_documents', [])
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing message: {str(e)}"
        )

@app.post("/feedback", response_model=FeedbackResponse, tags=["Feedback"])
async def submit_feedback(feedback: FeedbackRequest, ai: MentalHealthAIOrchestrator = Depends(get_ai_orchestrator)):
    """
    Submit feedback about the AI's response.
    
    This can be used to improve the system and provide better responses in the future.
    """
    try:
        # Process the feedback
        result = ai.process_feedback(
            feedback=feedback.feedback,
            context=feedback.context or {},
            user_id=feedback.session_id,  # Using session_id as user_id for consistency
            user_message=feedback.user_message,
            ai_response=feedback.ai_response,
            problem_id=feedback.problem_id,
            suggestion_id=feedback.suggestion_id
        )
        
        return FeedbackResponse(
            message=result['text'],
            feedback_id=result.get('feedback_id', ''),
            sentiment=result.get('sentiment', 'neutral'),
            next_action=result.get('next_action', 'A01')
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing feedback: {str(e)}"
        )

@app.get("/sessions/{session_id}", tags=["Sessions"])
async def get_session(session_id: str):
    """Get information about a conversation session"""
    if session_id not in conversation_sessions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    return conversation_sessions[session_id]

# Add startup event to initialize the database tables
@app.on_event("startup")
async def startup_event():
    """Initialize database and other resources on startup"""
    try:
        # This will create tables if they don't exist
        from sqlalchemy import create_engine
        from src.db_schema import Base
        
        engine = create_engine(f"sqlite:///{os.path.join(project_root, 'mental_health_kb.db')}")
        Base.metadata.create_all(bind=engine)
        print("Database tables verified/created successfully")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise