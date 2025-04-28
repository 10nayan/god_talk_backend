import asyncio
import argparse
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import God

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

async def show_god(god_id):
    """Show details of a specific god."""
    db = SessionLocal()
    try:
        god = db.query(God).filter(God.id == god_id).first()
        
        if not god:
            print(f"Error: No god found with ID {god_id}.")
            print("Use 'python list_gods.py' to see all available gods.")
            return
        
        print("\n" + "=" * 80)
        print(f"God ID: {god.id}")
        print(f"Name: {god.name}")
        print(f"Created: {god.created_at}")
        print("-" * 80)
        print("Description:")
        print(god.description)
        print("-" * 80)
        print("System Prompt:")
        print(god.system_prompt)
        print("=" * 80)
    except Exception as e:
        print(f"Error showing god: {str(e)}")
    finally:
        db.close()

def main():
    parser = argparse.ArgumentParser(description="Show details of a specific god.")
    parser.add_argument("--id", type=int, required=True, help="ID of the god to show")
    
    args = parser.parse_args()
    
    asyncio.run(show_god(args.id))

if __name__ == "__main__":
    main()
