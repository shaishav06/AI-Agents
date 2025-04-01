import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")
FIRECRAWL_BASE_URL = os.getenv("FIRECRAWL_BASE_URL")
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
OLLAMA_PATH = os.getenv("OLLAMA_PATH")
OLLAMA_URL = os.getenv("OLLAMA_URL")
OLLAMA_ORIGINS = os.getenv("OLLAMA_ORIGINS")
MODEL_NAME = os.getenv("MODEL_NAME")
