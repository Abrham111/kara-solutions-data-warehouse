from sqlalchemy import Column, Integer, String, TIMESTAMP, Text
from .database import Base

class Message(Base):
  __tablename__ = "cleaned_messages"

  id = Column(Integer, primary_key=True, index=True)
  sender = Column(String, index=True)
  content = Column(Text)
  links = Column(Text) 
  emojis = Column(Text) 
  timestamp = Column(TIMESTAMP)
