import os
import logging
import google.generativeai as genai

logger = logging.getLogger(__name__)

# Konfiguriere Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = (
    "Du bist Baily, 25 Jahre alt, süß und verspielt – aber im direkten Gespräch auch selbstbewusst und leicht dominant. "
    "Du flirtest gerne charmant, redest mit einer neckischen, aber klugen Art. Verwende gelegentlich Emojis und stelle Gegenfragen, "
    "um das Gespräch in Gang zu halten."
)

def generate_reply(user_input):
    try:
        logger.info(f"Gemini Anfrage wird generiert für: {user_input[:50]}...")
        
        model = genai.GenerativeModel("gemini-pro")

        chat = model.start_chat(history=[
            {"role": "user", "parts": [SYSTEM_PROMPT]},
        ])

        response = chat.send_message(user_input)
        reply = response.text.strip()
        logger.info(f"Antwort erhalten: {reply[:50]}...")
        return reply

    except Exception as e:
        logger.error(f"Gemini API Fehler: {e}")
        return "Ups, meine AI hat gerade einen kleinen Aussetzer 🛠️"
