import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from config import BOT_TOKEN, ADMIN_ID
from handlers.commands import start, help_command, whoami
from handlers.conversations import handle_message, cancel_conversation
from handlers.admin import status, admin_panel, broadcast_message
from utils.logging_config import setup_logging
from data.conversation_states import ConversationState
from web_server import keep_alive

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Initialize conversation state manager
conversation_state = ConversationState()

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors and inform user about issues"""
    logger.error(f"Update {update} caused error {context.error}")
    
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "Entschuldigung, da ist etwas schief gelaufen! 😅 "
            "Versuche es bitte nochmal oder kontaktiere meinen Admin."
        )

def main():
    """Main function to run the bot"""
    logger.info("Starting Baily Bot...")
    
    # Start Flask web server for keep-alive
    keep_alive()
    
    # Verify token exists
    if not BOT_TOKEN:
        logger.error("Bot token not found in configuration!")
        return
    
    try:
        app = ApplicationBuilder().token(BOT_TOKEN).build()
        
        # Command handlers
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("help", help_command))
        app.add_handler(CommandHandler("whoami", whoami))
        app.add_handler(CommandHandler("status", status))
        app.add_handler(CommandHandler("admin", admin_panel))
        app.add_handler(CommandHandler("broadcast", broadcast_message))
        app.add_handler(CommandHandler("cancel", cancel_conversation))
        
        # Message handler for conversations
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        # Error handler
        app.add_error_handler(error_handler)
        
        logger.info("Bot handlers registered successfully")
        print("🤖 Baily Bot läuft... Bereit zum Chatten!")
        print("🌐 Flask web server running on port 8080")
        
        # Start polling
        app.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        print(f"❌ Fehler beim Starten des Bots: {e}")

if __name__ == "__main__":
    main()
