import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# RAG settings
TOP_K = 8                        # Number of similar examples to retrieve
MAX_OUTPUT_TOKENS = 500          # Enough for thinking + short reply
CONVERSATION_HISTORY_LENGTH = 6  # Number of recent turns to keep in context