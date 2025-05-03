from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from passlib.context import CryptContext
from bson import ObjectId

from app.database import get_database
from app.schemas import Token, UserCreate, User as UserSchema
from app.config import settings
from app.dependencies import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
    responses={401: {"description": "Unauthorized"}},
)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

async def authenticate_user(db, username: str, password: str):
    user = await db["users"].find_one({"username": username})
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user

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

@router.post("/register", response_model=UserSchema)
async def register_user(user: UserCreate, db=Depends(get_database)):
    # Check if username already exists
    if await db["users"].find_one({"username": user.username}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    # Check if email already exists
    if await db["users"].find_one({"email": user.email}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    hashed_password = get_password_hash(user.password)
    user_doc = {
        "username": user.username,
        "email": user.email,
        "hashed_password": hashed_password,
        "is_active": True,
        "created_at": datetime.utcnow(),
    }
    result = await db["users"].insert_one(user_doc)
    new_user = await db["users"].find_one({"_id": result.inserted_id})
    return user_doc_to_schema(new_user)

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db=Depends(get_database)
):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
