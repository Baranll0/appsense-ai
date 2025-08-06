"""
AppSense API Routes
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
import logging

from services.search_service import SearchService
from services.llm_service import LLMService
from utils.language_detector import LanguageDetector
from core.config import settings

# Router oluştur
search_router = APIRouter()

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic modelleri
class SearchRequest(BaseModel):
    query: str
    language: Optional[str] = None
    category: Optional[str] = None
    max_results: Optional[int] = 10

class AppInfo(BaseModel):
    id: str
    name: str
    description: str
    category: str
    rating: Optional[float]
    review_count: Optional[int]
    download_count: Optional[str]
    price: Optional[str]
    developer: str
    similarity_score: float

class SearchResponse(BaseModel):
    query: str
    results: List[AppInfo]
    total_found: int
    processing_time: float
    language_detected: str
    llm_analysis: Optional[str] = None

@search_router.post("/search", response_model=SearchResponse)
async def search_apps(request: SearchRequest):
    """
    Uygulama arama endpoint'i (POST)
    """
    try:
        # Search service'i başlat
        search_service = SearchService()
        llm_service = LLMService()
        language_detector = LanguageDetector()
        
        # Dil algılama
        detected_language = language_detector.detect_language(request.query)
        
        # Arama yap
        results = await search_service.search_apps(
            query=request.query,
            language=request.language,
            category=request.category,
            max_results=request.max_results
        )
        
        # LLM ile analiz yap
        llm_analysis = await llm_service.analyze_search_results(
            query=request.query,
            search_results=results,
            detected_language=detected_language
        )
        
        return SearchResponse(
            query=request.query,
            results=results,
            total_found=len(results),
            processing_time=0.0,  # TODO: Gerçek süre hesapla
            language_detected=detected_language,
            llm_analysis=llm_analysis
        )
        
    except Exception as e:
        logger.error(f"Arama hatası: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Arama sırasında hata oluştu: {str(e)}")

@search_router.get("/search", response_model=SearchResponse)
async def search_apps_get(
    query: str = Query(..., description="Arama sorgusu"),
    category: Optional[str] = Query(None, description="Kategori filtresi"),
    max_results: Optional[int] = Query(10, description="Maksimum sonuç sayısı")
):
    """
    Uygulama arama endpoint'i (GET)
    """
    try:
        # Search service'i başlat
        search_service = SearchService()
        llm_service = LLMService()
        language_detector = LanguageDetector()
        
        # Dil algılama
        detected_language = language_detector.detect_language(query)
        
        # Arama yap
        results = await search_service.search_apps(
            query=query,
            category=category,
            max_results=max_results
        )
        
        # LLM ile analiz yap
        llm_analysis = await llm_service.analyze_search_results(
            query=query,
            search_results=results,
            detected_language=detected_language
        )
        
        return SearchResponse(
            query=query,
            results=results,
            total_found=len(results),
            processing_time=0.0,
            language_detected=detected_language,
            llm_analysis=llm_analysis
        )
        
    except Exception as e:
        logger.error(f"Arama hatası: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Arama sırasında hata oluştu: {str(e)}")

@search_router.get("/categories")
async def get_categories():
    """
    Mevcut kategorileri getir
    """
    categories = [
        "Fitness", "Finance", "Education", "Entertainment", 
        "Productivity", "Social", "Games", "Health", "Travel"
    ]
    return {"categories": categories}

@search_router.get("/health")
async def health_check():
    """
    API sağlık kontrolü
    """
    return {"status": "healthy", "service": "AppSense Search API"} 