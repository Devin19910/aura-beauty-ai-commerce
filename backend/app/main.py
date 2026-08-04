"""
Aura Beauty AI Commerce - FastAPI Backend
Main application entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.database import init_db, get_db
from app.api import router as api_router
from app.utils.logging import setup_logging

# Setup logging
setup_logging()

# Initialize logger
import logging
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for app startup/shutdown"""
    # Startup
    logger.info("🚀 Starting Aura Beauty AI Commerce Backend")
    await init_db()
    logger.info("✓ Database initialized")

    yield

    # Shutdown
    logger.info("🛑 Shutting down Aura Beauty Backend")


# Create FastAPI app
app = FastAPI(
    title="Aura Beauty AI Commerce API",
    description="Enterprise-grade AI-powered beauty ecommerce platform",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# Add middleware
app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["x-total-count", "x-page", "x-page-size"],
)

# Include routers
app.include_router(api_router, prefix="/api/v1")


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "version": "0.1.0",
    }


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Aura Beauty AI Commerce API",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/sitemap.xml", tags=["SEO"])
async def sitemap():
    """Dynamic sitemap for SEO"""
    # TODO: Implement dynamic sitemap generation from database
    return {
        "message": "Sitemap generation coming soon",
        "status": "In development",
    }


@app.get("/robots.txt", tags=["SEO"])
async def robots():
    """Robots.txt for search engines"""
    return """User-agent: *
Allow: /
Allow: /api/v1/products/
Allow: /api/v1/blog/
Disallow: /admin/
Disallow: /api/v1/admin/
Disallow: /api/v1/agents/
Sitemap: https://aurabeauty.com/sitemap.xml"""


@app.get("/rss.xml", tags=["SEO"])
async def rss_feed():
    """RSS feed for blog posts"""
    # TODO: Implement RSS feed generation
    return {
        "message": "RSS feed generation coming soon",
        "status": "In development",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info",
    )
