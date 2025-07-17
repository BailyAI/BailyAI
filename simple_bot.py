from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import os

# Konfiguration
BOT_TOKEN = "7664066988:AAHgjstUI8lX29LLjEK_7Gkch5qu6kOHtbA"
ADMIN_ID = 6546178150

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hey, ich bin Baily 😇\nBereit zum Chatten?")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ich bin Baily. Nutze /start, /whoami oder /status.")

async def whoami(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    await update.message.reply_text(f"Deine Telegram-ID ist: {user_id}")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id == ADMIN_ID:
        await update.message.reply_text("✅ Bot läuft einwandfrei!")
    else:
        await update.message.reply_text("⛔ Keine Berechtigung.")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ich bin noch schüchtern... aber bald chatte ich richtig 😋")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("whoami", whoami))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("Bot läuft...")
    app.run_polling()

if __name__ == "__main__":
    main()