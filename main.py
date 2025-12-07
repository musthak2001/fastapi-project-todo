from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import Todo, User
from schemas import Todo as TodoSchema, TodoCreate, User as UserSchema, UserCreate
from database import SessionLocal, Base, engine

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Dependency: create a new database session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to My Todo API! Go to /docs for the interactive UI"}

# Create a new Todo item
@app.post("/todos/", response_model=TodoSchema)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = Todo(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

# Register a new user
@app.post("/register/", response_model=UserSchema)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    new_user = User(
        name=user.name,
        email=user.email,
        password=user.password  # TODO: hash password before saving in production
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


#get all details
@app.get("/userdetails/")
def read_registered_users(db: Session = Depends(get_db)):
    return db.query(User).all() 

#usergetails
@app.get("/userdetails/{user_id}", response_model=UserSchema)
def read_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

# UPDATE USER - Update name or email (password later with hashing)
@app.put("/userdetails/{user_id}", response_model=UserSchema)
def update_user( user_id: int,
    user_update: UserCreate,  # Reuse UserCreate (has name, email, password)
    db: Session = Depends(get_db)
):
    # Find the user
    db_user = db.query(User).filter(User.id == user_id).first()
    
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Check if new email is already taken by someone else
    if user_update.email != db_user.email:
        email_exists = db.query(User).filter(
            User.email == user_update.email,
            User.id != user_id
        ).first()
        if email_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered by another user"
            )

    # Update only the fields that are provided
    db_user.name = user_update.name
    db_user.email = user_update.email
    # db_user.password = user_update.password  # ← We'll hash this later

    db.commit()
    db.refresh(db_user)
    
    return db_user

#delete
@app.delete("/userdetails/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return {"message" : "user deleted successfully"}