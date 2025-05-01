import asyncio
import argparse
import requests
from getpass import getpass
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API base URL from environment variable
BASE_URL = os.getenv("BACKEND_HOST_URL", "http://localhost:8000")

async def delete_conversation(conversation_id, username, password):
    """Delete a conversation."""
    try:
        # Step 1: Get access token
        print("Authenticating...")
        response = requests.post(
            f"{BASE_URL}/auth/token",
            data={
                "username": username,
                "password": password
            }
        )
        
        if response.status_code != 200:
            print(f"Authentication failed: {response.text}")
            return
        
        token_data = response.json()
        access_token = token_data["access_token"]
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        print("✅ Authentication successful")
        
        # Step 2: Get conversation details to verify it exists
        print(f"\nVerifying conversation with ID {conversation_id}...")
        response = requests.get(
            f"{BASE_URL}/conversations/{conversation_id}",
            headers=headers
        )
        
        if response.status_code != 200:
            print(f"Failed to find conversation with ID {conversation_id}: {response.text}")
            print("Use 'python list_conversations.py' to see all available conversations.")
            return
        
        conversation = response.json()
        
        # Confirm deletion
        print(f"\nYou are about to delete the conversation:")
        print(f"ID: {conversation['id']}")
        print(f"Title: {conversation['title']}")
        print(f"God: {conversation['god']['name']}")
        print(f"Messages: {len(conversation['messages'])}")
        
        confirm = input("\nAre you sure you want to delete this conversation? (y/n): ")
        
        if confirm.lower() != 'y':
            print("Deletion cancelled.")
            return
        
        # Step 3: Delete the conversation
        print(f"\nDeleting conversation...")
        response = requests.delete(
            f"{BASE_URL}/conversations/{conversation_id}",
            headers=headers
        )
        
        if response.status_code != 204:
            print(f"Failed to delete conversation: {response.text}")
            return
        
        print(f"✅ Successfully deleted conversation with ID {conversation_id}")
    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Delete a conversation.")
    parser.add_argument("--id", type=int, required=True, help="ID of the conversation to delete")
    parser.add_argument("--username", help="Username for authentication")
    parser.add_argument("--password", help="Password for authentication")
    
    args = parser.parse_args()
    
    username = args.username
    password = args.password
    
    if not username:
        username = input("Username: ")
    
    if not password:
        password = getpass("Password: ")
    
    asyncio.run(delete_conversation(args.id, username, password))

if __name__ == "__main__":
    main()
