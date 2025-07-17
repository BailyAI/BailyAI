import logging
import psutil
import os
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from config import ADMIN_ID, BOT_NAME, BOT_VERSION, ENABLE_ADMIN_FEATURES
from data.conversation_states import conversation_state

logger = logging.getLogger(__name__)

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status command with system information for admin"""
    try:
        user_id = update.effective_user.id
        
        if user_id != ADMIN_ID:
            await update.message.reply_text("⛔ Keine Berechtigung für diesen Befehl.")
            logger.warning(f"Unauthorized status access attempt by user {user_id}")
            return
        
        # Get system information
        memory = psutil.virtual_memory()
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # Get bot statistics
        active_users = conversation_state.get_active_users_count()
        total_users = conversation_state.get_total_users_count()
        
        status_message = f"🤖 <b>{BOT_NAME} Status Report</b>\n\n"
        status_message += f"📊 <b>Bot Information:</b>\n"
        status_message += f"• Version: {BOT_VERSION}\n"
        status_message += f"• Uptime: {get_uptime()}\n"
        status_message += f"• Status: ✅ Online\n\n"
        
        status_message += f"👥 <b>User Statistics:</b>\n"
        status_message += f"• Active Users: {active_users}\n"
        status_message += f"• Total Users: {total_users}\n\n"
        
        status_message += f"💻 <b>System Resources:</b>\n"
        status_message += f"• CPU Usage: {cpu_percent}%\n"
        status_message += f"• Memory Usage: {memory.percent}%\n"
        status_message += f"• Available Memory: {memory.available // (1024**2)} MB\n\n"
        
        status_message += f"🕐 <b>Last Updated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        await update.message.reply_text(status_message, parse_mode='HTML')
        logger.info(f"Status command executed by admin {user_id}")
        
    except Exception as e:
        logger.error(f"Error in status command: {e}")
        await update.message.reply_text("❌ Fehler beim Abrufen der Statusinformationen!")

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /admin command with admin panel information"""
    try:
        user_id = update.effective_user.id
        
        if user_id != ADMIN_ID:
            await update.message.reply_text("⛔ Keine Berechtigung für diesen Befehl.")
            logger.warning(f"Unauthorized admin panel access attempt by user {user_id}")
            return
        
        if not ENABLE_ADMIN_FEATURES:
            await update.message.reply_text("⚠️ Admin-Funktionen sind deaktiviert.")
            return
        
        admin_message = f"🔧 <b>{BOT_NAME} Admin Panel</b>\n\n"
        admin_message += f"📋 <b>Verfügbare Befehle:</b>\n"
        admin_message += f"• /status - System-Status anzeigen\n"
        admin_message += f"• /broadcast [Nachricht] - Nachricht an alle Nutzer senden\n"
        admin_message += f"• /admin - Dieses Panel anzeigen\n\n"
        
        admin_message += f"📈 <b>Quick Stats:</b>\n"
        admin_message += f"• Aktive Nutzer: {conversation_state.get_active_users_count()}\n"
        admin_message += f"• Gesamtnutzer: {conversation_state.get_total_users_count()}\n"
        admin_message += f"• Bot-Version: {BOT_VERSION}\n\n"
        
        admin_message += f"ℹ️ <b>Hinweise:</b>\n"
        admin_message += f"• Logs werden automatisch erstellt\n"
        admin_message += f"• Broadcast-Nachrichten werden an alle registrierten Nutzer gesendet\n"
        admin_message += f"• Nutze /status für detaillierte Systeminformationen"
        
        await update.message.reply_text(admin_message, parse_mode='HTML')
        logger.info(f"Admin panel accessed by user {user_id}")
        
    except Exception as e:
        logger.error(f"Error in admin panel: {e}")
        await update.message.reply_text("❌ Fehler beim Laden des Admin-Panels!")

async def broadcast_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /broadcast command to send messages to all users"""
    try:
        user_id = update.effective_user.id
        
        if user_id != ADMIN_ID:
            await update.message.reply_text("⛔ Keine Berechtigung für diesen Befehl.")
            logger.warning(f"Unauthorized broadcast attempt by user {user_id}")
            return
        
        if not ENABLE_ADMIN_FEATURES:
            await update.message.reply_text("⚠️ Admin-Funktionen sind deaktiviert.")
            return
        
        # Get the message to broadcast
        if not context.args:
            await update.message.reply_text(
                "📢 <b>Broadcast-Befehl:</b>\n\n"
                "Nutze: /broadcast [Deine Nachricht]\n\n"
                "Beispiel: /broadcast Hallo alle zusammen! 👋",
                parse_mode='HTML'
            )
            return
        
        broadcast_text = ' '.join(context.args)
        
        # Get all user IDs from conversation state
        user_ids = conversation_state.get_all_user_ids()
        
        if not user_ids:
            await update.message.reply_text("📭 Keine Nutzer zum Senden verfügbar.")
            return
        
        # Send broadcast message
        success_count = 0
        failed_count = 0
        
        for target_user_id in user_ids:
            try:
                await context.bot.send_message(
                    chat_id=target_user_id,
                    text=f"📢 <b>Nachricht von {BOT_NAME}:</b>\n\n{broadcast_text}",
                    parse_mode='HTML'
                )
                success_count += 1
            except Exception as e:
                logger.warning(f"Failed to send broadcast to user {target_user_id}: {e}")
                failed_count += 1
        
        # Send confirmation to admin
        result_message = f"📊 <b>Broadcast-Ergebnis:</b>\n\n"
        result_message += f"✅ Erfolgreich gesendet: {success_count}\n"
        result_message += f"❌ Fehlgeschlagen: {failed_count}\n"
        result_message += f"📝 Nachricht: {broadcast_text}"
        
        await update.message.reply_text(result_message, parse_mode='HTML')
        logger.info(f"Broadcast sent by admin {user_id}: {success_count} success, {failed_count} failed")
        
    except Exception as e:
        logger.error(f"Error in broadcast command: {e}")
        await update.message.reply_text("❌ Fehler beim Senden der Broadcast-Nachricht!")

def get_uptime():
    """Get bot uptime information"""
    try:
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
        
        hours, remainder = divmod(int(uptime_seconds), 3600)
        minutes, seconds = divmod(remainder, 60)
        
        return f"{hours}h {minutes}m {seconds}s"
    except:
        return "Unbekannt"
