from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

# Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# API key used to protect our endpoint
API_KEY = os.getenv("API_KEY")

# Validation
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing in .env")

if not API_KEY:
    raise ValueError("API_KEY is missing in .env")