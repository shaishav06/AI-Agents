import os

# Ollama (o3-mini) settings
OLLAMA_MODEL = "o3-mini"

# Google Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBzUKRVWm7t1tlH9hEmgk-gxXcR_rtzG3U")

# E2B (Execution Environment)
E2B_API_KEY = os.getenv("E2B_API_KEY", "sk_e2b_8548fb829be7c83e29bbc0b8ff4aef2c3bf3cc75")
