from fastapi import APIRouter
from pydantic import BaseModel
import requests
from app.helpers import (
    clean_html, chunk_text, embed_texts,
    get_url_hash, prepare_vectors
)
from app.pinecone_client import index

router = APIRouter()

class SearchRequest(BaseModel):
    url: str
    query: str

@router.post("/search")
async def search(req: SearchRequest):
    url_hash = get_url_hash(req.url)

    # Check if already indexed
    existing = index.query(
        vector=[0]*1024,  # dummy vector
        top_k=1,
        filter={"url_hash": {"$eq": url_hash}}
    )

    # If not indexed, fetch and store
    if not existing["matches"]:
        try:
            res = requests.get(req.url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            res.raise_for_status()
        except Exception as e:
            return {"error": f"Failed to fetch URL: {str(e)}"}

        text = clean_html(res.text)
        chunks = chunk_text(text, 500)

        index.delete(filter={"url": {"$eq": req.url}})  # remove old entries

        embeddings = embed_texts(chunks)
        vectors = prepare_vectors(chunks, embeddings, req.url)
        if vectors:
            index.upsert(vectors=vectors)

    # Search with query
    query_emb = embed_texts([req.query])[0]
    search_res = index.query(
        vector=query_emb,
        top_k=10,
        include_metadata=True,
        filter={"url": {"$eq": req.url}}
    )

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
