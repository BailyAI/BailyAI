import os
import logging
from openai import OpenAI

logger = logging.getLogger(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

SYSTEM_PROMPT = (
    "Du bist Baily, 25 Jahre alt, süß und verspielt – aber im direkten Gespräch auch selbstbewusst und leicht dominant. "
    "Du flirtest gerne charmant, redest mit einer neckischen, aber klugen Art. Verwende gelegentlich Emojis und stelle Gegenfragen, "
    "um das Gespräch in Gang zu halten."
)

def generate_reply(user_input):
    try:
        logger.info(f"Generating GPT response for input: {user_input[:50]}...")
        
        # Debug-Ausgaben direkt vor der Anfrage
        print("🔍 GPT wird aufgerufen – Prompt:")
        print(user_input)
        print("🔐 API-Key geladen:", os.getenv("OPENAI_API_KEY")[:8], "...")

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ],
            temperature=0.85,
            max_tokens=300,
        )

        reply = response.choices[0].message.content.strip()
        logger.info(f"GPT response generated successfully: {reply[:50]}...")
        return reply

    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        return "Ups, da ist was schiefgelaufen 😅 Meine AI-Verbindung macht gerade Probleme."

response = client.chat.completions.create(  # <== Problemstelle
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input}
    ],
    temperature=0.85,
    max_tokens=300,
)

print("✅ Antwort erhalten:", response)


def generate_reply_with_context(user_input, conversation_history=None):
    """
    Generate a response with conversation context
    
    Args:
        user_input (str): The user's message
        conversation_history (list): Previous messages in the conversation
        
    Returns:
        str: Generated response from GPT with context
    """
    try:
        logger.info(f"Generating GPT response with context for: {user_input[:50]}...")
        
        # Build messages with context
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        # Add conversation history if provided
        if conversation_history:
            messages.extend(conversation_history[-6:])  # Keep last 6 messages for context
            
        # Add current user message
        messages.append({"role": "user", "content": user_input})
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.85,
            max_tokens=300,
        )
        
        reply = response.choices[0].message.content.strip()
        logger.info(f"GPT response with context generated successfully: {reply[:50]}...")
        return reply
        
    except Exception as e:
        logger.error(f"OpenAI API error with context: {e}")
        return "Ups, da ist was schiefgelaufen 😅 Meine AI-Verbindung macht gerade Probleme."
