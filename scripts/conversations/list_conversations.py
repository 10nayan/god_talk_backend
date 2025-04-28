import asyncio
import argparse
import requests
from getpass import getpass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API base URL
BASE_URL = "http://localhost:8000"

async def list_conversations(username, password):
    """List all conversations for a user."""
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
        
        # Step 2: Get conversations
        print("\nFetching conversations...")
        response = requests.get(
            f"{BASE_URL}/conversations",
            headers=headers
        )
        
        if response.status_code != 200:
            print(f"Failed to fetch conversations: {response.text}")
            return
        
        conversations = response.json()
        
        if not conversations:
            print("No conversations found.")
            print("Use the API to create a new conversation with a god.")
            return
        
        print(f"\nFound {len(conversations)} conversations:\n")
        print(f"{'ID':<4} {'Title':<40} {'God':<15} {'Created':<20}")
        print("-" * 79)
        
        for conv in conversations:
            # Format the date
            created_at = conv['created_at'].split('T')[0]
            print(f"{conv['id']:<4} {conv['title']:<40} {conv['god']['name']:<15} {created_at:<20}")
        
        print("\nTo see the messages in a conversation, use: python show_conversation.py --id <conversation_id>")
    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="List all conversations for a user.")
    parser.add_argument("--username", help="Username for authentication")
    parser.add_argument("--password", help="Password for authentication")
    
    args = parser.parse_args()
    
    username = args.username
    password = args.password
    
    if not username:
        username = input("Username: ")
    
    if not password:
        password = getpass("Password: ")
    
    asyncio.run(list_conversations(username, password))

if __name__ == "__main__":
    main()
