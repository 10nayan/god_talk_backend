from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from bson import ObjectId
from datetime import datetime
import pytz

from app.database import get_database
from app.schemas import Conversation as ConversationSchema, ConversationCreate, Message as MessageSchema, ChatRequest, ChatResponse
from app.dependencies import get_current_active_user, get_current_user_optional
from app.services.openai_service import OpenAIService

# Set timezone to IST
IST = pytz.timezone('Asia/Kolkata')

router = APIRouter(
    prefix="/conversations",
    tags=["conversations"],
    responses={404: {"description": "Not found"}},
)

# Helpers to convert MongoDB docs to schemas
def conversation_doc_to_schema(doc, god=None):
    if not doc:
        return None
    
    # Convert UTC to IST for API response
    created_at = doc.get("created_at", datetime.utcnow())
    updated_at = doc.get("updated_at", created_at)
    
    if created_at.tzinfo is None:
        created_at = pytz.utc.localize(created_at)
    if updated_at.tzinfo is None:
        updated_at = pytz.utc.localize(updated_at)
    
    created_at_ist = created_at.astimezone(IST)
    updated_at_ist = updated_at.astimezone(IST)
    
    return ConversationSchema(
        id=str(doc["_id"]),
        title=doc["title"],
        user_id=str(doc["user_id"]) if doc.get("user_id") else None,
        god_id=str(doc["god_id"]),
        god=god,
        messages=[message_doc_to_schema(msg) for msg in doc.get("messages", [])],
        created_at=created_at_ist,
        updated_at=updated_at_ist,
        is_guest=doc.get("is_guest", False)
    )

def message_doc_to_schema(doc):
    if not doc:
        return None
    
    created_at = doc.get("created_at", datetime.utcnow())
    if created_at.tzinfo is None:
        created_at = pytz.utc.localize(created_at)
    created_at_ist = created_at.astimezone(IST)
    
    return MessageSchema(
        id=str(doc["_id"]),
        content=doc["content"],
        is_from_user=doc["is_from_user"],
        created_at=created_at_ist,
        conversation_id=str(doc.get("conversation_id", "")) if doc.get("conversation_id") else None
    )

@router.get("/find/{god_id}", response_model=ConversationSchema)
async def find_conversation_with_god(
    god_id: str,
    db=Depends(get_database),
    current_user=Depends(get_current_active_user)
):
    """Find an existing conversation with a specific god."""
    try:
        god_oid = ObjectId(god_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Invalid god ID")

    # Find the most recent conversation with this god
    conversation = await db["conversations"].find_one({
        "user_id": ObjectId(current_user.id),
        "god_id": god_oid
    }, sort=[("updated_at", -1)])

    if not conversation:
        raise HTTPException(status_code=404, detail="No conversation found with this god")

    # Get the god details
    god = await db["gods"].find_one({"_id": god_oid})
    if not god:
        raise HTTPException(status_code=404, detail="God not found")

    return conversation_doc_to_schema(conversation, god=god)

@router.post("/", response_model=ConversationSchema)
async def create_conversation(
    conversation: ConversationCreate,
    db=Depends(get_database),
    current_user=Depends(get_current_user_optional)
):
    """Create a new conversation with a god."""
    try:
        # Validate god_id format
        try:
            god_oid = ObjectId(conversation.god_id)
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid god ID format: {str(e)}"
            )

        # Check if god exists
        god = await db["gods"].find_one({"_id": god_oid})
        if not god:
            raise HTTPException(
                status_code=404,
                detail=f"God with ID {conversation.god_id} not found"
            )

        # For guest users
        if not current_user:
            # Create new guest conversation
            conv_doc = {
                "title": conversation.title,
                "god_id": god_oid,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "is_guest": True,
                "messages": []
            }
            
            result = await db["conversations"].insert_one(conv_doc)
            if not result.inserted_id:
                raise HTTPException(
                    status_code=500,
                    detail="Failed to create conversation"
                )

            new_conv = await db["conversations"].find_one({"_id": result.inserted_id})
            if not new_conv:
                raise HTTPException(
                    status_code=500,
                    detail="Failed to retrieve created conversation"
                )

            # Convert god to schema
            from app.routers.gods import god_doc_to_schema
            god_schema = god_doc_to_schema(god)
            return conversation_doc_to_schema(new_conv, god=god_schema)

        # For authenticated users
        # Check if conversation already exists
        existing_conv = await db["conversations"].find_one({
            "user_id": ObjectId(current_user.id),
            "god_id": god_oid
        })

        if existing_conv:
            # Return existing conversation with god details
            from app.routers.gods import god_doc_to_schema
            god_schema = god_doc_to_schema(god)
            return conversation_doc_to_schema(existing_conv, god=god_schema)

        # Create new conversation
        conv_doc = {
            "title": conversation.title,
            "user_id": ObjectId(current_user.id),
            "god_id": god_oid,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "is_guest": False,
            "messages": []
        }
        
        result = await db["conversations"].insert_one(conv_doc)
        if not result.inserted_id:
            raise HTTPException(
                status_code=500,
                detail="Failed to create conversation"
            )

        new_conv = await db["conversations"].find_one({"_id": result.inserted_id})
        if not new_conv:
            raise HTTPException(
                status_code=500,
                detail="Failed to retrieve created conversation"
            )

        # Convert god to schema
        from app.routers.gods import god_doc_to_schema
        god_schema = god_doc_to_schema(god)
        return conversation_doc_to_schema(new_conv, god=god_schema)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/", response_model=List[ConversationSchema])
async def get_conversations(
    skip: int = 0,
    limit: int = 100,
    db=Depends(get_database),
    current_user=Depends(get_current_user_optional)
):
    """Get all conversations for the current user."""
    if not current_user:
        # For guest users, return an empty list
        return []
    
    cursor = db["conversations"].find({"user_id": ObjectId(current_user.id)}).skip(skip).limit(limit)
    conversations = []
    async for doc in cursor:
        # Get god details
        god = await db["gods"].find_one({"_id": ObjectId(doc["god_id"])})
        from app.routers.gods import god_doc_to_schema
        god_schema = god_doc_to_schema(god) if god else None
        conversations.append(conversation_doc_to_schema(doc, god=god_schema))
    return conversations

@router.get("/{conversation_id}", response_model=ConversationSchema)
async def get_conversation(
    conversation_id: str,
    db=Depends(get_database),
    current_user=Depends(get_current_user_optional)
):
    """Get a specific conversation."""
    try:
        conv_oid = ObjectId(conversation_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    conv = await db["conversations"].find_one({"_id": conv_oid})
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # For guest conversations, allow access without authentication
    if conv.get("is_guest", False):
        # Get god details
        god = await db["gods"].find_one({"_id": ObjectId(conv["god_id"])})
        from app.routers.gods import god_doc_to_schema
        god_schema = god_doc_to_schema(god) if god else None
        return conversation_doc_to_schema(conv, god=god_schema)
    
    # For authenticated users, check if they have access
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required to access this conversation"
        )
    
    if conv.get("user_id") and str(conv["user_id"]) != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this conversation")
    
    # Get god details
    god = await db["gods"].find_one({"_id": ObjectId(conv["god_id"])})
    from app.routers.gods import god_doc_to_schema
    god_schema = god_doc_to_schema(god) if god else None
    
    return conversation_doc_to_schema(conv, god=god_schema)

@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    conversation_id: str,
    db=Depends(get_database),
    current_user=Depends(get_current_active_user)
):
    try:
        oid = ObjectId(conversation_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Conversation not found")
    result = await db["conversations"].delete_one({"_id": oid, "user_id": ObjectId(current_user.id)})
    await db["messages"].delete_many({"conversation_id": oid})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return None

@router.post("/chat", response_model=ChatResponse)
async def chat_with_god(
    chat_request: ChatRequest,
    db=Depends(get_database),
    current_user=Depends(get_current_user_optional)
):
    """Send a message in a conversation."""
    try:
        conv_oid = ObjectId(chat_request.conversation_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    conv = await db["conversations"].find_one({"_id": conv_oid})
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Check if user has access to this conversation
    if conv.get("user_id") and current_user and str(conv["user_id"]) != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this conversation")
    
    # Check message limit for guest users
    if conv.get("is_guest", False):
        message_count = len(conv.get("messages", []))
        if message_count >= 5:
            raise HTTPException(
                status_code=403,
                detail="Guest users are limited to 5 messages. Please log in to continue chatting."
            )
    
    # Get god details
    god = await db["gods"].find_one({"_id": ObjectId(conv["god_id"])})
    if not god:
        raise HTTPException(status_code=404, detail="God not found")
    
    # Create user message
    user_message = {
        "_id": ObjectId(),
        "content": chat_request.message,
        "is_from_user": True,
        "created_at": datetime.utcnow()
    }
    
    # Add user message to conversation
    await db["conversations"].update_one(
        {"_id": conv_oid},
        {
            "$push": {"messages": user_message},
            "$set": {"updated_at": datetime.utcnow()}
        }
    )
    
    # Get conversation history and convert messages to Message objects
    messages = [message_doc_to_schema(msg) for msg in conv.get("messages", [])]
    formatted_messages = OpenAIService.format_conversation_history(messages)
    
    # Generate response from OpenAI
    response_text = await OpenAIService.generate_response(
        messages=formatted_messages,
        system_prompt=god.get("system_prompt", "")
    )
    
    # Create god's response
    god_response = {
        "_id": ObjectId(),
        "content": response_text,
        "is_from_user": False,
        "created_at": datetime.utcnow()
    }
    
    # Add god's response to conversation
    await db["conversations"].update_one(
        {"_id": conv_oid},
        {
            "$push": {"messages": god_response},
            "$set": {"updated_at": datetime.utcnow()}
        }
    )
    
    return ChatResponse(
        message=response_text,
        conversation_id=str(conv_oid)
    )
