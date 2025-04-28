import asyncio
import argparse
import requests
import os
import sys
from getpass import getpass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API base URL
BASE_URL = "http://localhost:8000"

class GodTalkClient:
    def __init__(self):
        self.access_token = None
        self.headers = None
        self.current_conversation = None
        self.current_god = None
    
    async def login(self, username, password):
        """Log in and get access token."""
        try:
            response = requests.post(
                f"{BASE_URL}/auth/token",
                data={
                    "username": username,
                    "password": password
                }
            )
            
            if response.status_code != 200:
                print(f"Authentication failed: {response.text}")
                return False
            
            token_data = response.json()
            self.access_token = token_data["access_token"]
            self.headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            return True
        except Exception as e:
            print(f"Error during login: {str(e)}")
            return False
    
    async def list_gods(self):
        """List all available gods."""
        try:
            response = requests.get(
                f"{BASE_URL}/gods",
                headers=self.headers
            )
            
            if response.status_code != 200:
                print(f"Failed to retrieve gods: {response.text}")
                return None
            
            return response.json()
        except Exception as e:
            print(f"Error listing gods: {str(e)}")
            return None
    
    async def list_conversations(self):
        """List all conversations for the user."""
        try:
            response = requests.get(
                f"{BASE_URL}/conversations",
                headers=self.headers
            )
            
            if response.status_code != 200:
                print(f"Failed to retrieve conversations: {response.text}")
                return None
            
            return response.json()
        except Exception as e:
            print(f"Error listing conversations: {str(e)}")
            return None
    
    async def get_conversation(self, conversation_id):
        """Get details of a specific conversation."""
        try:
            response = requests.get(
                f"{BASE_URL}/conversations/{conversation_id}",
                headers=self.headers
            )
            
            if response.status_code != 200:
                print(f"Failed to retrieve conversation: {response.text}")
                return None
            
            return response.json()
        except Exception as e:
            print(f"Error retrieving conversation: {str(e)}")
            return None
    
    async def create_conversation(self, god_id, title):
        """Create a new conversation with a god."""
        try:
            response = requests.post(
                f"{BASE_URL}/conversations",
                headers=self.headers,
                json={
                    "title": title,
                    "god_id": god_id
                }
            )
            
            if response.status_code != 200:
                print(f"Failed to create conversation: {response.text}")
                return None
            
            return response.json()
        except Exception as e:
            print(f"Error creating conversation: {str(e)}")
            return None
    
    async def send_message(self, conversation_id, message):
        """Send a message to a god in a conversation."""
        try:
            response = requests.post(
                f"{BASE_URL}/conversations/chat",
                headers=self.headers,
                json={
                    "conversation_id": conversation_id,
                    "message": message
                }
            )
            
            if response.status_code != 200:
                print(f"Failed to send message: {response.text}")
                return None
            
            return response.json()
        except Exception as e:
            print(f"Error sending message: {str(e)}")
            return None

async def interactive_chat():
    """Run an interactive chat session with a god."""
    client = GodTalkClient()
    
    # Login
    print("Welcome to God Talk Interactive Chat!")
    print("====================================\n")
    
    username = input("Username: ")
    password = getpass("Password: ")
    
    print("\nLogging in...")
    if not await client.login(username, password):
        print("Login failed. Exiting.")
        return
    
    print("✅ Login successful!\n")
    
    # Main menu
    while True:
        if client.current_conversation:
            await chat_mode(client)
        else:
            await main_menu(client)

async def main_menu(client):
    """Display the main menu."""
    print("\nMain Menu:")
    print("1. List available gods")
    print("2. List your conversations")
    print("3. Create a new conversation")
    print("4. Join an existing conversation")
    print("5. Exit")
    
    choice = input("\nEnter your choice (1-5): ")
    
    if choice == "1":
        await list_gods_menu(client)
    elif choice == "2":
        await list_conversations_menu(client)
    elif choice == "3":
        await create_conversation_menu(client)
    elif choice == "4":
        await join_conversation_menu(client)
    elif choice == "5":
        print("\nThank you for using God Talk. Goodbye!")
        sys.exit(0)
    else:
        print("\nInvalid choice. Please try again.")

async def list_gods_menu(client):
    """List all available gods."""
    print("\nRetrieving gods...")
    gods = await client.list_gods()
    
    if not gods:
        print("No gods found or error retrieving gods.")
        return
    
    print(f"\nFound {len(gods)} gods:\n")
    print(f"{'ID':<4} {'Name':<15} {'Description'}")
    print("-" * 79)
    
    for god in gods:
        # Truncate description if it's too long
        description = god['description'][:60] + "..." if len(god['description']) > 60 else god['description']
        print(f"{god['id']:<4} {god['name']:<15} {description}")

async def list_conversations_menu(client):
    """List all conversations for the user."""
    print("\nRetrieving conversations...")
    conversations = await client.list_conversations()
    
    if not conversations:
        print("No conversations found.")
        return
    
    print(f"\nFound {len(conversations)} conversations:\n")
    print(f"{'ID':<4} {'Title':<40} {'God':<15}")
    print("-" * 79)
    
    for conv in conversations:
        print(f"{conv['id']:<4} {conv['title']:<40} {conv['god']['name']:<15}")

async def create_conversation_menu(client):
    """Create a new conversation with a god."""
    # First, list available gods
    print("\nRetrieving gods...")
    gods = await client.list_gods()
    
    if not gods:
        print("No gods found or error retrieving gods.")
        return
    
    print(f"\nAvailable gods:\n")
    print(f"{'ID':<4} {'Name':<15} {'Description'}")
    print("-" * 79)
    
    for god in gods:
        # Truncate description if it's too long
        description = god['description'][:60] + "..." if len(god['description']) > 60 else god['description']
        print(f"{god['id']:<4} {god['name']:<15} {description}")
    
    # Get god ID and conversation title
    try:
        god_id = int(input("\nEnter the ID of the god you want to talk to: "))
        
        # Verify god exists
        god = next((g for g in gods if g['id'] == god_id), None)
        if not god:
            print(f"No god found with ID {god_id}.")
            return
        
        title = input(f"Enter a title for your conversation with {god['name']}: ")
        
        # Create the conversation
        print(f"\nCreating conversation with {god['name']}...")
        conversation = await client.create_conversation(god_id, title)
        
        if not conversation:
            print("Failed to create conversation.")
            return
        
        print(f"✅ Conversation created successfully!")
        
        # Set current conversation and god
        client.current_conversation = conversation
        client.current_god = god
        
        print(f"\nYou are now chatting with {god['name']}.")
        print("Type your messages and press Enter to send.")
        print("Type '/exit' to return to the main menu.")
    except ValueError:
        print("Invalid input. Please enter a valid god ID.")
    except Exception as e:
        print(f"Error: {str(e)}")

async def join_conversation_menu(client):
    """Join an existing conversation."""
    # List available conversations
    print("\nRetrieving conversations...")
    conversations = await client.list_conversations()
    
    if not conversations:
        print("No conversations found.")
        return
    
    print(f"\nYour conversations:\n")
    print(f"{'ID':<4} {'Title':<40} {'God':<15}")
    print("-" * 79)
    
    for conv in conversations:
        print(f"{conv['id']:<4} {conv['title']:<40} {conv['god']['name']:<15}")
    
    # Get conversation ID
    try:
        conversation_id = int(input("\nEnter the ID of the conversation you want to join: "))
        
        # Verify conversation exists
        conversation = next((c for c in conversations if c['id'] == conversation_id), None)
        if not conversation:
            print(f"No conversation found with ID {conversation_id}.")
            return
        
        # Get full conversation details
        print(f"\nRetrieving conversation history...")
        conversation = await client.get_conversation(conversation_id)
        
        if not conversation:
            print("Failed to retrieve conversation details.")
            return
        
        # Set current conversation and god
        client.current_conversation = conversation
        client.current_god = conversation['god']
        
        # Display conversation history
        messages = conversation['messages']
        if messages:
            print(f"\nConversation history ({len(messages)} messages):")
            print("-" * 79)
            
            for msg in messages:
                sender = "You" if msg['is_from_user'] else conversation['god']['name']
                print(f"{sender}: {msg['content']}")
            
            print("-" * 79)
        
        print(f"\nYou are now chatting with {conversation['god']['name']}.")
        print("Type your messages and press Enter to send.")
        print("Type '/exit' to return to the main menu.")
    except ValueError:
        print("Invalid input. Please enter a valid conversation ID.")
    except Exception as e:
        print(f"Error: {str(e)}")

async def chat_mode(client):
    """Interactive chat mode with a god."""
    conversation = client.current_conversation
    god = client.current_god
    
    # Clear screen
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(f"Chatting with {god['name']} - {conversation['title']}")
    print("Type '/exit' to return to the main menu.")
    print("-" * 79)
    
    while True:
        # Get user input
        user_message = input("\nYou: ")
        
        if user_message.lower() == '/exit':
            client.current_conversation = None
            client.current_god = None
            return
        
        # Send message to god
        print(f"\nSending message to {god['name']}...")
        response = await client.send_message(conversation['id'], user_message)
        
        if not response:
            print("Failed to send message. Returning to main menu.")
            client.current_conversation = None
            client.current_god = None
            return
        
        # Display god's response
        print(f"\n{god['name']}: {response['message']}")

def main():
    parser = argparse.ArgumentParser(description="Interactive chat with gods.")
    
    args = parser.parse_args()
    
    try:
        asyncio.run(interactive_chat())
    except KeyboardInterrupt:
        print("\n\nChat session terminated by user. Goodbye!")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")

if __name__ == "__main__":
    main()
