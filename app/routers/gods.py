from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db, get_current_active_user
from app.models import God, User
from app.schemas import God as GodSchema, GodCreate

router = APIRouter(
    prefix="/gods",
    tags=["gods"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=GodSchema)
async def create_god(
    god: GodCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Check if god with the same name already exists
    db_god = db.query(God).filter(God.name == god.name).first()
    if db_god:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="God with this name already exists"
        )
    
    # Create new god
    db_god = God(
        name=god.name,
        description=god.description,
        system_prompt=god.system_prompt
    )
    db.add(db_god)
    db.commit()
    db.refresh(db_god)
    return db_god

@router.get("/", response_model=List[GodSchema])
async def get_gods(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    gods = db.query(God).offset(skip).limit(limit).all()
    return gods

@router.get("/{god_id}", response_model=GodSchema)
async def get_god(
    god_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_god = db.query(God).filter(God.id == god_id).first()
    if db_god is None:
        raise HTTPException(status_code=404, detail="God not found")
    return db_god

@router.put("/{god_id}", response_model=GodSchema)
async def update_god(
    god_id: int, 
    god: GodCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_god = db.query(God).filter(God.id == god_id).first()
    if db_god is None:
        raise HTTPException(status_code=404, detail="God not found")
    
    # Update god attributes
    db_god.name = god.name
    db_god.description = god.description
    db_god.system_prompt = god.system_prompt
    
    db.commit()
    db.refresh(db_god)
    return db_god

@router.delete("/{god_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_god(
    god_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_god = db.query(God).filter(God.id == god_id).first()
    if db_god is None:
        raise HTTPException(status_code=404, detail="God not found")
    
    db.delete(db_god)
    db.commit()
    return None
