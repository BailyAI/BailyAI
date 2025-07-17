import logging
from telegram import Update
from telegram.ext import ContextTypes
from config import BOT_NAME, BOT_VERSION, BOT_DESCRIPTION
from utils.responses import get_random_greeting, get_help_text

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command with personalized greeting"""
    try:
        user = update.effective_user
        greeting = get_random_greeting()
        
        message = f"Hey {user.first_name}! {greeting}\n\n"
        message += f"Ich bin {BOT_NAME} 😇\n"
        message += "Bereit zum Chatten?\n\n"
        message += "Nutze /help um zu sehen, was ich alles kann!"
        
        await update.message.reply_text(message)
        logger.info(f"User {user.id} ({user.username}) started the bot")
        
    except Exception as e:
        logger.error(f"Error in start command: {e}")
        await update.message.reply_text("Entschuldigung, da ist etwas schief gelaufen! 😅")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command with detailed information"""
    try:
        help_text = get_help_text()
        await update.message.reply_text(help_text, parse_mode='HTML')
        logger.info(f"Help command used by user {update.effective_user.id}")
        
    except Exception as e:
        logger.error(f"Error in help command: {e}")
        await update.message.reply_text("Entschuldigung, da ist etwas schief gelaufen! 😅")

async def whoami(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /whoami command with user information"""
    try:
        user = update.effective_user
        
        message = f"👤 <b>Deine Informationen:</b>\n\n"
        message += f"📱 <b>Telegram-ID:</b> <code>{user.id}</code>\n"
        message += f"👨‍💻 <b>Username:</b> @{user.username or 'Nicht gesetzt'}\n"
        message += f"🏷️ <b>Name:</b> {user.first_name}"
        
        if user.last_name:
            message += f" {user.last_name}"
        
        message += f"\n🌐 <b>Sprache:</b> {user.language_code or 'Unbekannt'}"
        
        await update.message.reply_text(message, parse_mode='HTML')
        logger.info(f"Whoami command used by user {user.id}")
        
    except Exception as e:
        logger.error(f"Error in whoami command: {e}")
        await update.message.reply_text("Entschuldigung, da ist etwas schief gelaufen! 😅")
