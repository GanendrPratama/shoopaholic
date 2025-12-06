import requests
from .config import KOLOSAI_API_KEY

def call_kolosal_api(context_text: str, user_question: str) -> str:
    """
    Sends the context and question to Kolosal AI via direct HTTP request.
    """
    url = "https://api.kolosal.ai/v1/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {KOLOSAI_API_KEY}"
    }
    
    system_prompt = (
        "You are a helpful shop assistant. "
        "Answer the user's question using ONLY the context provided below. "
        "If the information is not in the context, say you don't know."
    )
    
    user_message = f"Context Data:\n{context_text}\n\nQuestion:\n{user_question}"

    payload = {
        "model": "Llama 4 Maverick",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status() # Raises error for 4xx/5xx status codes
        return response.json()['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        # If the API call fails, return the error message so we can debug
        raise Exception(f"Kolosal API Error: {str(e)} - Response: {response.text}")