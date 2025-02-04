from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class MessageBase(BaseModel):
  sender: str
  content: str
  links: Optional[List[str]] = []
  emojis: Optional[List[str]] = []
  timestamp: datetime

class MessageCreate(MessageBase):
  pass

class MessageResponse(MessageBase):
  id: int

  class Config:
    from_attributes = True
