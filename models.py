from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class TaskTier(str, Enum):
    SURVIVAL_CRITICAL = "Survival-critical"
    LONG_TERM_MEANINGFUL = "Long-term meaningful"
    ROUTINE_REPETITIVE = "Routine repetitive"
    NOISE = "Noise"

class UserEnergy(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class TaskFrequency(str, Enum):
    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

class TaskInput(BaseModel):
    id: Optional[str] = None
    description: str
    deadline: Optional[datetime] = None
    frequency: TaskFrequency = TaskFrequency.ONCE
    estimated_effort_hours: float = Field(..., ge=0, le=100)
    emotional_weight: Optional[int] = Field(None, ge=1, le=10)

class TaskClassificationResponse(BaseModel):
    description: str
    score: float
    tier: TaskTier
    next_action: str
    reasoning: str

class RecommendationRequest(BaseModel):
    tasks: List[TaskInput]
    current_energy: UserEnergy
    time_available_minutes: float
    previous_task_category: Optional[str] = None

class RecommendationResponse(BaseModel):
    selected_task: Optional[TaskClassificationResponse]
    alternative_actions: List[TaskClassificationResponse]
    system_note: str # For edge cases like "Rest" or "Refresher"
