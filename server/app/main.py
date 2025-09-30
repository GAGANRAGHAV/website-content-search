from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import config
from app.routes import router as search_router

app = FastAPI()

# CORS setup
allowed_origins = [
    config.FRONTEND_ORIGIN,  # From environment variable
    "http://localhost:3000",  # Local development
    "https://website-content-search-three.vercel.app"  # Production deployment
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(search_router)

@app.get("/")
async def root():
    return {"message": "Search API is running 🚀"}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
