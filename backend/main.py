"""
MDRS Backend - Multimodal Deception Risk Scorer
FastAPI server for analyzing media and providing risk scores
"""
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional
import uvicorn
import os
import tempfile
from pathlib import Path

from risk_engine import RiskScoringEngine
from detectors.image_detector import ImageDetector
from detectors.video_detector import VideoDetector
from detectors.audio_detector import AudioDetector
from detectors.text_detector import TextDetector

from agents.orchestrator import fact_check_pipeline
from schemas.request import FactCheckRequest

app = FastAPI(
    title="MDRS API",
    description="Multimodal Deception Risk Scorer - Explainable Risk Assessment for Media",
    version="1.0.0"
)

# CORS configuration
# Get allowed origins from environment variable or use defaults
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,http://127.0.0.1:3000,https://abc.pages.dev"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize detectors and risk engine
image_detector = ImageDetector()
video_detector = VideoDetector()
audio_detector = AudioDetector()
text_detector = TextDetector()
risk_engine = RiskScoringEngine()

FAKE_KEYWORDS = [
    "shocking",
    "unbelievable",
    "must see",
    "breaking",
    "you won’t believe",
    "exposed",
    "secret",
    "urgent"
]

class PageData(BaseModel):
    url: str = ""
    title: str = ""
    text: str = ""



@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "operational",
        "service": "MDRS Backend",
        "version": "1.0.0",
        "disclaimer": "This system provides probabilistic risk assessment and does not determine truth."
    }


@app.post("/analyze/image")
async def analyze_image(
    file: UploadFile = File(...),
    source: Optional[str] = Form(None),
    timestamp: Optional[str] = Form(None),
    context: Optional[str] = Form(None)
):
    """
    Analyze an uploaded image for deception risk signals.
    
    Returns risk score, signals, and explainable recommendations.
    """
    try:
        # Validate file type
        if not file.content_type or not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="Invalid file type. Expected image.")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        try:
            # Run detection
            signals = image_detector.detect(tmp_path, {
                'source': source,
                'timestamp': timestamp,
                'context': context
            })
            
            # Calculate risk score (async)
            result = await risk_engine.calculate_risk(
                modality='image',
                signals=signals,
                metadata={'source': source, 'timestamp': timestamp, 'context': context}
            )
            
            return JSONResponse(content=result)
        
        finally:
            # Cleanup
            os.unlink(tmp_path)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/analyze/video")
async def analyze_video(
    file: UploadFile = File(...),
    source: Optional[str] = Form(None),
    timestamp: Optional[str] = Form(None),
    context: Optional[str] = Form(None)
):
    """
    Analyze an uploaded video for deception risk signals.
    
    Checks for facial artifacts, lighting inconsistencies, and temporal anomalies.
    """
    try:
        # Validate file type
        if not file.content_type or not file.content_type.startswith('video/'):
            raise HTTPException(status_code=400, detail="Invalid file type. Expected video.")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        try:
            # Run detection
            signals = video_detector.detect(tmp_path, {
                'source': source,
                'timestamp': timestamp,
                'context': context
            })
            
            # Calculate risk score (async)
            result = await risk_engine.calculate_risk(
                modality='video',
                signals=signals,
                metadata={'source': source, 'timestamp': timestamp, 'context': context}
            )
            
            return JSONResponse(content=result)
        
        finally:
            # Cleanup
            os.unlink(tmp_path)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/analyze/audio")
async def analyze_audio(
    file: UploadFile = File(...),
    source: Optional[str] = Form(None),
    timestamp: Optional[str] = Form(None),
    context: Optional[str] = Form(None)
):
    """
    Analyze an uploaded audio file for deception risk signals.
    
    Checks for spectral anomalies, voice synthesis artifacts, and phoneme inconsistencies.
    """
    try:
        # Validate file type
        if not file.content_type or not file.content_type.startswith('audio/'):
            raise HTTPException(status_code=400, detail="Invalid file type. Expected audio.")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        try:
            # Run detection
            signals = audio_detector.detect(tmp_path, {
                'source': source,
                'timestamp': timestamp,
                'context': context
            })
            
            # Calculate risk score (async)
            result = await risk_engine.calculate_risk(
                modality='audio',
                signals=signals,
                metadata={'source': source, 'timestamp': timestamp, 'context': context}
            )
            
            return JSONResponse(content=result)
        
        finally:
            # Cleanup
            os.unlink(tmp_path)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")



def detect_fake_news(text, title, url):
    score = 0
    content = (title + " " + text).lower()

    # sensational keywords
    for word in FAKE_KEYWORDS:
        if word in content:
            score += 1

    # too many capital letters
    if sum(c.isupper() for c in title) > len(title) * 0.4:
        score += 1

    # suspicious domains
    if any(x in url for x in [".xyz", ".click", ".buzz"]):
        score += 1

    if score >= 2:
        return "Suspicious"

    return "Safe"

@app.post("/analyze")
def analyze_page(data: PageData):

    print("Received:", data)

    status = detect_fake_news(
        data.text,
        data.title,
        data.url
    )

    return {"status": status}



@app.post("/analyze/text")
async def analyze_text(
    text: str = Form(...),
    source: Optional[str] = Form(None),
    timestamp: Optional[str] = Form(None),
    context: Optional[str] = Form(None)
):
    """
    Analyze text content for deception risk signals.
    
    Checks for sensational language, stylometric anomalies, and misinformation patterns.
    """
    try:
        if not text or len(text.strip()) == 0:
            raise HTTPException(status_code=400, detail="Text content cannot be empty.")
        
        # Run detection
        signals = text_detector.detect(text, {
            'source': source,
            'timestamp': timestamp,
            'context': context
        })
        
        # Calculate risk score (async)
        result = await risk_engine.calculate_risk(
            modality='text',
            signals=signals,
            metadata={'source': source, 'timestamp': timestamp, 'context': context}
        )
        
        return JSONResponse(content=result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/fact-check")
def feact_check(payload: FactCheckRequest):
    if not payload.text and not payload.url:
        raise HTTPException(status_code=400, detail="Text or URL is required.")
    
    result = fact_check_pipeline(
        input_text = payload.text, 
        url = payload.url
        )
        
    return result
    

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
