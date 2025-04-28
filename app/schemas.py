from typing import List, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True

# God schemas
class GodBase(BaseModel):
    name: str
    description: str
    system_prompt: str

class GodCreate(GodBase):
    pass

class God(GodBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# Message schemas
class MessageBase(BaseModel):
    content: str
    is_from_user: bool = True

class MessageCreate(MessageBase):
    conversation_id: int

class Message(MessageBase):
    id: int
    conversation_id: int
    created_at: datetime

    class Config:
        orm_mode = True

# Conversation schemas
class ConversationBase(BaseModel):
    title: str
    god_id: int

class ConversationCreate(ConversationBase):
    pass

class Conversation(ConversationBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    messages: List[Message] = []
    god: God

    class Config:
        orm_mode = True

# Chat request/response schemas
class ChatRequest(BaseModel):
    conversation_id: int
    message: str

class ChatResponse(BaseModel):
    message: str
    conversation_id: int
