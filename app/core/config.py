from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "FileConversion API"
    PROJECT_DESCRIPTION: str = "A comprehensive API for converting various file formats"
    VERSION: str = "1.0.0"
    
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8080
    
    # CORS settings
    ALLOWED_ORIGINS: List[str] = ["*"]
    
    # File upload settings
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: List[str] = [".md", ".txt", ".docx", ".pdf", ".html"]
    
    # PDF settings
    PDF_MARGIN: int = 30  # mm
    PDF_FONT_SIZE_NORMAL: int = 16
    PDF_FONT_SIZE_HEADER: int = 32
    
    class Config:
        env_file = ".env"

settings = Settings()
