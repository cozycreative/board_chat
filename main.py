import streamlit as st
import json
from config import DEFAULT_BOARD_MEMBERS, TRANSLATIONS, ADMIN_PASSWORD, SYSTEM_PROMPTS
from firebase_utils import (
    initialize_firebase, log_conversation, get_conversation_logs, generate_user_id,
    get_config, update_board_members, update_system_prompts, update_translations,
    initialize_config
)
from openrouter_utils import get_chat_response

# Initialize Firebase
db = initialize_firebase()
if db:
    initialize_config(db)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'user_id' not in st.session_state:
    st.session_state.user_id = generate_user_id()
if 'language' not in st.session_state:
    st.session_state.language = "English"
if 'custom_members' not in st.session_state:
    st.session_state.custom_members = []

def main():
    # Get dynamic configurations
    config = get_config(db) if db else {
        'board_members': DEFAULT_BOARD_MEMBERS,
        'system_prompts': SYSTEM_PROMPTS,
        'translations': TRANSLATIONS
    }
    
    # Check URL parameters
    params = dict(st.query_params)
    is_admin = params.get("admin") == "true"
    is_anonymous = params.get("anon") == "true"
    
    # Show admin panel if requested
    if is_admin:
        show_admin_panel(config)
        return
        
    # Language selection in upper right corner
    col1, col2, col3 = st.columns([6, 1, 1])
    with col2:
        if st.button("EN", type="secondary", use_container_width=True):
            st.session_state.language = "English"
            st.rerun()
    with col3:
        if st.button("RU", type="secondary", use_container_width=True):
            st.session_state.language = "Russian"
            st.rerun()
            
    language = st.session_state.language
    translations = config['translations'][language]
    
    st.title(translations["title"])
    
    # Show anonymous mode indicator if active
    if is_anonymous:
        st.info(
            "Anonymous Mode - Chat history will not be stored" if language == "English"
            else "Анонимный режим - История чата не будет сохранена"
        )
    
    st.write(translations["instructions"])
    
    # Board member selection
    all_members = config['board_members'] + st.session_state.custom_members
    selected_members = st.multiselect(
        translations["board_members_label"],
        options=all_members,
        default=all_members  # Show all members by default
    )
    
    # Add custom board member (aligned input and button)
    with st.container():
        col1, col2 = st.columns([4, 1])
        with col1:
            new_member = st.text_input(
                "Add Custom Member" if language == "English" else "Добавить Участника",
                key="new_member",
                label_visibility="collapsed"  # Hide label to align with button
            )
        with col2:
            add_clicked = st.button(
                "Add" if language == "English" else "Добавить",
                type="secondary",
                use_container_width=True
            )
            if add_clicked:
                if new_member and new_member not in all_members and len(all_members) < 12:
                    st.session_state.custom_members.append(new_member)
                    st.rerun()
                elif len(all_members) >= 12:
                    st.warning(
                        "Maximum 12 board members allowed." if language == "English"
                        else "Максимально допустимо 12 участников совета."
                    )
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if selected_members:
        user_input = st.chat_input(translations["chat_placeholder"])
        
        if user_input:
            # Add user message to chat immediately
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Show the user's message
            with st.chat_message("user"):
                st.write(user_input)
            
            # Show loading spinner while getting response
            with st.spinner('Getting response...' if language == "English" else 'Получение ответа...'):
                # Get AI response using dynamic system prompts
                response = get_chat_response(
                    st.session_state.messages,
                    selected_members,
                    language,
                    config['system_prompts']
                )
            
            # Add AI response to chat
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Show AI response
            with st.chat_message("assistant"):
                st.write(response)
            
            # Log conversation to Firebase only if not in anonymous mode
            if db and not is_anonymous:
                log_conversation(
                    db,
                    st.session_state.user_id,
                    st.session_state.messages,
                    selected_members,
                    language
                )
            
            # Rerun to update chat display
            st.rerun()
    else:
        st.warning(
            "Please select at least one board member to begin." if language == "English"
            else "Пожалуйста, выберите хотя бы одного члена совета, чтобы начать."
        )
    
    # Clear chat button (below chat)
    if st.button("New Chat" if language == "English" else "Новый Чат", type="secondary"):
        # Generate new user_id for the new chat session
        st.session_state.user_id = generate_user_id()
        # Clear only the local messages
        st.session_state.messages = []
        st.rerun()

def show_admin_panel(config):
    """Display enhanced admin panel with configuration management"""
    st.title("Admin Panel")
    
    password = st.text_input("Password", type="password")
    if password != ADMIN_PASSWORD:
        st.error("Invalid password")
        return
    
    # Create tabs for different admin functions
    chat_tab, board_tab, prompts_tab, translations_tab = st.tabs([
        "Chat Logs", "Board Members", "System Prompts", "Interface Text"
    ])
    
    # Chat Logs Tab
    with chat_tab:
        st.header("Conversation Logs")
        if db:
            logs = get_conversation_logs(db)
            for log in logs:
                with st.expander(f"Conversation {log['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}"):
                    st.write(f"User ID: {log['user_id']}")
                    st.write(f"Language: {log['language']}")
                    st.write(f"Board Members: {', '.join(log['board_members'])}")
                    for msg in log['messages']:
                        st.write(f"{msg['role'].title()}: {msg['content']}")
    
    # Board Members Tab
    with board_tab:
        st.header("Default Board Members")
        board_members = config.get('board_members', DEFAULT_BOARD_MEMBERS)
        
        # Display current members with delete buttons
        for i, member in enumerate(board_members):
            col1, col2 = st.columns([5, 1])
            with col1:
                st.text(member)
            with col2:
                if st.button("Delete", key=f"del_{i}"):
                    board_members.pop(i)
                    if db:
                        update_board_members(db, board_members)
                    st.rerun()
        
        # Add new member
        new_member = st.text_input("Add New Board Member")
        if st.button("Add Member"):
            if new_member and new_member not in board_members:
                board_members.append(new_member)
                if db:
                    update_board_members(db, board_members)
                st.rerun()
    
    # System Prompts Tab
    with prompts_tab:
        st.header("System Prompts")
        system_prompts = config.get('system_prompts', SYSTEM_PROMPTS)
        
        # Edit prompts for both languages
        en_prompt = st.text_area(
            "English System Prompt",
            value=system_prompts["English"],
            height=200
        )
        ru_prompt = st.text_area(
            "Russian System Prompt",
            value=system_prompts["Russian"],
            height=200
        )
        
        if st.button("Update Prompts"):
            new_prompts = {
                "English": en_prompt,
                "Russian": ru_prompt
            }
            if db:
                update_system_prompts(db, new_prompts)
            st.success("System prompts updated successfully!")
    
    # Interface Translations Tab
    with translations_tab:
        st.header("Interface Translations")
        translations = config.get('translations', TRANSLATIONS)
        
        # Create sections for each language
        for lang in ["English", "Russian"]:
            st.subheader(f"{lang} Interface Text")
            lang_translations = translations[lang]
            
            # Create input fields for each translation key
            new_translations = {}
            for key, value in lang_translations.items():
                if key == "instructions":
                    new_translations[key] = st.text_area(
                        f"{key}",
                        value=value,
                        height=200,
                        key=f"{lang}_{key}"
                    )
                else:
                    new_translations[key] = st.text_input(
                        f"{key}",
                        value=value,
                        key=f"{lang}_{key}"
                    )
            
            translations[lang] = new_translations
        
        if st.button("Update Translations"):
            if db:
                update_translations(db, translations)
            st.success("Interface translations updated successfully!")

if __name__ == "__main__":
    main()
