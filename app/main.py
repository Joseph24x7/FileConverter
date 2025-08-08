from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import health, markdown_converter
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(markdown_converter.router, prefix="/api/v1", tags=["converters"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "FileConversion API",
        "version": settings.VERSION,
        "status": "running"
    }
