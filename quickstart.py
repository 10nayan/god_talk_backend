#!/usr/bin/env python3
"""
God Talk API - Quick Start Guide

This script helps users get started with the God Talk API by guiding them through
the setup process and demonstrating basic functionality.
"""

import os
import sys
import time
import subprocess
import webbrowser
from getpass import getpass

def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 80)
    print(f" {text}")
    print("=" * 80)

def print_step(step_num, text):
    """Print a formatted step."""
    print(f"\n[Step {step_num}] {text}")
    print("-" * 80)

def run_command(command, show_output=True):
    """Run a shell command and return the result."""
    try:
        if show_output:
            print(f"Running: {command}")
        
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        
        if result.returncode != 0:
            print(f"Error executing command: {command}")
            print(f"Error message: {result.stderr}")
            return False
        
        if show_output and result.stdout:
            print(result.stdout)
        
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def check_dependencies():
    """Check if required dependencies are installed."""
    print_step(1, "Checking dependencies")
    
    # Check if Python is installed
    python_version = sys.version_info
    print(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("Error: Python 3.8 or higher is required.")
        return False
    
    # Check if pip is installed
    if not run_command("pip --version", show_output=True):
        print("Error: pip is not installed or not in PATH.")
        return False
    
    return True

def install_requirements():
    """Install required packages."""
    print_step(2, "Installing required packages")
    
    if not os.path.exists("requirements.txt"):
        print("Error: requirements.txt not found.")
        return False
    
    # Install requirements and ensure email-validator is inlidator
    # stalled
    success = run_command("pip install --break-system-packages -r requirements.txt")
    if not success:
        return False
    
    # Make sure email-validator and pydantic-settings are installed
    print("Ensuring required packages are installed...")
    run_command("pip install --break-system-packages email-validator pydantic-settings")
    
    return True

def setup_env_file():
    """Set up the .env file."""
    print_step(3, "Setting up environment variables")
    
    if os.path.exists(".env"):
        print(".env file already exists.")
        modify = input("Do you want to modify it? (y/n): ")
        if modify.lower() != 'y':
            return True
    
    openai_api_key = input("Enter your OpenAI API key (press Enter to skip): ")
    
    with open(".env", "w") as f:
        f.write("# Security settings\n")
        f.write("SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7\n")
        f.write("ALGORITHM=HS256\n")
        f.write("ACCESS_TOKEN_EXPIRE_MINUTES=30\n")
        f.write("\n# OpenAI API settings\n")
        
        if openai_api_key:
            f.write(f"OPENAI_API_KEY={openai_api_key}\n")
        else:
            f.write("OPENAI_API_KEY=your_openai_api_key_here\n")
            print("\nWarning: You didn't provide an OpenAI API key.")
            print("You'll need to edit the .env file later to add your key.")
        
        f.write("OPENAI_MODEL=gpt-3.5-turbo\n")
    
    print("✅ .env file created successfully.")
    return True

def initialize_database():
    """Initialize the database with predefined gods."""
    print_step(4, "Initializing database")
    
    return run_command("python init_db.py")

def register_test_user():
    """Register a test user."""
    print_step(5, "Registering a test user")
    
    username = input("Enter a username for the test user: ")
    email = input("Enter an email for the test user: ")
    password = getpass("Enter a password for the test user: ")
    
    if not username or not email or not password:
        print("Error: Username, email, and password are required.")
        return False
    
    return run_command(f"python scripts/user/register_user.py --username \"{username}\" --email \"{email}\" --password \"{password}\"")

def start_server():
    """Start the FastAPI server."""
    print_step(6, "Starting the server")
    
    print("Starting the server in a new terminal window...")
    
    # Different commands based on OS
    if sys.platform == "win32":
        # Windows
        subprocess.Popen("start cmd /k python run.py", shell=True)
    elif sys.platform == "darwin":
        # macOS
        subprocess.Popen("osascript -e 'tell app \"Terminal\" to do script \"cd $(pwd) && python run.py\"'", shell=True)
    else:
        # Linux
        subprocess.Popen("x-terminal-emulator -e 'python run.py'", shell=True)
    
    print("Waiting for the server to start...")
    time.sleep(5)  # Give the server some time to start
    
    return True

def open_api_docs():
    """Open the API documentation in a web browser."""
    print_step(7, "Opening API documentation")
    
    url = "http://localhost:8000/docs"
    print(f"Opening {url} in your default web browser...")
    
    try:
        webbrowser.open(url)
        return True
    except Exception as e:
        print(f"Error opening browser: {str(e)}")
        print(f"Please manually open {url} in your web browser.")
        return False

def show_next_steps():
    """Show next steps for the user."""
    print_header("Next Steps")
    
    print("""
Congratulations! You've successfully set up the God Talk API.

Here are some things you can do next:

1. Use the interactive chat interface:
   python interactive_chat.py

2. Explore the API documentation:
   http://localhost:8000/docs

3. Test the API functionality:
   python test_api.py

4. Manage gods:
   python scripts/gods/list_gods.py
   python scripts/gods/show_god.py --id 1
   python scripts/gods/add_god.py --name "NewGod" --description "Description" --prompt "System prompt"

5. Manage conversations:
   python scripts/conversations/list_conversations.py --username your_username
   python scripts/conversations/create_conversation.py --god_id 1 --title "My Conversation" --username your_username
   python scripts/conversations/chat_with_god.py --id 1 --message "Hello" --username your_username

For more information, please refer to the README.md file.
""")

def main():
    """Main function."""
    print_header("God Talk API - Quick Start Guide")
    
    print("""
This script will help you set up and get started with the God Talk API.
It will guide you through the following steps:

1. Check dependencies
2. Install required packages
3. Set up environment variables
4. Initialize the database
5. Register a test user
6. Start the server
7. Open API documentation

Press Ctrl+C at any time to exit.
""")
    
    input("Press Enter to continue...")
    
    if not check_dependencies():
        print("Error: Dependencies check failed.")
        return
    
    if not install_requirements():
        print("Error: Failed to install required packages.")
        return
    
    if not setup_env_file():
        print("Error: Failed to set up .env file.")
        return
    
    if not initialize_database():
        print("Error: Failed to initialize database.")
        return
    
    if not register_test_user():
        print("Error: Failed to register test user.")
        return
    
    if not start_server():
        print("Error: Failed to start server.")
        return
    
    if not open_api_docs():
        print("Warning: Failed to open API documentation in browser.")
    
    show_next_steps()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nQuick start guide terminated by user.")
        sys.exit(0)
