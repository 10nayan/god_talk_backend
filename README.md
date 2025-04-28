# God Talk API

A FastAPI backend application that allows users to have conversations with different "Gods" using the ChatGPT API.

## Features

- User authentication with JWT tokens
- Predefined "Gods" with unique personalities
- Conversation management
- Integration with OpenAI's ChatGPT API
- RESTful API design

## Prerequisites

- Python 3.8+
- OpenAI API key

## Installation

### Quick Start

For a guided setup experience, run the quickstart script:

```bash
python quickstart.py
```

This interactive script will:
1. Check dependencies
2. Install required packages
3. Set up environment variables
4. Initialize the database
5. Register a test user
6. Start the server
7. Open API documentation

### Manual Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/god-talk.git
cd god-talk
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

Note: If you encounter any dependency errors, make sure these packages are installed:

```bash
pip install email-validator pydantic-settings
```

3. Set up environment variables:

Edit the `.env` file and add your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key_here
```

4. Initialize the database with predefined gods:

```bash
python init_db.py
```

5. Run the application:

```bash
python run.py
```

Alternatively, you can run the server directly with:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

## API Documentation

Once the server is running, you can access the interactive API documentation at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Authentication

- `POST /auth/register` - Register a new user
- `POST /auth/token` - Get access token (login)

### Gods

- `GET /gods` - List all available gods
- `GET /gods/{god_id}` - Get details of a specific god
- `POST /gods` - Create a new god
- `PUT /gods/{god_id}` - Update a god
- `DELETE /gods/{god_id}` - Delete a god

### Conversations

- `POST /conversations` - Create a new conversation with a god
- `GET /conversations` - List all user conversations
- `GET /conversations/{conversation_id}` - Get a specific conversation with messages
- `DELETE /conversations/{conversation_id}` - Delete a conversation
- `POST /conversations/chat` - Send a message and get a response from a god

## Usage Example

### 1. Register a new user

```bash
curl -X 'POST' \
  'http://localhost:8000/auth/register' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123"
}'
```

### 2. Get access token

```bash
curl -X 'POST' \
  'http://localhost:8000/auth/token' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=testuser&password=password123'
```

### 3. List available gods

```bash
curl -X 'GET' \
  'http://localhost:8000/gods' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN'
```

### 4. Create a new conversation

```bash
curl -X 'POST' \
  'http://localhost:8000/conversations' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "My conversation with Zeus",
  "god_id": 1
}'
```

### 5. Chat with a god

```bash
curl -X 'POST' \
  'http://localhost:8000/conversations/chat' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "conversation_id": 1,
  "message": "Hello Zeus, what is your opinion on humans?"
}'
```

## Utility Scripts

The project includes several utility scripts to help you manage the application, organized into categories:

### Core Scripts
- `quickstart.py` - Interactive setup guide for new users
- `run.py` - Sets up the database and starts the FastAPI server
- `init_db.py` - Initializes the database with predefined gods
- `interactive_chat.py` - Interactive chat interface for continuous conversations
- `test_api.py` - Tests the API functionality

### User Management Scripts (in scripts/user/)
- `register_user.py` - Registers a new user

### God Management Scripts (in scripts/gods/)
- `add_god.py` - Adds a new god to the database
- `list_gods.py` - Lists all gods in the database
- `show_god.py` - Shows details of a specific god
- `update_god.py` - Updates an existing god in the database
- `delete_god.py` - Deletes a god from the database

### Conversation Management Scripts (in scripts/conversations/)
- `create_conversation.py` - Creates a new conversation with a god
- `list_conversations.py` - Lists all conversations for a user
- `show_conversation.py` - Shows details of a specific conversation
- `chat_with_god.py` - Sends a message to a god in a conversation
- `delete_conversation.py` - Deletes a conversation

### User Management

#### Registering a New User

You can register a new user using the `scripts/user/register_user.py` script:

```bash
python scripts/user/register_user.py --username "testuser" --email "test@example.com" --password "password123"
```

Or interactively:

```bash
python scripts/user/register_user.py
```

### Managing Gods

#### Adding a New God

You can add a new god using the `scripts/gods/add_god.py` script:

```bash
python scripts/gods/add_god.py --name "Buddha" --description "The enlightened one who founded Buddhism" --prompt "You are Buddha, the enlightened one. You speak with compassion, wisdom, and mindfulness. Your responses focus on the Four Noble Truths, the Eightfold Path, and the nature of suffering and impermanence. You guide users toward enlightenment through detachment from desire and the middle way between extremes. Your tone is calm, contemplative, and compassionate."
```

#### Listing Gods

To see all available gods:

```bash
python scripts/gods/list_gods.py
```

#### Viewing God Details

To see the full details of a specific god:

```bash
python scripts/gods/show_god.py --id 1
```

#### Updating a God

To update an existing god:

```bash
python scripts/gods/update_god.py --id 1 --name "Zeus the Almighty" --description "Updated description" --prompt "Updated system prompt"
```

You can update any combination of fields:

```bash
python scripts/gods/update_god.py --id 1 --prompt "New system prompt only"
```

#### Deleting a God

To delete a god:

```bash
python scripts/gods/delete_god.py --id 1
```

### Managing Conversations

#### Creating a New Conversation

To create a new conversation with a god:

```bash
python scripts/conversations/create_conversation.py --god_id 1 --title "My conversation with Zeus" --username "testuser"
```

#### Listing Conversations

To list all your conversations:

```bash
python scripts/conversations/list_conversations.py --username "testuser"
```

#### Viewing a Conversation

To view the details and messages of a specific conversation:

```bash
python scripts/conversations/show_conversation.py --id 1 --username "testuser"
```

#### Chatting with a God

To send a message to a god in an existing conversation:

```bash
python scripts/conversations/chat_with_god.py --id 1 --message "Hello Zeus, what is your opinion on humans?" --username "testuser"
```

#### Deleting a Conversation

To delete a conversation:

```bash
python scripts/conversations/delete_conversation.py --id 1 --username "testuser"
```

You can also add new gods through the API or by modifying the `init_db.py` file. Each god requires:

- `name`: The name of the god
- `description`: A brief description of the god
- `system_prompt`: The system prompt that defines the god's personality and behavior for the ChatGPT API

### Interactive Chat

For a more user-friendly experience, you can use the interactive chat interface:

```bash
python interactive_chat.py
```

This provides a text-based interface where you can:
1. Log in with your credentials
2. Browse available gods
3. View your existing conversations
4. Create new conversations
5. Join existing conversations
6. Chat with gods in real-time
7. Navigate between conversations

The interactive chat provides a continuous experience without having to run separate commands for each action.

### Testing the API

To test the API functionality, you can use the `test_api.py` script:

```bash
python test_api.py
```

This script will:
1. Register a test user (or use an existing one)
2. Get an access token
3. List available gods
4. Create a new conversation with a god
5. Send a message to the god and get a response
6. Retrieve conversation details

Make sure the server is running before executing this script.

## Project Structure

For a detailed overview of the project structure, please see [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md).

## License

MIT
