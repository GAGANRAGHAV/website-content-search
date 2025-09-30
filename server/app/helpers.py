from bs4 import BeautifulSoup
from transformers import AutoTokenizer
import hashlib
import uuid
from app import config
from app.pinecone_client import pc

# Use tokenizer
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

def clean_html(html: str):
    """Remove scripts/styles and return plain text."""
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style"]):
        tag.extract()
    return soup.get_text(separator=" ", strip=True)

def chunk_text(text: str, max_tokens: int = 500):
    """Chunk text by words (simple fallback)."""
    words = text.split()
    return [" ".join(words[i:i+max_tokens]) for i in range(0, len(words), max_tokens)]

def chunk_text_by_tokens(text: str, max_tokens: int = 500):
    """Chunk text using tokenizer for better accuracy."""
    tokens = tokenizer.tokenize(text)
    chunks = []
    for i in range(0, len(tokens), max_tokens):
        chunk_tokens = tokens[i:i+max_tokens]
        chunks.append(tokenizer.convert_tokens_to_string(chunk_tokens))
    return chunks

def embed_texts(texts: list[str]):
    """Call Pinecone inference API to embed texts."""
    response = pc.inference.embed(
        model=config.EMBED_MODEL,
        inputs=texts,
        parameters={"input_type": "passage"}
    )
    return [item.values for item in response.data]

def get_url_hash(url: str) -> str:
    """Return MD5 hash of a URL."""
    return hashlib.md5(url.encode()).hexdigest()

def prepare_vectors(chunks: list[str], embeddings: list[list[float]], url: str):
    """Prepare vectors for Pinecone upsert."""
    return [
        (str(uuid.uuid4()), emb, {"text": chunk, "url": url})
        for chunk, emb in zip(chunks, embeddings)
    ]
