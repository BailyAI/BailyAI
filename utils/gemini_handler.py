import google.generativeai as genai
import logging
import os

from config import GEMINI_API_KEY

logger = logging.getLogger(__name__)

genai.configure(api_key=GEMINI_API_KEY)

async def generate_reply(message: str) -> str:
    try:
        logger.info(f"Gemini Anfrage wird generiert für: {message}...")

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(message)

        return response.text.strip()
    except Exception as e:
        logger.error(f"Gemini API Fehler: {e}")
        return "Ups! Da ist etwas schief gelaufen bei meiner Antwort 🙈"
