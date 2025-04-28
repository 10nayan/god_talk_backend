import asyncio
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import God

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

async def list_gods():
    """List all gods in the database."""
    db = SessionLocal()
    try:
        gods = db.query(God).all()
        
        if not gods:
            print("No gods found in the database. Run init_db.py to add predefined gods.")
            return
        
        print(f"\nFound {len(gods)} gods in the database:\n")
        print(f"{'ID':<4} {'Name':<15} {'Description':<60}")
        print("-" * 79)
        
        for god in gods:
            # Truncate description if it's too long
            description = god.description[:57] + "..." if len(god.description) > 60 else god.description
            print(f"{god.id:<4} {god.name:<15} {description:<60}")
        
        print("\nTo see the full details of a god, use: python show_god.py --id <god_id>")
    except Exception as e:
        print(f"Error listing gods: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(list_gods())
