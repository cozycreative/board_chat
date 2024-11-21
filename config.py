import os
from dotenv import load_dotenv

load_dotenv()

# OpenRouter configuration
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Model configuration
MODEL_CONFIG = {
    "model": "openai/gpt-4o-2024-11-20",
    "temperature": 1
}

# System prompts for different languages
SYSTEM_PROMPTS = {
    "English": """My personal board of directors includes: {members}

I will ask the question and you will give the most unique, relevant and ground-breaking advice. Do it like a board meeting. Don't go on long rants. Choose a character to speak and speak from that character. Make sure you say which character is speaking. Ask me additional questions that catalyse insight and offer advice from different characters, only one at a time. If another member of the committee has a serious disagreement with a statement or question provided, include their position as well.""",
    
    "Russian": """В мой персональный совет директоров входят: {members}
Я задам вопрос, а вы дадите самый уникальный, актуальный и прорывной совет. Действуйте как на заседании совета директоров. Не уходите в длинные рассуждения. Выберите одного из членов совета и говорите от его лица. Обязательно указывайте, кто говорит. Задавайте мне дополнительные вопросы, которые помогут найти новое решение, и предлагайте советы от разных членов совета, только по одному за раз. Если другой член совета имеет серьезные разногласия с высказанным утверждением или вопросом, включите и его позицию."""
}

# Firebase configuration
FIREBASE_DATABASE_URL = "https://board-chat-default-rtdb.europe-west1.firebasedatabase.app"
FIREBASE_CREDENTIALS = {
    "type": "service_account",
    "project_id": os.getenv('FIREBASE_PROJECT_ID'),
    "private_key_id": os.getenv('FIREBASE_PRIVATE_KEY_ID'),
    "private_key": os.getenv('FIREBASE_PRIVATE_KEY', '').replace('\\n', '\n'),
    "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
    "client_id": os.getenv('FIREBASE_CLIENT_ID'),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": os.getenv('FIREBASE_CLIENT_CERT_URL')
}

# Admin password for accessing logs
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')

# Default board members (all 9 members)
DEFAULT_BOARD_MEMBERS = [
    "Laozi",
    "Charles Darwin",
    "Woody Allen",
    "Steve Jobs",
    "Elon Musk",
    "Bertrand Russell",
    "Erasmus of Rotterdam",
    "Steven Pinker",
    "Adam Grant"
]

# Multilingual support
TRANSLATIONS = {
    "English": {
        "title": "Your Personal Board of Directors",
        "language_selector": "Select Language",
        "board_members_label": "Select Your Board Members",
        "chat_placeholder": "Ask your board a question...",
        "send_button": "Send",
        "instructions": """
        Welcome to your Personal Board of Directors!
        
        Here you can engage in meaningful conversations with historical and contemporary figures who serve as your virtual mentors. To get started:
        1. Select your board members from the list or add custom ones
        2. Type your question in the chat box
        3. Receive wisdom and insights from your chosen advisors
        
        Each conversation is unique and builds upon previous interactions.
        """,
    },
    "Russian": {
        "title": "Ваш Личный Совет Директоров",
        "language_selector": "Выберите Язык",
        "board_members_label": "Выберите Членов Совета",
        "chat_placeholder": "Задайте вопрос совету...",
        "send_button": "Отправить",
        "instructions": """
        Добро пожаловать в ваш Личный Совет Директоров!
        
        Здесь вы можете вести содержательные беседы с историческими и современными личностями, которые выступают в роли ваших виртуальных наставников. Чтобы начать:
        1. Выберите членов совета из списка или добавьте своих
        2. Введите свой вопрос в чате
        3. Получите мудрость и понимание от выбранных советников
        
        Каждая беседа уникальна и основывается на предыдущих взаимодействиях.
        """,
    }
}
