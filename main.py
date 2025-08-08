from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, FileResponse
import markdown
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import tempfile
import os
from pathlib import Path
import re
from html import unescape

app = FastAPI(title="Simple FastAPI App", description="A simple FastAPI application that returns success responses and converts Markdown to PDF")

@app.get("/")
async def root():
    """Root endpoint that returns a success message"""
    return {"message": "Hello World!", "status": "success"}

@app.get("/success")
async def success():
    """Success endpoint that returns a success response"""
    return JSONResponse(
        status_code=200,
        content={
            "message": "Success!",
            "status": "success",
            "data": {
                "timestamp": "2024-01-01T00:00:00Z",
                "version": "1.0.0"
            }
        }
    )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Service is running"}

def create_exact_cursor_styles():
    """Create styles that exactly match Cursor's Markdown preview"""
    styles = getSampleStyleSheet()
    
    # Exact colors from Cursor's theme
    text_color = colors.HexColor('#24292f')      # Main text
    code_bg = colors.HexColor('#f6f8fa')        # Code background
    code_border = colors.HexColor('#d0d7de')    # Code border
    quote_color = colors.HexColor('#656d76')     # Quote text
    link_color = colors.HexColor('#0969da')      # Link color
    table_header_bg = colors.HexColor('#f6f8fa')
    table_border = colors.HexColor('#d0d7de')
    table_alt_row = colors.HexColor('#f6f8fa')
    
    # H1 - Exact Cursor styling
    h1_style = ParagraphStyle(
        'ExactH1',
        parent=styles['Normal'],
        fontSize=32,
        spaceAfter=24,
        spaceBefore=40,
        textColor=text_color,
        alignment=TA_LEFT,
        fontName='Helvetica-Bold',
        leading=38,
        leftIndent=0,
        rightIndent=0,
        firstLineIndent=0,
        borderWidth=0,
        borderColor=code_border,
        borderPadding=0
    )
    
    # H2 - Exact Cursor styling
    h2_style = ParagraphStyle(
        'ExactH2',
        parent=styles['Normal'],
        fontSize=24,
        spaceAfter=20,
        spaceBefore=32,
        textColor=text_color,
        alignment=TA_LEFT,
        fontName='Helvetica-Bold',
        leading=28,
        leftIndent=0,
        rightIndent=0,
        firstLineIndent=0,
        borderWidth=0,
        borderColor=code_border,
        borderPadding=0
    )
    
    # H3 - Exact Cursor styling
    h3_style = ParagraphStyle(
        'ExactH3',
        parent=styles['Normal'],
        fontSize=20,
        spaceAfter=16,
        spaceBefore=28,
        textColor=text_color,
        alignment=TA_LEFT,
        fontName='Helvetica-Bold',
        leading=24,
        leftIndent=0,
        rightIndent=0,
        firstLineIndent=0,
        borderWidth=0,
        borderColor=code_border,
        borderPadding=0
    )
    
    # H4 - Exact Cursor styling
    h4_style = ParagraphStyle(
        'ExactH4',
        parent=styles['Normal'],
        fontSize=18,
        spaceAfter=14,
        spaceBefore=24,
        textColor=text_color,
        alignment=TA_LEFT,
        fontName='Helvetica-Bold',
        leading=22,
        leftIndent=0,
        rightIndent=0,
        firstLineIndent=0,
        borderWidth=0,
        borderColor=code_border,
        borderPadding=0
    )
    
    # Normal text - Exact Cursor styling
    normal_style = ParagraphStyle(
        'ExactNormal',
        parent=styles['Normal'],
        fontSize=16,
        spaceAfter=12,
        spaceBefore=0,
        textColor=text_color,
        alignment=TA_LEFT,
        fontName='Helvetica',
        leading=24,
        leftIndent=0,
        rightIndent=0,
        firstLineIndent=0,
        borderWidth=0,
        borderColor=code_border,
        borderPadding=0
    )
    
    # Code block - Exact Cursor styling
    code_style = ParagraphStyle(
        'ExactCode',
        parent=styles['Normal'],
        fontSize=14,
        spaceAfter=20,
        spaceBefore=20,
        textColor=text_color,
        alignment=TA_LEFT,
        fontName='Courier',
        leading=18,
        leftIndent=0,
        rightIndent=0,
        firstLineIndent=0,
        borderWidth=1,
        borderColor=code_border,
        borderPadding=20,
        backColor=code_bg
    )
    
    # Inline code - Exact Cursor styling
    inline_code_style = ParagraphStyle(
        'ExactInlineCode',
        parent=styles['Normal'],
        fontSize=14,
        spaceAfter=0,
        spaceBefore=0,
        textColor=text_color,
        alignment=TA_LEFT,
        fontName='Courier',
        leading=18,
        leftIndent=0,
        rightIndent=0,
        firstLineIndent=0,
        borderWidth=0.5,
        borderColor=code_border,
        borderPadding=6,
        backColor=code_bg
    )
    
    # List - Exact Cursor styling
    list_style = ParagraphStyle(
        'ExactList',
        parent=normal_style,
        fontSize=16,
        spaceAfter=6,
        spaceBefore=6,
        textColor=text_color,
        alignment=TA_LEFT,
        fontName='Helvetica',
        leading=24,
        leftIndent=24,
        rightIndent=0,
        firstLineIndent=0,
        borderWidth=0,
        borderColor=code_border,
        borderPadding=0
    )
    
    # Quote - Exact Cursor styling
    quote_style = ParagraphStyle(
        'ExactQuote',
        parent=normal_style,
        fontSize=16,
        spaceAfter=12,
        spaceBefore=12,
        textColor=quote_color,
        alignment=TA_LEFT,
        fontName='Helvetica',
        leading=24,
        leftIndent=24,
        rightIndent=0,
        firstLineIndent=0,
        borderWidth=0,
        borderColor=code_border,
        borderPadding=0,
        leftBorderWidth=4,
        leftBorderColor=code_border,
        leftBorderPadding=16
    )
    
    return {
        'h1': h1_style,
        'h2': h2_style,
        'h3': h3_style,
        'h4': h4_style,
        'normal': normal_style,
        'code': code_style,
        'inline_code': inline_code_style,
        'list': list_style,
        'quote': quote_style
    }

def parse_markdown_exactly(md_content):
    """Parse markdown content with exact Cursor-style formatting"""
    # Get exact styles
    styles = create_exact_cursor_styles()
    
    elements = []
    
    # Split content by lines
    lines = md_content.split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Skip empty lines
        if not line:
            i += 1
            continue
        
        # Handle headers with exact styling
        if line.startswith('# '):
            text = format_inline_markdown_exactly(line[2:])
            elements.append(Paragraph(text, styles['h1']))
        elif line.startswith('## '):
            text = format_inline_markdown_exactly(line[3:])
            elements.append(Paragraph(text, styles['h2']))
        elif line.startswith('### '):
            text = format_inline_markdown_exactly(line[4:])
            elements.append(Paragraph(text, styles['h3']))
        elif line.startswith('#### '):
            text = format_inline_markdown_exactly(line[5:])
            elements.append(Paragraph(text, styles['h4']))
        
        # Handle lists with exact styling
        elif line.startswith('- ') or line.startswith('* '):
            bullet_text = line[2:]
            formatted_text = format_inline_markdown_exactly(bullet_text)
            elements.append(Paragraph(f"• {formatted_text}", styles['list']))
        
        # Handle numbered lists
        elif re.match(r'^\d+\. ', line):
            number_text = re.sub(r'^\d+\. ', '', line)
            formatted_text = format_inline_markdown_exactly(number_text)
            elements.append(Paragraph(f"• {formatted_text}", styles['list']))
        
        # Handle code blocks with exact styling
        elif line.startswith('```'):
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            if code_lines:
                code_text = '\n'.join(code_lines)
                elements.append(Paragraph(f"<code>{code_text}</code>", styles['code']))
        
        # Handle blockquotes with exact styling
        elif line.startswith('> '):
            quote_text = line[2:]
            formatted_text = format_inline_markdown_exactly(quote_text)
            elements.append(Paragraph(formatted_text, styles['quote']))
        
        # Handle tables with exact styling
        elif '|' in line and i + 1 < len(lines) and '|' in lines[i + 1]:
            # Exact table parsing
            table_data = []
            while i < len(lines) and '|' in lines[i]:
                row = [cell.strip() for cell in lines[i].split('|')[1:-1]]
                table_data.append(row)
                i += 1
            if table_data:
                table = Table(table_data)
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f6f8fa')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#24292f')),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 14),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('TOPPADDING', (0, 0), (-1, 0), 12),
                    ('LEFTPADDING', (0, 0), (-1, -1), 12),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                    ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#24292f')),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 14),
                    ('BOTTOMPADDING', (0, 1), (-1, -1), 12),
                    ('TOPPADDING', (0, 1), (-1, -1), 12),
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d0d7de')),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f6f8fa')])
                ]))
                elements.append(table)
                elements.append(Spacer(1, 20))
            continue
        
        # Handle horizontal rules
        elif line.startswith('---') or line.startswith('***'):
            elements.append(Spacer(1, 32))
            # Add exact horizontal rule
            hr_style = ParagraphStyle(
                'ExactHR',
                parent=styles['normal'],
                borderWidth=1,
                borderColor=colors.HexColor('#d0d7de'),
                spaceAfter=32,
                spaceBefore=32,
                leading=1
            )
            elements.append(Paragraph("", hr_style))
        
        # Handle regular text with exact styling
        else:
            formatted_text = format_inline_markdown_exactly(line)
            elements.append(Paragraph(formatted_text, styles['normal']))
        
        i += 1
    
    return elements

def format_inline_markdown_exactly(text):
    """Format inline markdown elements with exact HTML tags"""
    # Bold
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    # Italic
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    # Inline code with exact styling
    text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)
    # Links (simple handling)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1', text)
    # Unescape HTML entities
    text = unescape(text)
    return text

@app.post("/convert-md-to-pdf")
async def convert_md_to_pdf(file: UploadFile = File(...)):
    """
    Convert uploaded Markdown file to PDF with exact Cursor-style formatting
    """
    # Check if file is provided
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    # Check file extension
    if not file.filename.lower().endswith('.md'):
        raise HTTPException(status_code=400, detail="File must be a Markdown (.md) file")
    
    try:
        # Read the markdown content
        content = await file.read()
        md_content = content.decode('utf-8')
        
        # Create a temporary file for the PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            pdf_path = tmp_file.name
        
        # Create PDF document with exact margins
        doc = SimpleDocTemplate(
            pdf_path, 
            pagesize=A4,
            rightMargin=30*mm,
            leftMargin=30*mm,
            topMargin=30*mm,
            bottomMargin=30*mm
        )
        
        # Parse markdown with exact styling
        elements = parse_markdown_exactly(md_content)
        
        # Build PDF
        doc.build(elements)
        
        # Return the PDF file for download
        return FileResponse(
            path=pdf_path,
            filename=f"{Path(file.filename).stem}.pdf",
            media_type='application/pdf'
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error converting file: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
