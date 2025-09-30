
import pinecone
from app import config

# Initialize Pinecone client
pc = pinecone.Pinecone(api_key=config.PINECONE_API_KEY)

# Ensure index exists
if config.PINECONE_INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=config.PINECONE_INDEX_NAME,
        dimension=1024,
        metric="cosine",
        spec=pinecone.ServerlessSpec(cloud="aws", region="us-east-1")
    )

index = pc.Index(config.PINECONE_INDEX_NAME)
