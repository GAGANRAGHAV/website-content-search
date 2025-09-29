from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
import pinecone
import uuid
from transformers import AutoTokenizer
import hashlib
from urllib.parse import urlparse
# import validators

# ---------- CONFIG ----------
PINECONE_API_KEY = "pcsk_3BgdmL_KCyHE9EexXhVUHnUX36B4RnYGbDZigCr3umFAtQzgaJZrfPP13XUTfMe9866NK2"
PINECONE_INDEX_NAME = "smartercodes143"
EMBED_MODEL = "llama-text-embed-v2"  # Hosted by Pinecone
PINECONE_ENV = "gcp-starter"          # check in your Pinecone console

# ---------- INIT ----------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Pinecone
pc = pinecone.Pinecone(api_key=PINECONE_API_KEY)

# Create index if not exists
if PINECONE_INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=PINECONE_INDEX_NAME,
        dimension=1024,
        metric="cosine",
        spec=pinecone.ServerlessSpec(cloud="aws", region="us-east-1")
    )

index = pc.Index(PINECONE_INDEX_NAME)

# Use proper tokenizer
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

# ---------- HELPERS ----------
def clean_html(html: str):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style"]):
        tag.extract()
    return soup.get_text(separator=" ", strip=True)

def chunk_text(text: str, max_tokens: int = 500):
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_tokens):
        chunks.append(" ".join(words[i:i+max_tokens]))
    return chunks

def chunk_text_by_tokens(text: str, max_tokens: int = 500):
    # Tokenize the entire text
    tokens = tokenizer.tokenize(text)
    chunks = []
    
    for i in range(0, len(tokens), max_tokens):
        chunk_tokens = tokens[i:i+max_tokens]
        chunk_text = tokenizer.convert_tokens_to_string(chunk_tokens)
        chunks.append(chunk_text)
    
    return chunks

def embed_texts(texts: list[str]):
    response = pc.inference.embed(
        model=EMBED_MODEL,
        inputs=texts,
        parameters={"input_type": "passage"}
    )
    return [item.values for item in response.data]

def get_url_hash(url: str) -> str:
    return hashlib.md5(url.encode()).hexdigest()

# ---------- API ----------
class SearchRequest(BaseModel):
    url: str
    query: str

@app.post("/search")
async def search(req: SearchRequest):
    # Validate URL
    # if not validators.url(req.url):
    #     return {"error": "Invalid URL format"}
    
    # # Validate query
    # if not req.query.strip():
    #     return {"error": "Query cannot be empty"}
    
    # if len(req.query) > 1000:
    #     return {"error": "Query too long"}
    
    url_hash = get_url_hash(req.url)
    
    # Check if URL is already indexed
    existing = index.query(
        vector=[0]*1024,  # dummy vector
        top_k=1,
        filter={"url_hash": {"$eq": url_hash}}
    )
    
    # Only fetch and index if not already done
    if not existing["matches"]:
        # 1. Fetch website
        try:
            res = requests.get(req.url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            res.raise_for_status()
        except Exception as e:
            return {"error": f"Failed to fetch URL: {str(e)}"}

        text = clean_html(res.text)
        chunks = chunk_text(text, 500)

        # 2. Delete old vectors for this URL (optional)
        index.delete(filter={"url": {"$eq": req.url}})

        # 3. Embed and upsert chunks with URL metadata
        embeddings = embed_texts(chunks)
        vectors = []
        for chunk, emb in zip(chunks, embeddings):
            vec_id = str(uuid.uuid4())
            vectors.append((vec_id, emb, {"text": chunk, "url": req.url}))
        if vectors:
            index.upsert(vectors=vectors)

    # 4. Embed query
    query_emb = embed_texts([req.query])[0]

    # 5. Query Pinecone only for this URL
    search_res = index.query(
        vector=query_emb,
        top_k=10,
        include_metadata=True,
        filter={"url": {"$eq": req.url}}
    )

    # Return more structured results
    return {
        "url": req.url,
        "query": req.query,
        "total_matches": len(search_res["matches"]),
        "results": [
            {
                "content": match["metadata"]["text"],
                "relevance_score": match["score"],
                "chunk_id": match["id"]
            }
            for match in search_res["matches"]
        ]
    }
