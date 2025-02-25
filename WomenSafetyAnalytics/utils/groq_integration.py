import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def analyze_text_with_groq(text):
    """Analyze text input using Groq's LLM."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set in the environment variables.")
    
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": text}],
        model="llama3-8b-8192",
    )
    return response.choices[0].message.content
