from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from app.dependencies import get_db, get_current_active_user
from app.models import Conversation, Message, God, User
from app.schemas import Conversation as ConversationSchema, ConversationCreate, Message as MessageSchema, ChatRequest, ChatResponse
from app.services.openai_service import OpenAIService

router = APIRouter(
    prefix="/conversations",
    tags=["conversations"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=ConversationSchema)
async def create_conversation(
    conversation: ConversationCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Check if the god exists
    god = db.query(God).filter(God.id == conversation.god_id).first()
    if not god:
        raise HTTPException(status_code=404, detail="God not found")
    
    # Create new conversation
    db_conversation = Conversation(
        title=conversation.title,
        user_id=current_user.id,
        god_id=conversation.god_id
    )
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation

@router.get("/", response_model=List[ConversationSchema])
async def get_conversations(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    conversations = db.query(Conversation).filter(
        Conversation.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    return conversations

@router.get("/{conversation_id}", response_model=ConversationSchema)
async def get_conversation(
    conversation_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()
    
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return conversation

@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    conversation_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()
    
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    db.delete(conversation)
    db.commit()
    return None

@router.post("/chat", response_model=ChatResponse)
async def chat_with_god(
    chat_request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Get the conversation
    conversation = db.query(Conversation).filter(
        Conversation.id == chat_request.conversation_id,
        Conversation.user_id == current_user.id
    ).first()
    
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Get the god
    god = db.query(God).filter(God.id == conversation.god_id).first()
    if god is None:
        raise HTTPException(status_code=404, detail="God not found")
    
    # Save the user message
    user_message = Message(
        conversation_id=conversation.id,
        content=chat_request.message,
        is_from_user=True
    )
    db.add(user_message)
    db.commit()
    
    # Get conversation history
    messages = db.query(Message).filter(
        Message.conversation_id == conversation.id
    ).order_by(Message.created_at).all()
    
    # Format messages for OpenAI
    formatted_messages = OpenAIService.format_conversation_history(messages)
    
    # Generate response from OpenAI
    response_text = await OpenAIService.generate_response(
        messages=formatted_messages,
        system_prompt=god.system_prompt
    )
    
    # Save the god's response
    god_message = Message(
        conversation_id=conversation.id,
        content=response_text,
        is_from_user=False
    )
    db.add(god_message)
    db.commit()
    
    # Update conversation's updated_at timestamp
    conversation.updated_at = func.now()
    db.commit()
    
    return ChatResponse(
        message=response_text,
        conversation_id=conversation.id
    )
