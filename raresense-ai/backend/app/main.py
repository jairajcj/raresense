"""
RareSense.AI — FastAPI Application
LLM-Powered Rare Disease Detection from Unstructured Clinical Notes
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import connect_to_mongo, close_mongo_connection
from app.routes import auth, patients, diseases, analytics, search, matching


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    await connect_to_mongo()
    yield
    await close_mongo_connection()


app = FastAPI(
    title="RareSense.AI",
    description="LLM-Powered Rare Disease Detection from Unstructured Clinical Notes",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(auth.router)
app.include_router(patients.router)
app.include_router(diseases.router)
app.include_router(analytics.router)
app.include_router(search.router)
app.include_router(matching.router)


@app.get("/")
async def root():
    return {
        "name": "RareSense.AI",
        "version": "1.0.0",
        "description": "LLM-Powered Rare Disease Detection from Unstructured Clinical Notes",
        "docs": "/docs",
        "status": "running"
    }


@app.get("/api/health")
async def health_check():
    from app.config import mongo
    try:
        await mongo.client.admin.command("ping")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)}
