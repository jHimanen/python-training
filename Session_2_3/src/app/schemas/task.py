from pydantic import BaseModel, ConfigDict
from typing import Optional

class TaskCreate(BaseModel):
    user_id: int
    title: str

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None

class TaskOut(BaseModel):
    id: int
    user_id: int
    title: str
    completed: bool
    model_config = ConfigDict(from_attributes=True)
