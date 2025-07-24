import os


BOT_NAME = "Baily"
BOT_VERSION = "1.0"
BOT_DESCRIPTION = "Ich bin Baily – deine süße AI-Begleitung"

BOT_TOKEN = os.getenv("BOT_TOKEN") or "7664066988:AAHcg0Go0QSS1FNgXzRthqP8Nb4nd00_VuE"
ADMIN_ID = int(os.getenv("ADMIN_ID") or 123456789)  # Ersetze mit deiner Telegram-ID
