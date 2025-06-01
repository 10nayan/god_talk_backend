from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_optional_user
from app.database import get_database
from app.schemas import FeedbackCreate, Feedback as FeedbackSchema
from datetime import datetime
import pytz
import logging
from typing import Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/feedback",
    tags=["feedback"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=FeedbackSchema)
async def create_feedback(
    feedback: FeedbackCreate,
    current_user: Optional[dict] = Depends(get_optional_user),
    db = Depends(get_database)
):
    """
    Create new feedback.
    """
    logger.info("Received feedback request")
    try:
        feedback_doc = {
            "user_id": str(current_user.get("_id")) if current_user and current_user.get("_id") else None,
            "rating": feedback.rating,
            "likes": feedback.likes,
            "dislikes": feedback.dislikes,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = await db["feedback"].insert_one(feedback_doc)
        new_feedback = await db["feedback"].find_one({"_id": result.inserted_id})
        
        logger.info(f"Successfully created feedback with ID: {result.inserted_id}")
        return FeedbackSchema(
            id=str(new_feedback["_id"]),
            user_id=str(new_feedback["user_id"]) if new_feedback.get("user_id") else None,
            rating=new_feedback["rating"],
            likes=new_feedback["likes"],
            dislikes=new_feedback["dislikes"],
            created_at=new_feedback["created_at"],
            updated_at=new_feedback["updated_at"]
        )
    except Exception as e:
        logger.error(f"Error creating feedback: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 