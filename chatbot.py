import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the Azure OpenAI client
client = openai.AzureOpenAI(
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_KEY"),
)

conversation_history = []

def chat_with_ai():
    global conversation_history
    
    while True:
        user_input = input("\nYou: ")  # Get input from terminal
        if user_input.lower() == "exit":
            print("\nGoodbye!")
            break  # Exit the loop if user types 'exit'

        conversation_history.append({"role": "user", "content": user_input})

        # Define prompt for AI
        messages = [
            {"role": "system", "content": "You are a helpful AI assistant. Remember past user questions and your previous responses."},
            *conversation_history,  # Include conversation history
            {"role": "user", "content": user_input}
        ]

        try:
            # Call OpenAI API
            response = client.chat.completions.create(
                messages=messages,
                max_completion_tokens=500,
                temperature=0.7,
                top_p=1.0,
                model=os.getenv("AZURE_DEPLOYMENT_NAME"),
            )

            ai_response = response.choices[0].message.content.strip()
            conversation_history.append({"role": "assistant", "content": ai_response})
            
            print(f"\nAI: {ai_response}")  # Print response in terminal

            if len(conversation_history) > 50:
                conversation_history = conversation_history[-50:]  

        except Exception as e:
            print(f"\nError: {str(e)}")

# Start chatbot in terminal
if __name__ == "__main__":
    chat_with_ai()