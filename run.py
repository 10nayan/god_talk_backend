import uvicorn
import asyncio
from app.database import engine, Base
from init_db import init_db

async def setup():
    # Create database tables
    Base.metadata.create_all(bind=engine)
    
    # Initialize database with predefined gods
    await init_db()
    
    print("Database setup complete!")

if __name__ == "__main__":
    # Run database setup
    asyncio.run(setup())
    
    # Start the FastAPI server
    print("Starting God Talk API server...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
