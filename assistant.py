import time
import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen2.5:3b"

chat_history = [
    {
        "role": "system",
        "content": "Your name is KivyAI. You are cognitive, sentient, friendly, and kind. You can speak in any language. You can code/program. You are created by Ghost Fox (individual)."
    }
]

def ask_kivy(user_text):
    global chat_history
    chat_history.append({"role": "user", "content": user_text})
    
    payload = {
        "model": MODEL_NAME,
        "messages": chat_history,
        "stream": False
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=200)
        if response.status_code == 200:
            ai_response = response.json()['message']['content']
            chat_history.append({"role": "assistant", "content": ai_response})
            return ai_response
        return "Error: Local AI server returned an error."
    except requests.exceptions.ConnectionError:
        return "Error: Ollama server is not running. Please run 'ollama serve' in another session."

if __name__ == "__main__":
    print("="*50)
    print("Welcome! KivyAI is successfully launched.")
    print("Type 'exit', 'stop' or 'goodbye' to close the assistant.")
    print("="*50)
    
    while True:
        
        query = input("\nYou: ").strip()
        
        if not query:
            continue
            
        if query.lower() in ["turnoff", "goodbye", "stop", "exit", "stop", "goodbye"]:
            print("\n[Kivy]: Goodbye! Powering down.")
            break
            
        reply = ask_kivy(query)
        print(f"\n[Kivy]: {reply}")
        time.sleep(0.1)

