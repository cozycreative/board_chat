import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime
import uuid
from config import FIREBASE_CREDENTIALS, FIREBASE_DATABASE_URL, DEFAULT_BOARD_MEMBERS, SYSTEM_PROMPTS, TRANSLATIONS

def initialize_firebase():
    """Initialize Firebase Realtime Database connection"""
    try:
        # Check if default app exists
        if firebase_admin._apps:
            # Get the default app instance
            default_app = firebase_admin.get_app()
            # Delete it
            firebase_admin.delete_app(default_app)
            
        # Initialize new app
        cred = credentials.Certificate(FIREBASE_CREDENTIALS)
        firebase_admin.initialize_app(cred, {
            'databaseURL': FIREBASE_DATABASE_URL
        })
        return db.reference()
    except Exception as e:
        print(f"Firebase initialization error: {str(e)}")
        return None

def log_conversation(ref, user_id, messages, board_members, language):
    """Log a conversation entry to Firebase Realtime Database"""
    if not ref:
        return
    
    try:
        # Store entire chat history under user's ID
        chat_ref = ref.child('chats').child(user_id)
        
        chat_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'messages': [{'role': msg['role'], 'content': msg['content']} for msg in messages],
            'board_members': board_members,
            'language': language
        }
        
        # Update the user's chat entry (overwrite with latest)
        chat_ref.set(chat_data)
        
    except Exception as e:
        print(f"Error logging conversation: {str(e)}")

def get_conversation_logs(ref):
    """Retrieve all conversation logs for admin viewing"""
    if not ref:
        return []
    
    try:
        # Get all chats
        chats = ref.child('chats').get()
        
        if not chats:
            return []
        
        # Format logs for display
        all_logs = []
        for user_id, chat_data in chats.items():
            try:
                # Handle potential missing or malformed data
                timestamp = chat_data.get('timestamp', datetime.utcnow().isoformat())
                messages = chat_data.get('messages', [])
                board_members = chat_data.get('board_members', [])
                language = chat_data.get('language', 'English')
                
                log = {
                    'user_id': user_id,
                    'timestamp': datetime.fromisoformat(timestamp),
                    'messages': messages,
                    'board_members': board_members,
                    'language': language
                }
                all_logs.append(log)
            except Exception as e:
                print(f"Error processing chat log for user {user_id}: {str(e)}")
                continue
        
        # Sort by timestamp, newest first
        all_logs.sort(key=lambda x: x['timestamp'], reverse=True)
        return all_logs[:100]  # Return last 100 conversations
        
    except Exception as e:
        print(f"Error retrieving logs: {str(e)}")
        return []

def generate_user_id():
    """Generate a unique user ID for anonymous tracking"""
    return str(uuid.uuid4())

# New configuration management functions

def initialize_config(ref):
    """Initialize configuration in Firebase if it doesn't exist"""
    if not ref:
        return
    
    try:
        config_ref = ref.child('config')
        current_config = config_ref.get()
        
        if not current_config:
            default_config = {
                'board_members': DEFAULT_BOARD_MEMBERS,
                'system_prompts': SYSTEM_PROMPTS,
                'translations': TRANSLATIONS
            }
            config_ref.set(default_config)
    except Exception as e:
        print(f"Error initializing config: {str(e)}")

def get_config(ref):
    """Retrieve current configuration from Firebase"""
    if not ref:
        return None
    
    try:
        config_ref = ref.child('config')
        config = config_ref.get()
        
        if not config:
            initialize_config(ref)
            config = config_ref.get()
            
        return config
    except Exception as e:
        print(f"Error retrieving config: {str(e)}")
        return None

def update_board_members(ref, members):
    """Update default board members"""
    if not ref:
        return False
    
    try:
        config_ref = ref.child('config')
        config_ref.update({'board_members': members})
        return True
    except Exception as e:
        print(f"Error updating board members: {str(e)}")
        return False

def update_system_prompts(ref, prompts):
    """Update system prompts for both languages"""
    if not ref:
        return False
    
    try:
        config_ref = ref.child('config')
        config_ref.update({'system_prompts': prompts})
        return True
    except Exception as e:
        print(f"Error updating system prompts: {str(e)}")
        return False

def update_translations(ref, translations):
    """Update interface translations"""
    if not ref:
        return False
    
    try:
        config_ref = ref.child('config')
        config_ref.update({'translations': translations})
        return True
    except Exception as e:
        print(f"Error updating translations: {str(e)}")
        return False
