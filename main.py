from fastapi import FastAPI, Depends              
from models import Todo
from schemas import Todo as Todoschema  ,TodoCreate          
from sqlalchemy.orm import Session               
from database import SessionLocal,Base,engine            

app = FastAPI()                                   # Create FastAPI app
# At the bottom of database.py or in a separate script
Base.metadata.create_all(bind=engine)
# Create a new DB session for each request
def get_db():
    db = SessionLocal()                           # Open session
    try:
        yield db                                  # Provide session to endpoint
    finally:
        db.close()                                # Close session after request

# Create a new Todo item
@app.post("/todos/", response_model=Todoschema)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = Todo(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.get("/")
def read_root():
    return {"message": "Welcome to My Todo API! Go to /docs for the interactive UI"}
                                         