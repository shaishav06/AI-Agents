import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def generate_gemini_response(prompt):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set in the environment variables.")
    
    genai.configure(api_key=api_key)
    response = genai.generate_text(prompt=prompt)
    return response.result
