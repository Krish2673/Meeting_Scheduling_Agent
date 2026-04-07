from pydantic import BaseModel
from typing import List, Literal, Optional

class Meeting(BaseModel):
    id: str
    start: int
    end: int
    priority: Literal["low", "medium", "high"]
    deadline: int

class Observation(BaseModel):
    meetings: List[Meeting]
    conflicts: List[List[str]]  # pairs of meeting IDs
    remaining_steps: int

class Action(BaseModel):
    action_type: Literal["reschedule", "drop", "noop"]

    meeting_id: Optional[str] = None
    new_start: Optional[int] = None
    new_end: Optional[int] = None

class StepResult(BaseModel):
    observation: Observation
    reward: float
    done: bool
    info: dict