import logging
import random
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from config import ENABLE_CONVERSATION_MODE, ENABLE_OPENAI
from utils.responses import get_conversation_response, get_random_reaction
from utils.openai_handler import generate_reply, generate_reply_with_context
from data.conversation_states import conversation_state

logger = logging.getLogger(__name__)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular text messages with enhanced conversation capabilities"""
    try:
        if not ENABLE_CONVERSATION_MODE:
            await update.message.reply_text("Ich bin noch schüchtern... aber bald chatte ich richtig 😋")
            return
            
        user = update.effective_user
        message_text = update.message.text.strip()
        
        # Log conversation
        logger.info(f"User {user.id} ({user.username}): {message_text}")
        
        # Get or create conversation state
        user_state = conversation_state.get_user_state(user.id)
        
        # Update last activity
        user_state['last_activity'] = datetime.now()
        user_state['message_count'] = user_state.get('message_count', 0) + 1
        
        # Use OpenAI for enhanced conversation responses if enabled
        if ENABLE_OPENAI:
            try:
                # Build conversation history for context
                conversation_history = user_state.get('conversation_history', [])
                
                # Generate response using OpenAI
                response = generate_reply_with_context(message_text, conversation_history)
                
                # Update conversation history
                conversation_history.append({"role": "user", "content": message_text})
                conversation_history.append({"role": "assistant", "content": response})
                
                # Keep only last 10 messages for context
                if len(conversation_history) > 10:
                    conversation_history = conversation_history[-10:]
                
                user_state['conversation_history'] = conversation_history
                
            except Exception as e:
                logger.error(f"OpenAI fallback error: {e}")
                # Fallback to original response system
                response = await generate_contextual_response(message_text, user_state, user)
                
                # Add some personality with reactions
                if random.random() < 0.3:  # 30% chance of reaction
                    reaction = get_random_reaction()
                    response = f"{reaction} {response}"
        else:
            # Use original response system
            response = await generate_contextual_response(message_text, user_state, user)
            
            # Add some personality with reactions
            if random.random() < 0.3:  # 30% chance of reaction
                reaction = get_random_reaction()
                response = f"{reaction} {response}"
        
        await update.message.reply_text(response)
        
        # Update conversation state
        conversation_state.update_user_state(user.id, user_state)
        
    except Exception as e:
        logger.error(f"Error handling message: {e}")
        await update.message.reply_text("Entschuldigung, da ist etwas schief gelaufen! 😅")

async def generate_contextual_response(message_text: str, user_state: dict, user):
    """Generate contextual response based on message content and user state"""
    message_lower = message_text.lower()
    
    # Greeting detection
    greetings = ['hallo', 'hi', 'hey', 'guten tag', 'guten morgen', 'guten abend', 'servus', 'moin']
    if any(greeting in message_lower for greeting in greetings):
        return f"Hallo {user.first_name}! 😊 Wie geht es dir denn heute?"
    
    # Question detection
    question_words = ['wie', 'was', 'wo', 'wann', 'warum', 'wer', 'welche', 'können', 'kannst']
    if any(word in message_lower for word in question_words) or message_text.endswith('?'):
        return get_conversation_response('question', user_state)
    
    # Emotional expressions
    positive_words = ['gut', 'toll', 'super', 'fantastisch', 'wunderbar', 'freue', 'glücklich', 'danke']
    negative_words = ['schlecht', 'traurig', 'müde', 'stress', 'problem', 'sorge', 'ärger']
    
    if any(word in message_lower for word in positive_words):
        return get_conversation_response('positive', user_state)
    elif any(word in message_lower for word in negative_words):
        return get_conversation_response('negative', user_state)
    
    # Topic-based responses
    topics = {
        'wetter': ['wetter', 'regen', 'sonne', 'kalt', 'warm', 'schnee'],
        'essen': ['essen', 'hunger', 'restaurant', 'kochen', 'rezept'],
        'musik': ['musik', 'lied', 'band', 'konzert', 'hören'],
        'sport': ['sport', 'fußball', 'tennis', 'laufen', 'fitness'],
        'arbeit': ['arbeit', 'job', 'büro', 'kollege', 'chef', 'projekt']
    }
    
    for topic, keywords in topics.items():
        if any(keyword in message_lower for keyword in keywords):
            return get_conversation_response(topic, user_state)
    
    # Default conversational response
    return get_conversation_response('general', user_state)

async def cancel_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /cancel command to reset conversation state"""
    try:
        user_id = update.effective_user.id
        conversation_state.reset_user_state(user_id)
        
        await update.message.reply_text(
            "Okay, ich habe unsere Unterhaltung zurückgesetzt! 🔄\n"
            "Du kannst jederzeit ein neues Gespräch mit mir beginnen. 😊"
        )
        
        logger.info(f"User {user_id} reset conversation state")
        
    except Exception as e:
        logger.error(f"Error in cancel conversation: {e}")
        await update.message.reply_text("Entschuldigung, da ist etwas schief gelaufen! 😅")
