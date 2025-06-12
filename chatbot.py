import openai
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
import json
import logging
import fitz  

# Load environment variables
load_dotenv()

# Initialize the Azure OpenAI client
client = openai.AzureOpenAI(
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_KEY"),
)

conversation_history = []

# Extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

pdf_text = extract_text_from_pdf(r"C:\Users\isabe\Downloads\Gildan Heavy Cotton T-Shirt.html")

def chat_with_ai():
    global conversation_history

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == "exit":
            print("\nGoodbye!")
            break

        conversation_history.append({"role": "user", "content": user_input})

        messages = [
            {"role": "system", "content": "You are a highly knowledgeable assistant with access to the full text of the uploaded PDF."},
            {"role": "system", "content": f"Here is the PDF content for reference:\n{pdf_text}"},
            *conversation_history,
            {"role": "user", "content": user_input}
        ]

        try:
            response = client.chat.completions.create(
                messages=messages,
                max_completion_tokens=500,
                temperature=0.7,
                top_p=1.0,
                model=os.getenv("AZURE_DEPLOYMENT_NAME"),
            )

            ai_response = response.choices[0].message.content.strip()
            conversation_history.append({"role": "assistant", "content": ai_response})

            print(f"\nAI: {ai_response}")

            if len(conversation_history) > 50:
                conversation_history = conversation_history[-50:]

        except Exception as e:
            print(f"\nError: {str(e)}")

# Start chatbot in terminal
if __name__ == "__main__":
    chat_with_ai()