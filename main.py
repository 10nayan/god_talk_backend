import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
import logging

from app.routers import auth, conversations, gods, questions, feedback

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="God Talk API",
    description="An API for having conversations with different Gods using ChatGPT",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.ALLOWED_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
logger.info("Including routers...")
app.include_router(auth.router)
app.include_router(gods.router)
app.include_router(conversations.router)
app.include_router(questions.router)
app.include_router(feedback.router)
logger.info("All routers included")

@app.get("/")
def read_root():
    return {"message": "Welcome to God Talk API. Use /docs to view the API documentation."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
