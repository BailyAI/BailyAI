import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class ConversationState:
    """Manage conversation states for users"""
    
    def __init__(self, state_file: str = "data/conversation_states.json"):
        self.state_file = state_file
        self.states: Dict[int, Dict[str, Any]] = {}
        self.load_states()
    
    def load_states(self):
        """Load conversation states from file"""
        try:
            # Create data directory if it doesn't exist
            os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
            
            if os.path.exists(self.state_file):
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Convert string keys back to integers
                    self.states = {int(k): v for k, v in data.items()}
                    logger.info(f"Loaded {len(self.states)} conversation states")
            else:
                self.states = {}
                logger.info("No existing conversation states found, starting fresh")
                
        except Exception as e:
            logger.error(f"Error loading conversation states: {e}")
            self.states = {}
    
    def save_states(self):
        """Save conversation states to file"""
        try:
            # Create data directory if it doesn't exist
            os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
            
            with open(self.state_file, 'w', encoding='utf-8') as f:
                # Convert integer keys to strings for JSON
                data = {str(k): v for k, v in self.states.items()}
                json.dump(data, f, ensure_ascii=False, indent=2, default=str)
                logger.debug(f"Saved {len(self.states)} conversation states")
                
        except Exception as e:
            logger.error(f"Error saving conversation states: {e}")
    
    def get_user_state(self, user_id: int) -> Dict[str, Any]:
        """Get conversation state for a user"""
        if user_id not in self.states:
            self.states[user_id] = {
                'user_id': user_id,
                'first_seen': datetime.now().isoformat(),
                'last_activity': datetime.now().isoformat(),
                'message_count': 0,
                'topics_discussed': [],
                'mood': 'neutral',
                'conversation_history': []
            }
        
        return self.states[user_id]
    
    def update_user_state(self, user_id: int, state: Dict[str, Any]):
        """Update conversation state for a user"""
        self.states[user_id] = state
        self.save_states()
    
    def reset_user_state(self, user_id: int):
        """Reset conversation state for a user"""
        if user_id in self.states:
            # Keep some basic info but reset conversation
            old_state = self.states[user_id]
            self.states[user_id] = {
                'user_id': user_id,
                'first_seen': old_state.get('first_seen', datetime.now().isoformat()),
                'last_activity': datetime.now().isoformat(),
                'message_count': 0,
                'topics_discussed': [],
                'mood': 'neutral',
                'conversation_history': []
            }
            self.save_states()
            logger.info(f"Reset conversation state for user {user_id}")
    
    def get_active_users_count(self, hours: int = 24) -> int:
        """Get count of users active in the last X hours"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        active_count = 0
        
        for user_id, state in self.states.items():
            try:
                last_activity = datetime.fromisoformat(state.get('last_activity', ''))
                if last_activity > cutoff_time:
                    active_count += 1
            except (ValueError, TypeError):
                continue
        
        return active_count
    
    def get_total_users_count(self) -> int:
        """Get total number of users who have interacted with the bot"""
        return len(self.states)
    
    def get_all_user_ids(self) -> List[int]:
        """Get all user IDs that have interacted with the bot"""
        return list(self.states.keys())
    
    def add_topic_to_user(self, user_id: int, topic: str):
        """Add a topic to user's discussed topics"""
        user_state = self.get_user_state(user_id)
        topics = user_state.get('topics_discussed', [])
        
        if topic not in topics:
            topics.append(topic)
            user_state['topics_discussed'] = topics[-10:]  # Keep last 10 topics
            self.update_user_state(user_id, user_state)
    
    def update_user_mood(self, user_id: int, mood: str):
        """Update user's mood based on conversation"""
        user_state = self.get_user_state(user_id)
        user_state['mood'] = mood
        self.update_user_state(user_id, user_state)
    
    def cleanup_old_states(self, days: int = 30):
        """Remove states for users inactive for more than X days"""
        cutoff_time = datetime.now() - timedelta(days=days)
        users_to_remove = []
        
        for user_id, state in self.states.items():
            try:
                last_activity = datetime.fromisoformat(state.get('last_activity', ''))
                if last_activity < cutoff_time:
                    users_to_remove.append(user_id)
            except (ValueError, TypeError):
                users_to_remove.append(user_id)
        
        for user_id in users_to_remove:
            del self.states[user_id]
        
        if users_to_remove:
            self.save_states()
            logger.info(f"Cleaned up {len(users_to_remove)} old conversation states")
        
        return len(users_to_remove)

# Global instance
conversation_state = ConversationState()
