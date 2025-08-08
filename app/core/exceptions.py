from fastapi import HTTPException
from typing import Optional

class FileConversionError(HTTPException):
    """Base exception for file conversion errors"""
    def __init__(self, detail: str, status_code: int = 500):
        super().__init__(status_code=status_code, detail=detail)

class UnsupportedFileTypeError(FileConversionError):
    """Raised when file type is not supported"""
    def __init__(self, file_type: str):
        super().__init__(
            detail=f"File type '{file_type}' is not supported",
            status_code=400
        )

class FileTooLargeError(FileConversionError):
    """Raised when file is too large"""
    def __init__(self, max_size: int):
        super().__init__(
            detail=f"File too large. Maximum size is {max_size} bytes",
            status_code=413
        )

class ConversionFailedError(FileConversionError):
    """Raised when file conversion fails"""
    def __init__(self, error: str):
        super().__init__(
            detail=f"Conversion failed: {error}",
            status_code=500
        )
