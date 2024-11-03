# Board of Directors Chat App

## Overview
A Streamlit-based application that enables users to engage in conversations with a virtual "board of directors" composed of historical and contemporary figures. The app uses OpenRouter API for AI responses and Firebase Realtime Database for chat storage.

## Project Structure

```
board_chat/
├── main.py              # Main Streamlit application
├── config.py            # Configuration and constants
├── firebase_utils.py    # Firebase database utilities
├── openrouter_utils.py  # OpenRouter API integration
└── .env                 # Environment variables (not in repo)
```

## Key Features

### 1. Board Member Selection
- Default board includes 9 members: Laozi, Charles Darwin, Woody Allen, Steve Jobs, Elon Musk, Bertrand Russell, Erasmus of Rotterdam, Steven Pinker, and Adam Grant
- Users can add custom board members (up to 12 total)
- All members are shown by default but can be deselected

### 2. Multilingual Support
- English and Russian interfaces
- Language toggle in upper right corner
- Separate system prompts for each language
- All UI elements and messages are translated

### 3. Chat Interface
- Continuous chat history within session
- Real-time message display
- Loading spinner during AI response
- "New Chat" button to start fresh conversation
- Each new chat generates new user_id while preserving old chats

### 4. Admin Panel
- Accessible via `?admin=true` URL parameter
- Password protected
- Shows all chat histories
- Displays user IDs, timestamps, languages, and full conversations

### 5. Data Storage
- Firebase Realtime Database integration
- Anonymous user tracking with UUID
- Complete chat history stored per user
- Preserves chat history when starting new conversations

## Technical Implementation

### Firebase Integration
- Uses Realtime Database (not Firestore)
- Data structure:
```json
{
  "chats": {
    "user_id": {
      "timestamp": "ISO datetime",
      "messages": [
        {"role": "user/assistant", "content": "message"}
      ],
      "board_members": ["member1", "member2"],
      "language": "English/Russian"
    }
  }
}
```

### OpenRouter Integration
- Uses GPT-4 model via OpenRouter API
- Maintains conversation context
- Custom system prompts per language
- Sends full chat history for context

### Session Management
- Uses Streamlit session state for:
  * Messages history
  * User ID
  * Language preference
  * Custom board members
- Generates new user ID for each chat session

## Configuration

### Environment Variables (.env)
```
OPENROUTER_API_KEY=your_api_key
FIREBASE_DATABASE_URL=your_database_url
FIREBASE_PROJECT_ID=your_project_id
FIREBASE_PRIVATE_KEY_ID=your_key_id
FIREBASE_PRIVATE_KEY=your_private_key
FIREBASE_CLIENT_EMAIL=your_client_email
FIREBASE_CLIENT_ID=your_client_id
FIREBASE_CLIENT_CERT_URL=your_cert_url
ADMIN_PASSWORD=your_admin_password
```

### Model Configuration
- Model: openai/gpt-4-0125-preview
- Temperature: 0.7
- Configured in config.py

## Usage

1. Start the app:
```bash
streamlit run board_chat/main.py
```

2. Regular use:
- Select/deselect board members
- Type questions in chat
- Start new chat sessions as needed
- Switch languages via EN/RU buttons

3. Admin access:
- Visit: http://localhost:8501/?admin=true
- Enter admin password
- View all chat histories

## Development Notes

- Firebase initialization is handled carefully to prevent multiple instances
- Chat histories are preserved across new chat sessions
- Admin panel uses secure password verification
- Language switching maintains chat state
- Board member limit enforced (max 12)
- Custom members persist in session state
