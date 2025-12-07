from pydantic import BaseModel

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
        from_attributes = True

# ------------------- User Schemas -------------------

# 👉 Base schema for user (shared)
class UserBase(BaseModel):
    name: str
    email: str

# 👉 Used for registering new user
class UserCreate(UserBase):
    password: str

# 👉 Used when returning user details
class User(UserBase):
    id: int

    class Config:
        from_attributes = True
