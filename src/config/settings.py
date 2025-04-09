import os
from dotenv import load_dotenv

load_dotenv()

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

PDF_DIRECTORY = "files"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100
VECTOR_DB_PATH = "./chroma_db"

DEFAULT_MODEL = "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8"

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

APP_TITLE = "🤖 Llama-4-Maverick Chatbot"
APP_ICON = "🤖"
DEFAULT_SEARCH_RESULTS = 3
MAX_SEARCH_RESULTS = 10 