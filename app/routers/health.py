from fastapi import APIRouter
from app.core.config import settings

router = APIRouter()

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Service is running",
        "version": settings.VERSION
    }

@router.get("/status")
async def status():
    """Detailed status endpoint"""
    return {
        "status": "running",
        "version": settings.VERSION,
        "project_name": settings.PROJECT_NAME,
        "description": settings.PROJECT_DESCRIPTION
    }
