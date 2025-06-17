import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

VAPI_ENDPOINT_SESSION = os.getenv("VAPI_ENDPOINT_SESSION")
VAPI_ENDPOINT_CHAT = os.getenv("VAPI_ENDPOINT_CHAT")
VAPI_TOKEN = os.getenv("VAPI_TOKEN")
VAPI_ASSISTANT_ID = os.getenv("VAPI_ASSISTANT_ID")

def create_vapi_session():
    headers = {
        "Authorization": f"Bearer {VAPI_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {"assistantId": VAPI_ASSISTANT_ID}
    response = requests.post(VAPI_ENDPOINT_SESSION, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["id"]

def create_vapi_chat(session_id, user_input):
    headers = {
        "Authorization": f"Bearer {VAPI_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "input": user_input,
        "sessionId": session_id
    }
    response = requests.post(VAPI_ENDPOINT_CHAT, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["output"]

def chat_with_vapi():
    session_id = create_vapi_session()
    print("Chat session started. Type 'exit' to quit.")

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == "exit":
            print("\nGoodbye!")
            break

        try:
            ai_response = create_vapi_chat(session_id, user_input)
            print(f"\nAI: {ai_response}")
        except Exception as e:
            print(f"\nError: {str(e)}")

if __name__ == "__main__":
    chat_with_vapi()