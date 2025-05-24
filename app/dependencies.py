from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from bson import ObjectId

from app.database import get_database
from app.schemas import TokenData, User as UserSchema
from app.config import settings

# Make OAuth2PasswordBearer optional for public endpoints
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token", auto_error=False)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# Helper to convert MongoDB user doc to UserSchema
def user_doc_to_schema(doc):
    if not doc:
        return None
    return UserSchema(
        id=str(doc["_id"]),
        username=doc["username"],
        email=doc["email"],
        is_active=doc.get("is_active", True),
        created_at=doc.get("created_at", datetime.utcnow()),
    )

async def get_current_user(token: Optional[str] = Depends(oauth2_scheme), db=Depends(get_database)) -> Optional[UserSchema]:
    if not token:
        return None
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
    except JWTError:
        return None
    
    user_doc = await db["users"].find_one({"_id": ObjectId(user_id)})
    if user_doc is None:
        return None
    
    return user_doc_to_schema(user_doc)

async def get_current_active_user(current_user: Optional[UserSchema] = Depends(get_current_user)) -> UserSchema:
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def get_current_user_optional(token: Optional[str] = Depends(oauth2_scheme), db=Depends(get_database)) -> Optional[UserSchema]:
    return await get_current_user(token, db)
