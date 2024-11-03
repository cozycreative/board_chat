import requests
import json
from config import OPENROUTER_API_KEY, OPENROUTER_URL, MODEL_CONFIG

def create_system_message(board_members, language, system_prompts):
    """Create a system message based on selected board members and language"""
    members_str = ', '.join(board_members)
    return system_prompts[language].format(members=members_str)

def get_chat_response(messages, board_members, language, system_prompts):
    """Get response from OpenRouter API"""
    try:
        system_message = create_system_message(board_members, language, system_prompts)
        
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8501",  # Required by OpenRouter
            "X-Title": "Board of Directors Chat"      # Required by OpenRouter
        }
        
        # Prepare messages with system message and full chat history
        full_messages = [
            {"role": "system", "content": system_message},
            *messages  # Include entire chat history
        ]
        
        data = {
            "model": MODEL_CONFIG["model"],
            "temperature": MODEL_CONFIG["temperature"],
            "messages": full_messages
        }
        
        response = requests.post(OPENROUTER_URL, headers=headers, json=data)
        response.raise_for_status()
        
        response_data = response.json()
        
        if 'error' in response_data:
            error_details = response_data['error']
            print(f"OpenRouter API Error: {json.dumps(error_details, indent=2)}")
            raise Exception(f"API Error: {error_details.get('message', 'Unknown error')}")
            
        if 'choices' not in response_data:
            print(f"Unexpected API Response: {json.dumps(response_data, indent=2)}")
            raise Exception("API response missing 'choices' field")
            
        return response_data['choices'][0]['message']['content']
        
    except requests.exceptions.RequestException as e:
        print(f"OpenRouter API Request Error: {str(e)}")
        if hasattr(e.response, 'text'):
            print(f"Response content: {e.response.text}")
        error_msg = ("I apologize, but I encountered an error while connecting to the API." if language == "English" 
                    else "Извините, произошла ошибка при подключении к API.")
        return error_msg
        
    except Exception as e:
        print(f"OpenRouter Processing Error: {str(e)}")
        error_msg = ("I apologize, but I encountered an error while processing your request." if language == "English" 
                    else "Извините, произошла ошибка при обработке вашего запроса.")
        return error_msg
