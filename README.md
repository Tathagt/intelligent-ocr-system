# 🔍 Intelligent OCR & Document Understanding System

**SPAZORLABS AI/ML Internship - Task 2**

An AI-powered OCR system that extracts text from scanned documents, analyzes layout structure, and identifies entities with high accuracy.

## 🎯 Features

- **Advanced OCR**: Text extraction using EasyOCR with preprocessing
- **Layout Analysis**: Detects headers, paragraphs, tables, and text blocks
- **Entity Extraction**: Identifies persons, organizations, emails, phones, dates, amounts, and URLs
- **Post-Processing**: Confidence scoring, text cleaning, and structured output
- **Interactive UI**: Beautiful Streamlit frontend with real-time processing
- **REST API**: FastAPI backend with comprehensive documentation

## 🏗️ Architecture

```
┌─────────────────┐
│   Frontend      │
│   (Streamlit)   │
└────────┬────────┘
         │ HTTP
         ▼
┌─────────────────┐
│   Backend API   │
│   (FastAPI)     │
└────────┬────────┘
         │
    ┌────┴────┬────────┬──────────┐
    ▼         ▼        ▼          ▼
┌────────┐ ┌──────┐ ┌──────┐ ┌────────┐
│EasyOCR │ │OpenCV│ │spaCy │ │Regex   │
└────────┘ └──────┘ └──────┘ └────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- pip

### Local Development

#### Backend

```bash
cd backend
pip install -r requirements.txt
python -m spacy download en_core_web_sm
uvicorn main:app --reload
```

Backend will run on `http://localhost:8000`

#### Frontend

```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

Frontend will run on `http://localhost:8501`

## 📦 Deployment

### Deploy Backend to Railway

1. Fork this repository
2. Go to [Railway](https://railway.app)
3. Click "New Project" → "Deploy from GitHub repo"
4. Select this repository
5. Railway will auto-detect the configuration
6. Copy the deployed URL

### Deploy Frontend to Streamlit Cloud

1. Go to [Streamlit Cloud](https://streamlit.io/cloud)
2. Click "New app"
3. Select this repository
4. Set main file path: `frontend/app.py`
5. Update the API URL in the frontend to your Railway backend URL
6. Deploy!

### Alternative: Deploy Backend to Render

1. Go to [Render](https://render.com)
2. Click "New" → "Web Service"
3. Connect this repository
4. Render will use `render.yaml` configuration
5. Deploy and copy the URL

## 🔧 API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Main Endpoint

**POST** `/api/process-document`

Upload an image file to process.

**Request:**
- Content-Type: `multipart/form-data`
- Body: `file` (image file)

**Response:**
```json
{
  "success": true,
  "filename": "document.jpg",
  "ocr": {
    "full_text": "Extracted text...",
    "text_blocks": [...],
    "average_confidence": 0.95,
    "word_count": 150,
    "character_count": 850
  },
  "layout": {
    "blocks": [...],
    "total_blocks": 12,
    "has_tables": true
  },
  "entities": {
    "persons": ["John Doe"],
    "organizations": ["ACME Corp"],
    "emails": ["john@example.com"],
    "phones": ["555-1234"],
    "dates": ["2025-12-16"],
    "amounts": ["$1,000"],
    "locations": ["New York"],
    "urls": ["https://example.com"]
  },
  "metadata": {
    "image_dimensions": {...},
    "processing_complete": true,
    "total_entities_found": 8
  }
}
```

## 🧪 Testing

Test with sample documents:

```bash
curl -X POST "http://localhost:8000/api/process-document" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@sample_document.jpg"
```

## 📊 Technology Stack

### Backend
- **FastAPI**: Modern web framework
- **EasyOCR**: OCR engine
- **OpenCV**: Image preprocessing
- **spaCy**: NLP and entity extraction
- **NumPy**: Numerical operations

### Frontend
- **Streamlit**: Interactive web UI
- **Requests**: HTTP client
- **Pillow**: Image handling

## 🎨 Features in Detail

### 1. OCR Text Extraction
- Preprocessing with denoising and adaptive thresholding
- Multi-language support (currently English)
- Confidence scoring for each text block
- Bounding box detection

### 2. Layout Analysis
- Automatic detection of document structure
- Classification of text blocks (headers, paragraphs, tables)
- Table detection using morphological operations
- Spatial ordering of content

### 3. Entity Extraction
- Named Entity Recognition (NER) using spaCy
- Pattern matching for structured data
- Support for multiple entity types
- Deduplication and cleaning

### 4. Post-Processing
- Text normalization
- Confidence-based filtering
- Structured JSON output
- Comprehensive metadata

## 📝 Project Structure

```
intelligent-ocr-system/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile          # Container configuration
├── frontend/
│   ├── app.py              # Streamlit application
│   └── requirements.txt    # Frontend dependencies
├── .streamlit/
│   └── config.toml         # Streamlit configuration
├── railway.json            # Railway deployment config
├── render.yaml            # Render deployment config
└── README.md              # This file
```

## 🔒 Security

- CORS enabled for frontend communication
- File type validation
- Error handling and logging
- Input sanitization

## 🚧 Future Enhancements

- [ ] Multi-language OCR support
- [ ] PDF document processing
- [ ] Batch processing
- [ ] Custom entity training
- [ ] Export to multiple formats (PDF, DOCX)
- [ ] OCR result editing interface
- [ ] Database integration for history
- [ ] User authentication

## 📄 License

MIT License

## 👨‍💻 Author

**Sam Carr**
- Email: carr9156@gmail.com
- GitHub: [@Tathagt](https://github.com/Tathagt)

## 🙏 Acknowledgments

- SPAZORLABS for the internship opportunity
- EasyOCR team for the OCR engine
- spaCy team for NLP capabilities
- FastAPI and Streamlit communities

---

**Built for SPAZORLABS AI/ML Internship - December 2025**
