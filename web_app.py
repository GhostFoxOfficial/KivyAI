import json
import requests
import gradio as gr

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen2.5:3b"

def predict(message, history):
    
    formatted_messages = [
        {
            "role": "system",
            "content": "Your name is KivyAI. You are cognitive, sentient, friendly, and kind. You can speak in any language. You can code/program. You are created by Ghost Fox (individual)."
        }
    ]
    
    
    for chat_turn in history:
        if isinstance(chat_turn, dict):
            
            role = chat_turn.get("role")
            content = chat_turn.get("text", "")
            if role in ["user", "assistant"] and content:
                formatted_messages.append({"role": role, "content": content})
        elif isinstance(chat_turn, (list, tuple)) and len(chat_turn) == 2:
            
            if chat_turn[0]:
                formatted_messages.append({"role": "user", "content": chat_turn[0]})
            if chat_turn[1]:
                formatted_messages.append({"role": "assistant", "content": chat_turn[1]})
        
    
    formatted_messages.append({"role": "user", "content": message})

    payload = {
        "model": MODEL_NAME,
        "messages": formatted_messages,
        "stream": True
    }
    
    try:
        
        response = requests.post(OLLAMA_URL, json=payload, timeout=200, stream=True)
        
        if response.status_code == 200:
            partial_text = ""
            
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line.decode('utf-8'))
                    if 'message' in chunk and 'content' in chunk['message']:
                        partial_text += chunk['message']['content']
                        yield partial_text
        else:
            yield "Error: AI server returned an error."
            
    except requests.exceptions.Timeout:
        yield "Error: Kivy is taking too long to think. Your device's CPU needs a break or try a shorter prompt."
    except requests.exceptions.ConnectionError:
        yield "Error: Ollama server is offline. Run 'ollama serve' in Termux, Linux, or WSL."


demo = gr.ChatInterface(
    predict, 
    title="KivyAI", 
    description="Your fully AI."
)

if __name__ == "__main__":
    
    demo.launch(server_name="127.0.0.1", server_port=7860, share=True)

