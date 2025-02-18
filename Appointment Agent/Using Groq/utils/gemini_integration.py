import os
import google.generativeai as genai
from google.generativeai import types
from dotenv import load_dotenv

load_dotenv()

def generate_gemini_content(prompt):
    """Generate content using the Gemini API."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set in the environment variables.")
    
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=prompt
    )
    return response.result
