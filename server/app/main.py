from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import config
from app.routes import router as search_router

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=[config.FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(search_router)

@app.get("/")
async def root():
    return {"message": "Search API is running 🚀"}
