from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import your data loader and AI orchestration logic
from src.data_loader import DataLoader
from src.ai_orchestration import MentalHealthAIOrchestrator

# Initialize FastAPI app
app = FastAPI(title="Mental Health AI Assistant API")

# Load the knowledge base at startup
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
excel_file_path = os.path.join(project_root, 'data', 'missing_values_updated.xlsx')
data_loader = DataLoader(excel_file_path)
knowledge_base = data_loader.load_all_data()

# Initialize AI orchestrator
ai_orchestrator = MentalHealthAIOrchestrator()

# Pydantic models for responses
class Problem(BaseModel):
    id: int
    problem_name: str
    description: Optional[str] = None

class Suggestion(BaseModel):
    id: int
    suggestion_text: str
    problem_id: Optional[int] = None

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: Optional[str] = None

@app.get("/problems", response_model=List[Problem])
def get_problems():
    return [Problem(id=p.id, problem_name=p.problem_name, description=getattr(p, 'description', None)) for p in knowledge_base['problems']]

@app.get("/suggestions", response_model=List[Suggestion])
def get_suggestions():
    return [Suggestion(id=s.id, suggestion_text=s.suggestion_text, problem_id=getattr(s, 'problem_id', None)) for s in knowledge_base['suggestions']]

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        # Use the AI orchestrator to generate a response
        response = ai_orchestrator.chat(request.message, session_id=request.session_id)
        return ChatResponse(response=response, session_id=request.session_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))