# God Talk API - Project Structure

## Directory Structure

```
god_talk/
├── app/                        # Main application package
│   ├── routers/                # API route handlers
│   │   ├── auth.py             # Authentication routes
│   │   ├── conversations.py    # Conversation management routes
│   │   └── gods.py             # God management routes
│   ├── services/               # Business logic services
│   │   └── openai_service.py   # OpenAI API integration
│   ├── config.py               # Application configuration
│   ├── database.py             # Database connection and setup
│   ├── dependencies.py         # FastAPI dependencies
│   ├── models.py               # SQLAlchemy database models
│   └── schemas.py              # Pydantic schemas for API
├── scripts/                    # Utility scripts
│   ├── user/                   # User management scripts
│   │   └── register_user.py    # Register a new user
│   ├── gods/                   # God management scripts
│   │   ├── add_god.py          # Add a new god
│   │   ├── delete_god.py       # Delete a god
│   │   ├── list_gods.py        # List all gods
│   │   ├── show_god.py         # Show details of a god
│   │   └── update_god.py       # Update a god
│   └── conversations/          # Conversation management scripts
│       ├── chat_with_god.py    # Send a message to a god
│       ├── create_conversation.py  # Create a new conversation
│       ├── delete_conversation.py  # Delete a conversation
│       ├── list_conversations.py   # List all conversations
│       └── show_conversation.py    # Show details of a conversation
├── .env                        # Environment variables
├── .gitignore                  # Git ignore file
├── init_db.py                  # Initialize database with predefined gods
├── interactive_chat.py         # Interactive chat interface
├── main.py                     # FastAPI application entry point
├── PROJECT_STRUCTURE.md        # This file
├── quickstart.py               # Quick start guide
├── README.md                   # Project documentation
├── requirements.txt            # Python dependencies
├── run.py                      # Run the application
└── test_api.py                 # Test the API functionality
```

## Current Structure

The project is organized as follows:

- Core application code is in the `app/` directory
- Utility scripts are organized in the `scripts/` directory:
  - `scripts/conversations/` contains conversation management scripts
  - `scripts/gods/` contains god management scripts
  - `scripts/user/` contains user management scripts
- Configuration and main application files are in the root directory

## Key Components

### Core Application

- **main.py**: The entry point for the FastAPI application.
- **app/**: The main application package containing all the core functionality.
- **app/routers/**: API route handlers for different endpoints.
- **app/services/**: Business logic services, including the OpenAI API integration.
- **app/models.py**: SQLAlchemy database models for users, gods, conversations, and messages.
- **app/schemas.py**: Pydantic schemas for API request and response validation.

### Database

- **app/database.py**: Database connection and setup using SQLAlchemy.
- **init_db.py**: Script to initialize the database with predefined gods.

### Configuration

- **.env**: Environment variables for the application.
- **app/config.py**: Application configuration using Pydantic settings.

### Utility Scripts

- **register_user.py**: Register a new user.
- **add_god.py**, **list_gods.py**, **show_god.py**, **update_god.py**, **delete_god.py**: God management scripts.
- **create_conversation.py**, **list_conversations.py**, **show_conversation.py**, **chat_with_god.py**, **delete_conversation.py**: Conversation management scripts.
- **interactive_chat.py**: Interactive chat interface for continuous conversations.
- **quickstart.py**: Quick start guide for new users.
- **test_api.py**: Test the API functionality.

### Documentation

- **README.md**: Project documentation.
- **PROJECT_STRUCTURE.md**: This file, explaining the project structure.
