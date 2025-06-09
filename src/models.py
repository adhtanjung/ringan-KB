from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Problem:
    problem_id: str
    problem_name: str
    description: Optional[str] = None

@dataclass
class SelfAssessment:
    question_id: str
    problem_id: str
    question_text: str
    response_type: str
    next_step: Optional[str] = None

@dataclass
class Suggestion:
    suggestion_id: str
    problem_id: str
    suggestion_text: str
    resource_link: Optional[str] = None

@dataclass
class FeedbackPrompt:
    prompt_id: str
    stage: str
    prompt_text: str
    next_action: Optional[str] = None

@dataclass
class NextAction:
    action_id: str
    label: str
    description: Optional[str] = None

@dataclass
class FinetuningExample:
    id: str
    prompt: str
    completion: str
    problem: Optional[str] = None
    conversation_id: Optional[str] = None