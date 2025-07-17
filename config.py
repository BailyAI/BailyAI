import os
from typing import Optional

# Bot configuration - prioritize environment variables for security
BOT_TOKEN: str = os.getenv("BOT_TOKEN", "7664066988:AAHgjstUI8lX29LLjEK_7Gkch5qu6kOHtbA")
ADMIN_ID: int = int(os.getenv("ADMIN_ID", "6546178150"))

# Additional configuration
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE: str = os.getenv("LOG_FILE", "bot.log")

# Bot personality settings
BOT_NAME: str = "Baily"
BOT_VERSION: str = "2.0"
BOT_DESCRIPTION: str = "Ein freundlicher deutscher Telegram-Bot mit erweiterten Chat-Funktionen"

# Feature flags
ENABLE_CONVERSATION_MODE: bool = os.getenv("ENABLE_CONVERSATION_MODE", "true").lower() == "true"
ENABLE_ADMIN_FEATURES: bool = os.getenv("ENABLE_ADMIN_FEATURES", "true").lower() == "true"
ENABLE_LOGGING: bool = os.getenv("ENABLE_LOGGING", "true").lower() == "true"
ENABLE_OPENAI: bool = os.getenv("ENABLE_OPENAI", "true").lower() == "true"

# Rate limiting
MAX_MESSAGES_PER_MINUTE: int = int(os.getenv("MAX_MESSAGES_PER_MINUTE", "20"))
