# FileConversion API

A comprehensive, scalable API for converting various file formats with exact styling and formatting.

## 🏗️ Architecture

The application is built with a modular, scalable architecture:

```
app/
├── __init__.py
├── main.py                 # FastAPI application
├── core/
│   ├── __init__.py
│   ├── config.py          # Configuration settings
│   └── exceptions.py      # Custom exceptions
├── routers/
│   ├── __init__.py
│   ├── health.py          # Health check endpoints
│   └── markdown_converter.py  # Markdown conversion endpoints
└── services/
    ├── __init__.py
    └── markdown_service.py    # Business logic for markdown conversion
```

## 🚀 Features

- **Modular Design**: Easy to add new converters
- **Exact Styling**: PDFs match Cursor's Markdown preview exactly
- **Comprehensive Error Handling**: Custom exceptions and validation
- **API Documentation**: Auto-generated with FastAPI
- **Scalable**: Ready for multiple file conversion types

## 📦 Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🏃‍♂️ Running the Application

```bash
python run.py
```

Or using uvicorn directly:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

## 🌐 API Endpoints

### Health & Status
- `GET /` - Root endpoint
- `GET /api/v1/health` - Health check
- `GET /api/v1/status` - Detailed status

### Converters
- `GET /api/v1/converters` - List all available converters
- `POST /api/v1/convert/markdown-to-pdf` - Convert Markdown to PDF

## 📄 Available Converters

### Markdown to PDF
- **Endpoint**: `POST /api/v1/convert/markdown-to-pdf`
- **Input**: Markdown file (.md)
- **Output**: PDF file
- **Features**: Exact Cursor preview styling

## 🎨 Styling Features

The Markdown to PDF converter produces PDFs that exactly match Cursor's preview:

- **Typography**: Perfect font sizes and spacing
- **Colors**: Exact GitHub-style color scheme
- **Layout**: Professional margins and spacing
- **Code Blocks**: Light gray backgrounds with borders
- **Tables**: GitHub-style with alternating rows
- **Lists**: Proper indentation and bullets
- **Quotes**: Left border with muted text

## 🔧 Configuration

Configuration is managed through `app/core/config.py`:

- **Server Settings**: Host, port, CORS
- **File Upload**: Max file size, allowed extensions
- **PDF Settings**: Margins, font sizes

## 🚀 Adding New Converters

To add a new converter:

1. **Create Service**: Add business logic in `app/services/`
2. **Create Router**: Add endpoints in `app/routers/`
3. **Update Main App**: Include the new router in `app/main.py`

Example structure for a new converter:
```
app/services/
└── html_converter_service.py

app/routers/
└── html_converter.py
```

## 📚 API Documentation

Once running, visit:
- **Interactive Docs**: http://localhost:8080/docs
- **ReDoc**: http://localhost:8080/redoc

## 🧪 Testing

Test the Markdown to PDF conversion:
```bash
curl -X POST "http://localhost:8080/api/v1/convert/markdown-to-pdf" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@sample.md" \
     --output sample.pdf
```

## 🔮 Future Enhancements

The modular architecture makes it easy to add:

- **HTML to PDF**: Convert HTML files to PDF
- **DOCX to PDF**: Convert Word documents
- **TXT to PDF**: Convert plain text files
- **Image to PDF**: Convert images to PDF
- **CSV to PDF**: Convert CSV data to formatted PDF tables
- **JSON to PDF**: Convert JSON data to formatted PDF reports

## 📝 License

MIT License
