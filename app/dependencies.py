from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import logging

from app.database import get_database
from app.schemas import TokenData, User as UserSchema
from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Set up logging (keeping import but not using logger instances)
logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

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

async def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_database)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user_doc = await db["users"].find_one({"username": token_data.username})
    if user_doc is None:
        raise credentials_exception
    return user_doc_to_schema(user_doc)

async def get_current_active_user(current_user: UserSchema = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Dependency to get token or None without raising HTTPException
# Manually call oauth2_scheme and catch HTTPException
async def get_token_or_none(request: Request) -> Optional[str]:
    try:
        # Manually call the oauth2_scheme dependency
        token: str = await oauth2_scheme(request=request)
        return token
    except HTTPException as e:
        if e.status_code == status.HTTP_401_UNAUTHORIZED:
            return None
        raise e
    except Exception:
        return None

async def get_optional_user(token: Optional[str] = Depends(get_token_or_none), db=Depends(get_database)):
    if not token:
        return None
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        token_data = TokenData(username=username)
        user_doc = await db["users"].find_one({"username": token_data.username})
        if user_doc is None:
            return None
        return user_doc_to_schema(user_doc)
    except JWTError:
        return None
    except Exception:
        return None
