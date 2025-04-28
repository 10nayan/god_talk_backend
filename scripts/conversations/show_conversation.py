import asyncio
import argparse
import requests
from getpass import getpass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API base URL
BASE_URL = "http://localhost:8000"

async def show_conversation(conversation_id, username, password):
    """Show details of a specific conversation."""
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
        
        # Step 2: Get conversation details
        print(f"\nFetching conversation {conversation_id}...")
        response = requests.get(
            f"{BASE_URL}/conversations/{conversation_id}",
            headers=headers
        )
        
        if response.status_code != 200:
            print(f"Failed to fetch conversation: {response.text}")
            return
        
        conversation = response.json()
        
        # Display conversation details
        print("\n" + "=" * 80)
        print(f"Conversation ID: {conversation['id']}")
        print(f"Title: {conversation['title']}")
        print(f"God: {conversation['god']['name']}")
        print(f"Created: {conversation['created_at']}")
        if conversation['updated_at']:
            print(f"Last Updated: {conversation['updated_at']}")
        print("-" * 80)
        
        # Display messages
        messages = conversation['messages']
        if not messages:
            print("No messages in this conversation yet.")
            print("Use the API to send a message to the god.")
        else:
            print(f"Messages ({len(messages)}):\n")
            
            for msg in messages:
                sender = "You" if msg['is_from_user'] else conversation['god']['name']
                print(f"{sender} ({msg['created_at'].split('.')[0].replace('T', ' ')}):")
                print(f"{msg['content']}\n")
                print("-" * 80)
        
        print("\nTo send a new message to this conversation, use the API endpoint:")
        print(f"POST /conversations/chat with conversation_id={conversation_id}")
    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Show details of a specific conversation.")
    parser.add_argument("--id", type=int, required=True, help="ID of the conversation to show")
    parser.add_argument("--username", help="Username for authentication")
    parser.add_argument("--password", help="Password for authentication")
    
    args = parser.parse_args()
    
    username = args.username
    password = args.password
    
    if not username:
        username = input("Username: ")
    
    if not password:
        password = getpass("Password: ")
    
    asyncio.run(show_conversation(args.id, username, password))

if __name__ == "__main__":
    main()
