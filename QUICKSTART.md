# ⚡ Quick Start Guide

Get the Intelligent OCR System running in 5 minutes!

## 🚀 Local Development

### Prerequisites
- Python 3.10 or higher
- pip package manager
- Git

### Step 1: Clone Repository

```bash
git clone https://github.com/Tathagt/intelligent-ocr-system.git
cd intelligent-ocr-system
```

### Step 2: Start Backend

```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Start the server
uvicorn main:app --reload
```

Backend will run at: **http://localhost:8000**

✅ Test it: Open http://localhost:8000 in your browser

### Step 3: Start Frontend (New Terminal)

```bash
# Navigate to frontend directory (from project root)
cd frontend

# Install dependencies
pip install -r requirements.txt

# Start Streamlit
streamlit run app.py
```

Frontend will run at: **http://localhost:8501**

✅ Test it: Upload an image and click "Process Document"

---

## 🌐 Quick Deploy (No Code Required)

### Deploy Backend to Railway

1. **Fork this repository** on GitHub
2. Go to [Railway.app](https://railway.app)
3. Click "New Project" → "Deploy from GitHub repo"
4. Select `intelligent-ocr-system`
5. Wait 5-10 minutes for deployment
6. Copy your backend URL

### Deploy Frontend to Streamlit Cloud

1. Go to [Streamlit Cloud](https://streamlit.io/cloud)
2. Click "New app"
3. Select your forked repository
4. Main file: `frontend/app.py`
5. Click "Deploy"
6. Update API URL in the sidebar to your Railway URL

**Done! Your OCR system is live! 🎉**

---

## 🧪 Quick Test

### Test Backend API

```bash
# Health check
curl http://localhost:8000/health

# Process a document
curl -X POST "http://localhost:8000/api/process-document" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_image.jpg"
```

### Test Frontend

1. Open http://localhost:8501
2. Upload any document image (receipt, invoice, form, etc.)
3. Click "🚀 Process Document"
4. View extracted text, entities, and layout analysis

---

## 📝 Sample Test Images

Create a simple test document:
1. Open any text editor
2. Type some text with your name, email, and phone
3. Take a screenshot
4. Upload to the OCR system

Or use any:
- Receipt
- Invoice
- Business card
- Form
- Scanned document

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Make sure you're in the backend directory
cd backend

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Download spaCy model again
python -m spacy download en_core_web_sm
```

### Frontend can't connect to backend
- Make sure backend is running on port 8000
- Check the API URL in the frontend sidebar
- Verify CORS is enabled in backend

### Processing fails
- Check image file size (< 10MB)
- Ensure image format is supported (PNG, JPG, JPEG)
- Check backend logs for errors

---

## 📚 Next Steps

- Read [README.md](README.md) for detailed documentation
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
- Review [SUBMISSION.md](SUBMISSION.md) for project details
- Explore API docs at http://localhost:8000/docs

---

## 💡 Tips

- **Better OCR results**: Use high-resolution, clear images
- **Faster processing**: Reduce image size before upload
- **More entities**: Use documents with structured data
- **Test different formats**: Try receipts, forms, invoices

---

## 🎯 Common Use Cases

1. **Receipt Processing**: Extract items, prices, totals
2. **Invoice Analysis**: Get vendor info, amounts, dates
3. **Form Digitization**: Convert paper forms to structured data
4. **Business Card Scanning**: Extract contact information
5. **Document Archival**: Convert scanned docs to searchable text

---

**Ready to go! Start processing documents! 🚀**

Questions? Check the [README.md](README.md) or open an issue on GitHub.
