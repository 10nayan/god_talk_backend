import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API base URL
BASE_URL = "http://localhost:8000"

# Test user credentials
TEST_USER = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
}

def test_api():
    print("Testing God Talk API...")
    
    # Step 1: Register a new user
    print("\n1. Registering a new user...")
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json=TEST_USER
        )
        if response.status_code == 200:
            print("✅ User registered successfully")
            user_data = response.json()
            print(f"User ID: {user_data['id']}")
        else:
            print(f"❌ Failed to register user: {response.text}")
            # If user already exists, continue with the test
            if "already registered" in response.text:
                print("Continuing with existing user...")
            else:
                return
    except Exception as e:
        print(f"❌ Error during registration: {str(e)}")
        return
    
    # Step 2: Get access token
    print("\n2. Getting access token...")
    try:
        response = requests.post(
            f"{BASE_URL}/auth/token",
            data={
                "username": TEST_USER["username"],
                "password": TEST_USER["password"]
            }
        )
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data["access_token"]
            print("✅ Access token obtained successfully")
            
            # Set authorization header for subsequent requests
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
        else:
            print(f"❌ Failed to get access token: {response.text}")
            return
    except Exception as e:
        print(f"❌ Error getting access token: {str(e)}")
        return
    
    # Step 3: List available gods
    print("\n3. Listing available gods...")
    try:
        response = requests.get(
            f"{BASE_URL}/gods",
            headers=headers
        )
        if response.status_code == 200:
            gods = response.json()
            print("✅ Gods retrieved successfully")
            print(f"Found {len(gods)} gods:")
            for god in gods:
                print(f"  - {god['name']}: {god['description'][:50]}...")
            
            # Select the first god for testing
            if gods:
                test_god = gods[0]
                god_id = test_god["id"]
            else:
                print("❌ No gods found. Please run init_db.py first.")
                return
        else:
            print(f"❌ Failed to retrieve gods: {response.text}")
            return
    except Exception as e:
        print(f"❌ Error listing gods: {str(e)}")
        return
    
    # Step 4: Create a new conversation
    print(f"\n4. Creating a new conversation with {test_god['name']}...")
    try:
        response = requests.post(
            f"{BASE_URL}/conversations",
            headers=headers,
            json={
                "title": f"Test conversation with {test_god['name']}",
                "god_id": god_id
            }
        )
        if response.status_code == 200:
            conversation = response.json()
            conversation_id = conversation["id"]
            print(f"✅ Conversation created successfully with ID: {conversation_id}")
        else:
            print(f"❌ Failed to create conversation: {response.text}")
            return
    except Exception as e:
        print(f"❌ Error creating conversation: {str(e)}")
        return
    
    # Step 5: Send a message to the god
    print(f"\n5. Sending a message to {test_god['name']}...")
    try:
        test_message = f"Hello {test_god['name']}, who are you and what is your purpose?"
        
        response = requests.post(
            f"{BASE_URL}/conversations/chat",
            headers=headers,
            json={
                "conversation_id": conversation_id,
                "message": test_message
            }
        )
        if response.status_code == 200:
            chat_response = response.json()
            print("✅ Message sent and response received:")
            print(f"\nYou: {test_message}")
            print(f"\n{test_god['name']}: {chat_response['message']}")
        else:
            print(f"❌ Failed to send message: {response.text}")
            return
    except Exception as e:
        print(f"❌ Error sending message: {str(e)}")
        return
    
    # Step 6: Get conversation details
    print(f"\n6. Retrieving conversation details...")
    try:
        response = requests.get(
            f"{BASE_URL}/conversations/{conversation_id}",
            headers=headers
        )
        if response.status_code == 200:
            conversation_details = response.json()
            print("✅ Conversation details retrieved successfully")
            print(f"Title: {conversation_details['title']}")
            print(f"Messages: {len(conversation_details['messages'])}")
        else:
            print(f"❌ Failed to retrieve conversation details: {response.text}")
    except Exception as e:
        print(f"❌ Error retrieving conversation details: {str(e)}")
    
    print("\n✅ API test completed successfully!")

if __name__ == "__main__":
    test_api()
