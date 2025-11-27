from pydantic import BaseModel
from datetime import datetime


class MessageCreate(BaseModel):
    role: str
    content: str

class MessageOut(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime

    class Config:
        orm_mode = True

class MessageRequest(BaseModel):
    message: str