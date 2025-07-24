import os

BOT_NAME = "Baily"
BOT_VERSION = "1.0"
BOT_DESCRIPTION = "Ich bin Baily – deine süße AI-Begleitung"

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN fehlt! Bitte im Render Environment setzen.")

ADMIN_ID = int(os.getenv("ADMIN_ID") or 123456789)

ENABLE_CONVERSATION_MODE = True
ENABLE_OPENAI = False  # falls du OpenAI endgültig ersetzt hast
ENABLE_ADMIN_FEATURES = True  # <-- Das ist die fehlende Zeile!

LOG_LEVEL = "INFO"
LOG_FILE = "logs/bot.log"
ENABLE_LOGGING = True
