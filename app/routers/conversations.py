from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from bson import ObjectId
from datetime import datetime

from app.database import get_database
from app.schemas import Conversation as ConversationSchema, ConversationCreate, Message as MessageSchema, ChatRequest, ChatResponse
from app.dependencies import get_current_active_user
from app.services.openai_service import OpenAIService

router = APIRouter(
    prefix="/conversations",
    tags=["conversations"],
    responses={404: {"description": "Not found"}},
)

# Helpers to convert MongoDB docs to schemas
def conversation_doc_to_schema(doc, messages=None, god=None):
    if not doc:
        return None
    return ConversationSchema(
        id=str(doc["_id"]),
        title=doc["title"],
        user_id=str(doc["user_id"]),
        god_id=str(doc["god_id"]),
        created_at=doc.get("created_at", datetime.utcnow()),
        updated_at=doc.get("updated_at"),
        messages=messages or [],
        god=god,
    )

def message_doc_to_schema(doc):
    if not doc:
        return None
    return MessageSchema(
        id=str(doc["_id"]),
        conversation_id=str(doc["conversation_id"]),
        content=doc["content"],
        is_from_user=doc.get("is_from_user", True),
        created_at=doc.get("created_at", datetime.utcnow()),
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
    current_user=Depends(get_current_active_user)
):
    """Create a new conversation with a god if one doesn't exist."""
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
    current_user=Depends(get_current_active_user)
):
    # Get all conversations for the user
    cursor = db["conversations"].find({"user_id": ObjectId(current_user.id)}).sort("updated_at", -1).skip(skip).limit(limit)
    conversations = [doc async for doc in cursor]
    
    # Filter conversations that have at least one message and get god details
    result = []
    for conv in conversations:
        # Check if conversation has any messages
        msg_count = await db["messages"].count_documents({"conversation_id": conv["_id"]})
        if msg_count > 0:
            god = await db["gods"].find_one({"_id": conv["god_id"]})
            if god:
                from app.routers.gods import god_doc_to_schema
                god_schema = god_doc_to_schema(god)
                result.append(conversation_doc_to_schema(conv, god=god_schema))
            else:
                result.append(conversation_doc_to_schema(conv))
    
    return result

@router.get("/{conversation_id}", response_model=ConversationSchema)
async def get_conversation(
    conversation_id: str,
    db=Depends(get_database),
    current_user=Depends(get_current_active_user)
):
    try:
        oid = ObjectId(conversation_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Conversation not found")
    conv_doc = await db["conversations"].find_one({"_id": oid, "user_id": ObjectId(current_user.id)})
    if not conv_doc:
        raise HTTPException(status_code=404, detail="Conversation not found")
    # Get messages
    msg_cursor = db["messages"].find({"conversation_id": oid}).sort("created_at", 1)
    messages = [message_doc_to_schema(doc) async for doc in msg_cursor]
    # Get god
    god_doc = await db["gods"].find_one({"_id": conv_doc["god_id"]})
    god = None
    if god_doc:
        from app.routers.gods import god_doc_to_schema
        god = god_doc_to_schema(god_doc)
    return conversation_doc_to_schema(conv_doc, messages=messages, god=god)

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
    current_user=Depends(get_current_active_user)
):
    try:
        conv_oid = ObjectId(chat_request.conversation_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Conversation not found")
    conversation = await db["conversations"].find_one({"_id": conv_oid, "user_id": ObjectId(current_user.id)})
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    god = await db["gods"].find_one({"_id": conversation["god_id"]})
    if not god:
        raise HTTPException(status_code=404, detail="God not found")
    # Save the user message
    user_message_doc = {
        "conversation_id": conv_oid,
        "content": chat_request.message,
        "is_from_user": True,
        "created_at": datetime.utcnow(),
    }
    await db["messages"].insert_one(user_message_doc)
    # Get conversation history
    msg_cursor = db["messages"].find({"conversation_id": conv_oid}).sort("created_at", 1)
    messages = [message_doc_to_schema(doc) async for doc in msg_cursor]
    # Format messages for OpenAI
    formatted_messages = OpenAIService.format_conversation_history(messages)
    # Generate response from OpenAI
    response_text = await OpenAIService.generate_response(
        messages=formatted_messages,
        system_prompt=god.get("system_prompt", "")
    )
    # Save the god's response
    god_message_doc = {
        "conversation_id": conv_oid,
        "content": response_text,
        "is_from_user": False,
        "created_at": datetime.utcnow(),
    }
    await db["messages"].insert_one(god_message_doc)
    # Update conversation's updated_at timestamp
    await db["conversations"].update_one({"_id": conv_oid}, {"$set": {"updated_at": datetime.utcnow()}})
    return ChatResponse(
        message=response_text,
        conversation_id=str(conv_oid)
    )
