#!/usr/bin/env python3
"""
Baily Bot - Ein einfacher deutscher Telegram Bot
"""

import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# Konfiguration
BOT_TOKEN = "7664066988:AAHgjstUI8lX29LLjEK_7Gkch5qu6kOHtbA"
ADMIN_ID = 6546178150

# Logging Setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    await update.message.reply_text(f"Hey {user.first_name}, ich bin Baily 😇\nBereit zum Chatten?")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = """
🤖 Baily Bot - Hilfe & Befehle

📋 Grundbefehle:
• /start - Bot starten und begrüßen
• /help - Diese Hilfe anzeigen
• /whoami - Deine Benutzerinformationen anzeigen

🔧 Admin-Befehle:
• /status - System-Status prüfen (nur Admin)

💬 Chat-Funktionen:
• Schreibe einfach eine Nachricht und ich antworte!

Viel Spaß beim Chatten! 😊
"""
    await update.message.reply_text(help_text)

async def whoami(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /whoami command"""
    user = update.effective_user
    
    message = f"👤 Deine Informationen:\n\n"
    message += f"📱 Telegram-ID: {user.id}\n"
    message += f"👨‍💻 Username: @{user.username or 'Nicht gesetzt'}\n"
    message += f"🏷️ Name: {user.first_name}"
    
    if user.last_name:
        message += f" {user.last_name}"
    
    message += f"\n🌐 Sprache: {user.language_code or 'Unbekannt'}"
    
    await update.message.reply_text(message)

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status command"""
    user_id = update.effective_user.id
    
    if user_id == ADMIN_ID:
        await update.message.reply_text("✅ Bot läuft einwandfrei!")
    else:
        await update.message.reply_text("⛔ Keine Berechtigung.")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular messages"""
    message_text = update.message.text.lower()
    
    # Greetings
    if any(greeting in message_text for greeting in ['hallo', 'hi', 'hey', 'guten tag']):
        await update.message.reply_text("Hallo! 😊 Wie geht es dir denn heute?")
    
    # Questions
    elif message_text.endswith('?') or any(word in message_text for word in ['wie', 'was', 'wo']):
        await update.message.reply_text("Das ist eine interessante Frage! 🤔 Lass mich überlegen...")
    
    # Positive expressions
    elif any(word in message_text for word in ['gut', 'toll', 'super', 'danke']):
        await update.message.reply_text("Das freut mich total zu hören! 😊 Erzähl mir mehr davon!")
    
    # Default response
    else:
        await update.message.reply_text("Interessant! 💭 Erzähl mir mehr davon!")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    logger.error(f"Update {update} caused error {context.error}")
    
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "Entschuldigung, da ist etwas schief gelaufen! 😅 "
            "Versuche es bitte nochmal."
        )

def main():
    """Main function"""
    logger.info("Starting Baily Bot...")
    
    if not BOT_TOKEN:
        logger.error("Bot token not found!")
        return
    
    try:
        # Create application
        application = ApplicationBuilder().token(BOT_TOKEN).build()
        
        # Add handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("whoami", whoami))
        application.add_handler(CommandHandler("status", status))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
        
        # Add error handler
        application.add_error_handler(error_handler)
        
        logger.info("Bot handlers registered successfully")
        print("🤖 Baily Bot läuft... Bereit zum Chatten!")
        
        # Start polling
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        print(f"❌ Fehler beim Starten des Bots: {e}")

if __name__ == "__main__":
    main()