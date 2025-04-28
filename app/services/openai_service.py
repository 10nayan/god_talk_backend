from openai import AsyncOpenAI
from typing import List, Dict, Any
import httpx
from app.config import settings

# Initialize the OpenAI client with a custom HTTP client
http_client = httpx.AsyncClient()
client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY, http_client=http_client)

class OpenAIService:
    @staticmethod
    async def generate_response(messages: List[Dict[str, str]], system_prompt: str) -> str:
        """
        Generate a response using the OpenAI API.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            system_prompt: The system prompt to set the god's personality
            
        Returns:
            The generated response text
        """
        try:
            # Prepend the system message to set the god's personality
            full_messages = [{"role": "system", "content": system_prompt}]
            full_messages.extend(messages)
            
            # Call the OpenAI API
            response = await client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=full_messages,
                max_tokens=1000,
                temperature=0.7,
            )
            
            # Extract and return the generated text
            return response.choices[0].message.content.strip()
        except Exception as e:
            # Log the error and return a fallback message
            print(f"Error generating response from OpenAI: {str(e)}")
            return "I apologize, but I am unable to respond at the moment. Please try again later."
    
    @staticmethod
    def format_conversation_history(messages: List[Any]) -> List[Dict[str, str]]:
        """
        Format the conversation history into the format expected by the OpenAI API.
        
        Args:
            messages: List of Message objects from the database
            
        Returns:
            List of message dictionaries with 'role' and 'content'
        """
        formatted_messages = []
        
        for message in messages:
            role = "user" if message.is_from_user else "assistant"
            formatted_messages.append({
                "role": role,
                "content": message.content
            })
        
        return formatted_messages
