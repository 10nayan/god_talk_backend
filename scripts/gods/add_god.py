import asyncio
import argparse
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import God

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

async def add_god(name, description, system_prompt):
    """Add a new god to the database."""
    db = SessionLocal()
    try:
        # Check if god with the same name already exists
        existing_god = db.query(God).filter(God.name == name).first()
        if existing_god:
            print(f"Error: A god named '{name}' already exists.")
            return False
        
        # Create new god
        new_god = God(
            name=name,
            description=description,
            system_prompt=system_prompt
        )
        db.add(new_god)
        db.commit()
        db.refresh(new_god)
        
        print(f"Successfully added god '{name}' with ID {new_god.id}.")
        return True
    except Exception as e:
        print(f"Error adding god: {str(e)}")
        return False
    finally:
        db.close()

def main():
    parser = argparse.ArgumentParser(description="Add a new god to the God Talk API.")
    parser.add_argument("--name", required=True, help="Name of the god")
    parser.add_argument("--description", required=True, help="Description of the god")
    parser.add_argument("--prompt", required=True, help="System prompt for the god's personality")
    
    args = parser.parse_args()
    
    asyncio.run(add_god(args.name, args.description, args.prompt))

if __name__ == "__main__":
    main()
