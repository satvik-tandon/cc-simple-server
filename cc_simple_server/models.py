################################################
# This file is used to define the models for the application. Do not alter this file.
################################################
from pydantic import BaseModel
from typing import Optional


# Pydantic model for creating a new task
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


# Pydantic model for reading a task
class TaskRead(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool
