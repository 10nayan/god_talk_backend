"""
This project now uses MongoDB via Motor. Collections are accessed directly in the code.

Example God document structure:
{
    _id: ObjectId,
    name: str,
    description: str,
    system_prompt: str,
    example_phrases: list,
    interaction_style: str,
    personality_traits: list,
    image_url: str,
    religion: str,
    created_at: datetime
}

Example User document structure:
{
    _id: ObjectId,
    username: str,
    email: str,
    hashed_password: str,
    is_active: bool,
    created_at: datetime
}

Example Conversation document structure:
{
    _id: ObjectId,
    title: str,
    user_id: ObjectId,      # Reference to User._id
    god_id: ObjectId,       # Reference to God._id
    created_at: datetime,
    updated_at: datetime
}

Example Message document structure:
{
    _id: ObjectId,
    conversation_id: ObjectId,  # Reference to Conversation._id
    content: str,
    is_from_user: bool,
    created_at: datetime
}
"""
