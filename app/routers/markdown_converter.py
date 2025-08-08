from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import FileResponse
from pathlib import Path
from app.services.markdown_service import markdown_service
from app.core.exceptions import UnsupportedFileTypeError, FileTooLargeError
from app.core.config import settings

router = APIRouter()

def validate_markdown_file(file: UploadFile) -> UploadFile:
    """Validate uploaded markdown file"""
    if not file:
        raise UnsupportedFileTypeError("No file uploaded")
    
    # Check file extension
    if not file.filename.lower().endswith('.md'):
        raise UnsupportedFileTypeError(f"File must be a Markdown (.md) file, got {Path(file.filename).suffix}")
    
    # Check file size
    if hasattr(file, 'size') and file.size > settings.MAX_FILE_SIZE:
        raise FileTooLargeError(settings.MAX_FILE_SIZE)
    
    return file

@router.post("/convert/markdown-to-pdf")
async def convert_markdown_to_pdf(
    file: UploadFile = Depends(validate_markdown_file)
):
    """
    Convert uploaded Markdown file to PDF with exact Cursor-style formatting
    
    - **file**: Markdown file (.md) to convert
    - **Returns**: PDF file for download
    """
    try:
        # Read the markdown content
        content = await file.read()
        md_content = content.decode('utf-8')
        
        # Convert to PDF
        pdf_path = await markdown_service.convert_markdown_to_pdf(md_content, file.filename)
        
        # Return the PDF file for download
        return FileResponse(
            path=pdf_path,
            filename=f"{Path(file.filename).stem}.pdf",
            media_type='application/pdf'
        )
        
    except Exception as e:
        raise UnsupportedFileTypeError(f"Error converting file: {str(e)}")

@router.get("/converters")
async def list_converters():
    """List all available converters"""
    return {
        "converters": [
            {
                "name": "Markdown to PDF",
                "endpoint": "/api/v1/convert/markdown-to-pdf",
                "description": "Convert Markdown files to PDF with exact Cursor styling",
                "supported_formats": [".md"],
                "output_format": "PDF"
            }
        ],
        "total": 1
    }
