from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from bson import ObjectId
from datetime import datetime
import pytz

from app.database import get_database
from app.schemas import Question as QuestionSchema
from app.dependencies import get_current_active_user

# Set timezone to IST
IST = pytz.timezone('Asia/Kolkata')

router = APIRouter(
    prefix="/questions",
    tags=["questions"],
    responses={404: {"description": "Not found"}},
)

# Helper to convert MongoDB doc to QuestionSchema
def question_doc_to_schema(doc):
    if not doc:
        return None
    
    # Convert UTC to IST for API response
    created_at = doc.get("created_at", datetime.utcnow())
    if created_at.tzinfo is None:
        created_at = pytz.utc.localize(created_at)
    created_at_ist = created_at.astimezone(IST)
    
    updated_at = doc.get("updated_at")
    if updated_at:
        if updated_at.tzinfo is None:
            updated_at = pytz.utc.localize(updated_at)
        updated_at = updated_at.astimezone(IST)
    
    return QuestionSchema(
        id=str(doc["_id"]),
        question=doc["question"],
        god_id=str(doc["god_id"]),
        created_at=created_at_ist,
        updated_at=updated_at
    )

@router.get("/god/{god_id}", response_model=List[QuestionSchema])
async def get_questions_for_god(
    god_id: str,
    db=Depends(get_database),
    current_user=Depends(get_current_active_user)
):
    """Get all questions for a specific god."""
    try:
        god_oid = ObjectId(god_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Invalid god ID")

    # Check if god exists
    god = await db["gods"].find_one({"_id": god_oid})
    if not god:
        raise HTTPException(status_code=404, detail="God not found")

    # Get all questions for this god
    cursor = db["questions"].find({"god_id": god_oid})
    questions = [question_doc_to_schema(doc) async for doc in cursor]
    return questions 