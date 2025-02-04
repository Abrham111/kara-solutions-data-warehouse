from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import schemas
import crud
import database


app = FastAPI()

# Create tables
models.Base.metadata.create_all(bind=database.engine)

# Dependency to get DB session
def get_db():
  db = database.SessionLocal()
  try:
    yield db
  finally:
    db.close()

# Create message
@app.post("/messages/", response_model=schemas.MessageResponse)
def create_message(message: schemas.MessageCreate, db: Session = Depends(get_db)):
  return crud.create_message(db=db, message=message)

# Get all messages
@app.get("/messages/", response_model=list[schemas.MessageResponse])
def read_messages(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
  return crud.get_messages(db=db, skip=skip, limit=limit)

# Get a single message by ID
@app.get("/messages/{message_id}", response_model=schemas.MessageResponse)
def read_message(message_id: int, db: Session = Depends(get_db)):
  db_message = crud.get_message(db=db, message_id=message_id)
  if db_message is None:
    raise HTTPException(status_code=404, detail="Message not found")
  return db_message
