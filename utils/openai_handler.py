import os
import logging
import requests

logger = logging.getLogger(__name__)

# Gemini API-Parameter
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "models/gemini-pro"  # Alternativ: gemini-1.5-pro / gemini-1.5-flash
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta1/{GEMINI_MODEL}:generateContent"

SYSTEM_PROMPT = (
    "Du bist Baily, 25 Jahre alt, süß und verspielt – aber im direkten Gespräch auch selbstbewusst und leicht dominant. "
    "Du flirtest gerne charmant, redest mit einer neckischen, aber klugen Art. Verwende gelegentlich Emojis und stelle Gegenfragen, "
    "um das Gespräch in Gang zu halten."
)


def generate_reply(user_input):
    try:
        logger.info(f"Generating Gemini response for input: {user_input[:50]}...")
        print("🔍 Gemini wird aufgerufen – Prompt:", user_input)

        headers = {
            "Authorization": f"Bearer {GEMINI_API_KEY}",
            "Content-Type": "application/json"
        }

        body = {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {"text": SYSTEM_PROMPT + "\n\n" + user_input}
                    ]
                }
            ]
        }

        response = requests.post(GEMINI_URL, headers=headers, json=body, timeout=30)
        data = response.json()

        if response.status_code == 200 and "candidates" in data:
            reply = data["candidates"][0]["content"]["parts"][0]["text"]
            logger.info(f"Gemini response generated successfully: {reply[:50]}...")
            return reply.strip()
        else:
            logger.error(f"Gemini API response error: {data}")
            return "Ups, da ist was schiefgelaufen 😅 Meine AI-Verbindung macht gerade Probleme."

    except Exception as e:
        logger.error(f"Gemini API exception: {e}")
        return "Ups, da ist was schiefgelaufen 😅 Meine AI-Verbindung macht gerade Probleme."


def generate_reply_with_context(user_input, conversation_history=None):
    try:
        logger.info(f"Generating Gemini response with context for: {user_input[:50]}...")

        parts = [{"text": SYSTEM_PROMPT}]
        if conversation_history:
            for msg in conversation_history[-6:]:
                parts.append({"text": f"{msg['role'].capitalize()}: {msg['content']}"})

        parts.append({"text": f"User: {user_input}"})

        headers = {
            "Authorization": f"Bearer {GEMINI_API_KEY}",
            "Content-Type": "application/json"
        }

        body = {
            "contents": [
                {
                    "role": "user",
                    "parts": parts
                }
            ]
        }

        response = requests.post(GEMINI_URL, headers=headers, json=body, timeout=30)
        data = response.json()

        if response.status_code == 200 and "candidates" in data:
            reply = data["candidates"][0]["content"]["parts"][0]["text"]
            logger.info(f"Gemini contextual response generated: {reply[:50]}...")
            return reply.strip()
        else:
            logger.error(f"Gemini API error with context: {data}")
            return "Ups, da ist was schiefgelaufen 😅 Meine AI-Verbindung macht gerade Probleme."

    except Exception as e:
        logger.error(f"Gemini API exception with context: {e}")
        return "Ups, da ist was schiefgelaufen 😅 Meine AI-Verbindung macht gerade Probleme."
