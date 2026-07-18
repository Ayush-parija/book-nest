from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routers
from app.api.auth import router as auth_router
from app.api.user import router as users_router
from app.api.book import router as book_router
from app.api.lending import router as lending_router
from app.api.shelf import router as shelf_router
from app.api.shelf_share import router as shelf_share_router
from app.api.stats import router as stats_router
from app.api.dashboard import router as dashboard_router
from app.api.activity import router as activity_router
from app.api.websocket import router as websocket_router

# Database
from app.db.database import Base, engine

# Models
from app.models.user import User
from app.models.book import Book
from app.models.shelf import Shelf
from app.models.shelf_share import ShelfShare
from app.models.lending import Lending
from app.models.activity import Activity

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="BookNest API",
    version="1.0.0",
    description="BookNest Backend API",
)

# =========================
# CORS Configuration
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Include Routers
# =========================
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(book_router)
app.include_router(lending_router)
app.include_router(shelf_router)
app.include_router(shelf_share_router)
app.include_router(stats_router)
app.include_router(dashboard_router)
app.include_router(activity_router)
app.include_router(websocket_router)

# =========================
# Root Endpoint
# =========================
@app.get("/")
def home():
    return {
        "message": "Welcome to BookNest API"
    }