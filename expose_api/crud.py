from sqlalchemy.orm import Session
from . import models, schemas

# Create a message
def create_message(db: Session, message: schemas.MessageCreate):
  db_message = models.Message(**message.dict())
  db.add(db_message)
  db.commit()
  db.refresh(db_message)
  return db_message

# Get all messages
def get_messages(db: Session, skip: int = 0, limit: int = 10):
  return db.query(models.Message).offset(skip).limit(limit).all()

# Get message by ID
def get_message(db: Session, message_id: int):
  return db.query(models.Message).filter(models.Message.id == message_id).first()
