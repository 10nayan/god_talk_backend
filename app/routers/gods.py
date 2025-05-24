from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from bson import ObjectId
from datetime import datetime
import pytz

from app.database import get_database
from app.schemas import God as GodSchema, GodCreate
from app.dependencies import get_current_active_user, get_current_user_optional

# Set timezone to IST
IST = pytz.timezone('Asia/Kolkata')

router = APIRouter(
    prefix="/gods",
    tags=["gods"],
    responses={404: {"description": "Not found"}},
)

# Helper to convert MongoDB doc to GodSchema
def god_doc_to_schema(doc):
    if not doc:
        return None
    
    # Convert UTC to IST for API response
    created_at = doc.get("created_at", datetime.utcnow())
    if created_at.tzinfo is None:
        created_at = pytz.utc.localize(created_at)
    created_at_ist = created_at.astimezone(IST)
    
    return GodSchema(
        id=str(doc["_id"]),
        name=doc["name"],
        description=doc["description"],
        system_prompt=doc.get("system_prompt"),
        example_phrases=doc.get("example_phrases", []),
        interaction_style=doc.get("interaction_style"),
        personality_traits=doc.get("personality_traits", []),
        image_url=doc.get("image_url"),
        religion=doc["religion"],
        created_at=created_at_ist,
    )

@router.post("/", response_model=GodSchema)
async def create_god(
    god: GodCreate,
    db=Depends(get_database),
    current_user=Depends(get_current_active_user)
):
    # Check if god with the same name already exists
    existing = await db["gods"].find_one({"name": god.name})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="God with this name already exists"
        )
    god_doc = god.dict()
    # Store UTC time in database
    god_doc["created_at"] = datetime.utcnow()
    result = await db["gods"].insert_one(god_doc)
    new_god = await db["gods"].find_one({"_id": result.inserted_id})
    return god_doc_to_schema(new_god)

@router.get("/", response_model=List[GodSchema])
async def get_gods(
    skip: int = 0,
    limit: int = 100,
    db=Depends(get_database),
    current_user=Depends(get_current_user_optional)
):
    cursor = db["gods"].find().skip(skip).limit(limit)
    gods = [god_doc_to_schema(doc) async for doc in cursor]
    return gods

@router.get("/{god_id}", response_model=GodSchema)
async def get_god(
    god_id: str,
    db=Depends(get_database),
    current_user=Depends(get_current_user_optional)
):
    try:
        oid = ObjectId(god_id)
    except Exception:
        raise HTTPException(status_code=404, detail="God not found")
    doc = await db["gods"].find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="God not found")
    return god_doc_to_schema(doc)

@router.put("/{god_id}", response_model=GodSchema)
async def update_god(
    god_id: str,
    god: GodCreate,
    db=Depends(get_database),
    current_user=Depends(get_current_active_user)
):
    try:
        oid = ObjectId(god_id)
    except Exception:
        raise HTTPException(status_code=404, detail="God not found")
    update_doc = {"$set": god.dict()}
    result = await db["gods"].update_one({"_id": oid}, update_doc)
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="God not found")
    doc = await db["gods"].find_one({"_id": oid})
    return god_doc_to_schema(doc)

@router.delete("/{god_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_god(
    god_id: str,
    db=Depends(get_database),
    current_user=Depends(get_current_active_user)
):
    try:
        oid = ObjectId(god_id)
    except Exception:
        raise HTTPException(status_code=404, detail="God not found")
    result = await db["gods"].delete_one({"_id": oid})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="God not found")
    return None
