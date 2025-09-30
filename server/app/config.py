import os
from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "smartercodes143")
EMBED_MODEL = os.getenv("EMBED_MODEL", "llama-text-embed-v2")
PINECONE_ENV = os.getenv("PINECONE_ENV", "gcp-starter")
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")
