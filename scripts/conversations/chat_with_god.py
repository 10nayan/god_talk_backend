import asyncio
import argparse
import requests
from getpass import getpass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API base URL
BASE_URL = "http://localhost:8000"

async def chat_with_god(conversation_id, message, username, password):
    """Send a message to a god in a conversation."""
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
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        print("✅ Authentication successful")
        
        # Step 2: Get conversation details to know which god we're talking to
        print(f"\nFetching conversation {conversation_id}...")
        response = requests.get(
            f"{BASE_URL}/conversations/{conversation_id}",
            headers=headers
        )
        
        if response.status_code != 200:
            print(f"Failed to fetch conversation: {response.text}")
            return
        
        conversation = response.json()
        god_name = conversation['god']['name']
        
        print(f"✅ Conversation found: '{conversation['title']}' with {god_name}")
        
        # Step 3: Send message to the god
        print(f"\nSending message to {god_name}...")
        response = requests.post(
            f"{BASE_URL}/conversations/chat",
            headers=headers,
            json={
                "conversation_id": conversation_id,
                "message": message
            }
        )
        
        if response.status_code != 200:
            print(f"Failed to send message: {response.text}")
            return
        
        chat_response = response.json()
        
        # Display the conversation
        print("\n" + "=" * 80)
        print(f"You:")
        print(f"{message}")
        print("\n" + "-" * 80)
        print(f"{god_name}:")
        print(f"{chat_response['message']}")
        print("=" * 80)
        
        print(f"\nTo view the full conversation, use: python show_conversation.py --id {conversation_id}")
    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Send a message to a god in a conversation.")
    parser.add_argument("--id", type=int, required=True, help="ID of the conversation")
    parser.add_argument("--message", help="Message to send to the god")
    parser.add_argument("--username", help="Username for authentication")
    parser.add_argument("--password", help="Password for authentication")
    
    args = parser.parse_args()
    
    username = args.username
    password = args.password
    message = args.message
    
    if not username:
        username = input("Username: ")
    
    if not password:
        password = getpass("Password: ")
    
    if not message:
        message = input("Enter your message: ")
    
    asyncio.run(chat_with_god(args.id, message, username, password))

if __name__ == "__main__":
    main()
