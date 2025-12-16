from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import easyocr
import cv2
import numpy as np
from PIL import Image
import io
import spacy
import re
from typing import Dict, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Intelligent OCR System",
    description="AI-powered OCR with layout analysis and entity extraction",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize models
logger.info("Initializing OCR reader...")
reader = easyocr.Reader(['en'], gpu=False)

logger.info("Loading spaCy model...")
try:
    nlp = spacy.load("en_core_web_sm")
except:
    logger.warning("Downloading spaCy model...")
    import os
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")


class LayoutAnalyzer:
    """Analyzes document layout structure"""
    
    def analyze_layout(self, image: np.ndarray) -> Dict:
        """Detect document structure: headers, paragraphs, tables"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detect horizontal and vertical lines (for tables)
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
        
        horizontal_lines = cv2.morphologyEx(gray, cv2.MORPH_OPEN, horizontal_kernel)
        vertical_lines = cv2.morphologyEx(gray, cv2.MORPH_OPEN, vertical_kernel)
        
        # Detect text blocks using contours
        _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        blocks = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w > 50 and h > 20:  # Filter small noise
                blocks.append({
                    "type": self._classify_block(w, h),
                    "bbox": [int(x), int(y), int(w), int(h)],
                    "area": int(w * h)
                })
        
        # Sort blocks by position (top to bottom, left to right)
        blocks.sort(key=lambda b: (b["bbox"][1], b["bbox"][0]))
        
        return {
            "blocks": blocks,
            "total_blocks": len(blocks),
            "has_tables": bool(np.sum(horizontal_lines) > 0 or np.sum(vertical_lines) > 0)
        }
    
    def _classify_block(self, width: int, height: int) -> str:
        """Classify block as header, paragraph, or table"""
        aspect_ratio = width / height if height > 0 else 0
        
        if aspect_ratio > 10:
            return "header"
        elif aspect_ratio > 3:
            return "paragraph"
        elif aspect_ratio < 1.5:
            return "table_cell"
        else:
            return "text_block"


class EntityExtractor:
    """Extracts named entities and patterns from text"""
    
    def __init__(self, nlp_model):
        self.nlp = nlp_model
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract named entities and custom patterns"""
        doc = self.nlp(text)
        
        entities = {
            "persons": [],
            "organizations": [],
            "locations": [],
            "dates": [],
            "emails": [],
            "phones": [],
            "amounts": [],
            "urls": []
        }
        
        # NER entities from spaCy
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                entities["persons"].append(ent.text)
            elif ent.label_ == "ORG":
                entities["organizations"].append(ent.text)
            elif ent.label_ == "GPE" or ent.label_ == "LOC":
                entities["locations"].append(ent.text)
            elif ent.label_ == "DATE":
                entities["dates"].append(ent.text)
            elif ent.label_ == "MONEY":
                entities["amounts"].append(ent.text)
        
        # Regex patterns for structured data
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_pattern = r'\b(?:\+?1[-.]?)?\(?\d{3}\)?[-.]?\d{3}[-.]?\d{4}\b'
        url_pattern = r'https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)'
        
        entities["emails"] = list(set(re.findall(email_pattern, text)))
        entities["phones"] = list(set(re.findall(phone_pattern, text)))
        entities["urls"] = list(set(re.findall(url_pattern, text)))
        
        # Remove duplicates and clean
        for key in entities:
            entities[key] = list(set(entities[key]))
        
        return entities


# Initialize analyzers
layout_analyzer = LayoutAnalyzer()
entity_extractor = EntityExtractor(nlp)


def preprocess_image(image: np.ndarray) -> np.ndarray:
    """Preprocess image for better OCR results"""
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Denoise
    denoised = cv2.fastNlMeansDenoising(gray)
    
    # Adaptive thresholding for better contrast
    binary = cv2.adaptiveThreshold(
        denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    
    return binary


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Intelligent OCR API",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "process": "/api/process-document",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "ocr_ready": reader is not None,
        "nlp_ready": nlp is not None
    }


@app.post("/api/process-document")
async def process_document(file: UploadFile = File(...)):
    """
    Complete document processing pipeline:
    1. OCR text extraction
    2. Layout analysis
    3. Entity extraction
    4. Post-processing
    """
    try:
        logger.info(f"Processing file: {file.filename}")
        
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read and decode image
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            raise HTTPException(status_code=400, detail="Invalid image file")
        
        # Step 1: Preprocess image
        logger.info("Preprocessing image...")
        preprocessed = preprocess_image(image)
        
        # Step 2: OCR extraction
        logger.info("Performing OCR...")
        ocr_results = reader.readtext(preprocessed)
        
        # Extract text with confidence scores
        text_blocks = []
        for (bbox, text, confidence) in ocr_results:
            text_blocks.append({
                "text": text,
                "confidence": float(confidence),
                "bbox": [[int(coord) for coord in point] for point in bbox]
            })
        
        full_text = " ".join([block["text"] for block in text_blocks])
        avg_confidence = np.mean([block["confidence"] for block in text_blocks]) if text_blocks else 0
        
        # Step 3: Layout analysis
        logger.info("Analyzing layout...")
        layout = layout_analyzer.analyze_layout(image)
        
        # Step 4: Entity extraction
        logger.info("Extracting entities...")
        entities = entity_extractor.extract_entities(full_text)
        
        # Step 5: Post-processing and structuring
        logger.info("Post-processing results...")
        
        # Calculate statistics
        word_count = len(full_text.split())
        char_count = len(full_text)
        
        # Build response
        response = {
            "success": True,
            "filename": file.filename,
            "ocr": {
                "full_text": full_text,
                "text_blocks": text_blocks,
                "average_confidence": float(avg_confidence),
                "word_count": word_count,
                "character_count": char_count
            },
            "layout": layout,
            "entities": entities,
            "metadata": {
                "image_dimensions": {
                    "width": int(image.shape[1]),
                    "height": int(image.shape[0]),
                    "channels": int(image.shape[2])
                },
                "processing_complete": True,
                "total_entities_found": sum(len(v) for v in entities.values())
            }
        }
        
        logger.info(f"Processing complete for {file.filename}")
        return response
        
    except Exception as e:
        logger.error(f"Error processing document: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
