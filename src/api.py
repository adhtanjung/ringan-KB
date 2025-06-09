from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import os
import uuid
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import your data loader and AI orchestration logic
from src.data_loader import DataLoader
from src.ai_orchestration import MentalHealthAIOrchestrator

# Initialize FastAPI app
app = FastAPI(
    title="Mental Health AI Assistant API",
    description="API for the Mental Health AI Assistant with feedback and conversation tracking",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the knowledge base at startup
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

def get_ai_orchestrator():
    # Initialize AI orchestrator with config
    config = {
        "openai_api_key": os.getenv("OPENAI_API_KEY"),
        "db_connection_string": f"sqlite:///{os.path.join(project_root, 'mental_health_kb.db')}",
        "model_name": "ft:gpt-4o-mini-2024-07-18:personal::BgSR6SI0"
    }
    return MentalHealthAIOrchestrator(config)

# In-memory session storage (in production, use a proper database)
conversation_sessions = {}

# Pydantic models for requests and responses
class Problem(BaseModel):
    id: str = Field(..., description="Unique identifier for the problem")
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

@app.get("/problems", response_model=List[Problem], tags=["Knowledge Base"])
async def get_problems(ai: MentalHealthAIOrchestrator = Depends(get_ai_orchestrator)):
    """Get list of all available mental health problems"""
    try:
        problems = ai.get_problem_list()
        return [
            Problem(
                id=p['id'],
                problem_name=p['name'],
                description=None
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

@app.post("/chat", response_model=ChatResponse, tags=["Conversation"])
async def chat(request: ChatRequest, ai: MentalHealthAIOrchestrator = Depends(get_ai_orchestrator)):
    """
    Process a user message and return an AI response.
    
    - If no session_id is provided, a new session will be created.
    - The response will include a session_id that should be used for subsequent requests.
    """
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
        
        # Process the message
        response = ai.process_user_message(
            user_id=session_id,  # Using session_id as user_id for backward compatibility
            message=request.message
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
                'key_phrases': response.get('key_phrases', [])
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