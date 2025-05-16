import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, conversations, gods, questions

app = FastAPI(
    title="God Talk API",
    description="An API for having conversations with different Gods using ChatGPT",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(gods.router)
app.include_router(conversations.router)
app.include_router(questions.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to God Talk API. Use /docs to view the API documentation."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
