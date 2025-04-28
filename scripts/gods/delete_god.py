import asyncio
import argparse
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import God

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

async def delete_god(god_id):
    """Delete a god from the database."""
    db = SessionLocal()
    try:
        # Check if god exists
        god = db.query(God).filter(God.id == god_id).first()
        if not god:
            print(f"Error: No god found with ID {god_id}.")
            print("Use 'python list_gods.py' to see all available gods.")
            return False
        
        # Confirm deletion
        print(f"You are about to delete the god '{god.name}' (ID: {god.id}).")
        confirm = input("Are you sure you want to proceed? (y/n): ")
        
        if confirm.lower() != 'y':
            print("Deletion cancelled.")
            return False
        
        # Delete the god
        db.delete(god)
        db.commit()
        
        print(f"Successfully deleted god '{god.name}' with ID {god.id}.")
        return True
    except Exception as e:
        print(f"Error deleting god: {str(e)}")
        return False
    finally:
        db.close()

def main():
    parser = argparse.ArgumentParser(description="Delete a god from the God Talk API.")
    parser.add_argument("--id", type=int, required=True, help="ID of the god to delete")
    
    args = parser.parse_args()
    
    asyncio.run(delete_god(args.id))

if __name__ == "__main__":
    main()
