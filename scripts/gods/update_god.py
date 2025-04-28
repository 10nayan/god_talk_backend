import asyncio
import argparse
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import God

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

async def update_god(god_id, name=None, description=None, system_prompt=None):
    """Update an existing god in the database."""
    db = SessionLocal()
    try:
        # Check if god exists
        god = db.query(God).filter(God.id == god_id).first()
        if not god:
            print(f"Error: No god found with ID {god_id}.")
            print("Use 'python list_gods.py' to see all available gods.")
            return False
        
        # Show current values
        print(f"\nCurrent values for god '{god.name}' (ID: {god.id}):")
        print(f"Name: {god.name}")
        print(f"Description: {god.description}")
        print(f"System Prompt: {god.system_prompt[:50]}...\n")
        
        # Update values if provided
        updated = False
        
        if name and name != god.name:
            # Check if the new name already exists
            existing = db.query(God).filter(God.name == name).first()
            if existing and existing.id != god_id:
                print(f"Error: A god with the name '{name}' already exists.")
                return False
            
            god.name = name
            updated = True
            print(f"Name updated to: {name}")
        
        if description and description != god.description:
            god.description = description
            updated = True
            print(f"Description updated.")
        
        if system_prompt and system_prompt != god.system_prompt:
            god.system_prompt = system_prompt
            updated = True
            print(f"System prompt updated.")
        
        if updated:
            db.commit()
            print(f"\nSuccessfully updated god with ID {god.id}.")
            return True
        else:
            print("No changes were made.")
            return False
    except Exception as e:
        print(f"Error updating god: {str(e)}")
        return False
    finally:
        db.close()

def main():
    parser = argparse.ArgumentParser(description="Update an existing god in the God Talk API.")
    parser.add_argument("--id", type=int, required=True, help="ID of the god to update")
    parser.add_argument("--name", help="New name for the god")
    parser.add_argument("--description", help="New description for the god")
    parser.add_argument("--prompt", help="New system prompt for the god")
    
    args = parser.parse_args()
    
    # Ensure at least one update parameter is provided
    if not (args.name or args.description or args.prompt):
        print("Error: At least one of --name, --description, or --prompt must be provided.")
        return
    
    asyncio.run(update_god(args.id, args.name, args.description, args.prompt))

if __name__ == "__main__":
    main()
