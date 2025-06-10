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

def chat_with_ai():
    while True:
        user_input = input("\nYou: ")  # Get input from terminal
        if user_input.lower() == "exit":
            print("\nGoodbye!")
            break  # Exit the loop if user types 'exit'

        # Define prompt for AI
        messages = [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": user_input},
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
            print(f"\nAI: {ai_response}")  # Print response in terminal

        except Exception as e:
            print(f"\nError: {str(e)}")

# Start chatbot in terminal
if __name__ == "__main__":
    chat_with_ai()