# =========================================================
# File: main.py
# Purpose:
# The entry point for the FastAPI application.
#
# Responsibilities:
# - Initialize FastAPI application instance
# - Configure CORS (Cross-Origin Resource Sharing)
# - Connect and create database tables
# - Register and include all API routers
#
# Depends on:
# - FastAPI framework
# - Database engine (app.db.database)
# - All API routers (app.api.*)
#
# Used by:
# - Uvicorn or other ASGI servers to run the app
# =========================================================

# Navigation
# [1] Standard Library & Third-party Imports
# [2] API Routers
# [3] Database & Models
# [4] App Initialization
# [5] CORS Configuration
# [6] Router Inclusion
# [7] Root Endpoint

# =====================================================
# [1] Standard Library & Third-party Imports
# =====================================================
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
    docs_url=None,
    redoc_url=None,
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

# =====================================================
# [7] Root Endpoint
# =====================================================
@app.get("/")
def home():
    """
    ---------------------------------------------------------
    Function:
    home()

    Purpose:
    Provides a simple health check and welcome message for the API.

    Parameters:
    None

    Returns:
    dict: A welcome message JSON object.

    Raises:
    None

    Side Effects:
    None
    ---------------------------------------------------------
    """
    return {
        "message": "Welcome to BookNest API"
    }