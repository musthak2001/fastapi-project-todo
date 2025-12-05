from pydantic import BaseModel
from typing import Optional

# Base model shared by create and update requests
class TodoBase(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False

# Model used when creating a new Todo
class TodoCreate(TodoBase):
    pass

# Model used when reading data from DB (with ID)
class Todo(TodoBase):
    id: int

    class Config:
        orm_mode = True
