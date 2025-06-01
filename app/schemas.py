from typing import List, Optional, Dict, Any
from pydantic import BaseModel, EmailStr, Field
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
    id: str
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True

# God schemas
class GodBase(BaseModel):
    name: str
    description: str
    system_prompt: str
    example_phrases: Optional[List[str]] = None
    interaction_style: Optional[str] = None
    personality_traits: Optional[List[str]] = None
    image_url: Optional[str] = None
    religion: str

class GodCreate(GodBase):
    pass

class God(GodBase):
    id: str
    created_at: datetime

    class Config:
        orm_mode = True

# Message schemas
class MessageBase(BaseModel):
    content: str
    is_from_user: bool = True

class MessageCreate(MessageBase):
    conversation_id: str

class Message(MessageBase):
    id: str
    conversation_id: str
    created_at: datetime

    class Config:
        orm_mode = True

# Conversation schemas
class ConversationBase(BaseModel):
    title: str
    god_id: str

class ConversationCreate(ConversationBase):
    pass

class Conversation(ConversationBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    messages: List[Message] = []
    god: Optional[God] = None

    class Config:
        orm_mode = True

# Chat schemas
class ChatRequest(BaseModel):
    conversation_id: str
    message: str

class ChatResponse(BaseModel):
    message: str
    conversation_id: str

class Question(BaseModel):
    id: str
    question: str
    god_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

# Feedback schemas
class FeedbackBase(BaseModel):
    rating: float = Field(ge=0.0, le=5.0, description="Rating from 0.0 to 5.0 with one decimal place")
    likes: Optional[str] = None
    dislikes: Optional[str] = None

class FeedbackCreate(FeedbackBase):
    pass

class Feedback(FeedbackBase):
    id: str
    user_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
