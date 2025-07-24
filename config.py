import os

BOT_NAME = "Baily"
BOT_VERSION = "1.0"
BOT_DESCRIPTION = "Ich bin Baily – deine süße AI-Begleitung"

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN fehlt! Bitte im Render Environment setzen.")

ADMIN_ID = int(os.getenv("ADMIN_ID") or 123456789)

# Neue Flags für Steuerung
ENABLE_CONVERSATION_MODE = True
ENABLE_OPENAI = True  # Gemini statt OpenAI verwenden
