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

async def create_conversation(god_id, title, username, password):
    """Create a new conversation with a god."""
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
        
        # Step 2: Get god details to verify it exists
        print(f"\nVerifying god with ID {god_id}...")
        response = requests.get(
            f"{BASE_URL}/gods/{god_id}",
            headers=headers
        )
        
        if response.status_code != 200:
            print(f"Failed to find god with ID {god_id}: {response.text}")
            print("Use 'python list_gods.py' to see all available gods.")
            return
        
        god = response.json()
        print(f"✅ Found god: {god['name']}")
        
        # Step 3: Create the conversation
        print(f"\nCreating conversation with {god['name']}...")
        response = requests.post(
            f"{BASE_URL}/conversations",
            headers=headers,
            json={
                "title": title,
                "god_id": god_id
            }
        )
        
        if response.status_code != 200:
            print(f"Failed to create conversation: {response.text}")
            return
        
        conversation = response.json()
        
        print(f"✅ Successfully created conversation:")
        print(f"ID: {conversation['id']}")
        print(f"Title: {conversation['title']}")
        print(f"God: {god['name']}")
        
        print(f"\nTo chat with {god['name']}, use: python chat_with_god.py --id {conversation['id']}")
    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Create a new conversation with a god.")
    parser.add_argument("--god_id", type=int, required=True, help="ID of the god to converse with")
    parser.add_argument("--title", help="Title for the conversation")
    parser.add_argument("--username", help="Username for authentication")
    parser.add_argument("--password", help="Password for authentication")
    
    args = parser.parse_args()
    
    username = args.username
    password = args.password
    title = args.title
    
    if not username:
        username = input("Username: ")
    
    if not password:
        password = getpass("Password: ")
    
    if not title:
        title = input("Enter a title for the conversation: ")
    
    asyncio.run(create_conversation(args.god_id, title, username, password))

if __name__ == "__main__":
    main()
