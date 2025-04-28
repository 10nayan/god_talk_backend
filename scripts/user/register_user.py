import asyncio
import argparse
import requests
import re
from getpass import getpass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API base URL
BASE_URL = "http://localhost:8000"

def validate_email(email):
    """Validate email format."""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    return True, ""

async def register_user(username, email, password):
    """Register a new user."""
    try:
        # Validate inputs
        if not username:
            print("Error: Username cannot be empty.")
            return
        
        if not validate_email(email):
            print("Error: Invalid email format.")
            return
        
        is_valid, message = validate_password(password)
        if not is_valid:
            print(f"Error: {message}")
            return
        
        # Register the user
        print(f"Registering user '{username}'...")
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json={
                "username": username,
                "email": email,
                "password": password
            }
        )
        
        if response.status_code != 200:
            print(f"Registration failed: {response.text}")
            return
        
        user_data = response.json()
        
        print(f"✅ User registered successfully!")
        print(f"Username: {user_data['username']}")
        print(f"Email: {user_data['email']}")
        print(f"User ID: {user_data['id']}")
        
        print("\nYou can now log in using your credentials.")
        print("To list available gods, use: python list_gods.py --username your_username")
    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Register a new user.")
    parser.add_argument("--username", help="Username for the new account")
    parser.add_argument("--email", help="Email for the new account")
    parser.add_argument("--password", help="Password for the new account")
    
    args = parser.parse_args()
    
    username = args.username
    email = args.email
    password = args.password
    
    if not username:
        username = input("Username: ")
    
    if not email:
        email = input("Email: ")
    
    if not password:
        password = getpass("Password: ")
        confirm_password = getpass("Confirm password: ")
        
        if password != confirm_password:
            print("Error: Passwords do not match.")
            return
    
    asyncio.run(register_user(username, email, password))

if __name__ == "__main__":
    main()
