"""
AppSense Backend - LLM + RAG Tabanlı Uygulama Mağazası Arama Motoru
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

from api.routes import search_router
from core.config import settings

app = FastAPI(
    title="AppSense API",
    description="LLM + RAG Tabanlı Uygulama Mağazası Arama Motoru",
    version="1.0.0"
)

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router'ları ekle
app.include_router(search_router, prefix="/api/v1")

@app.get("/")
async def root():
    """Ana endpoint"""
    return {
        "message": "AppSense API'ye Hoş Geldiniz!",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Sağlık kontrolü"""
    return {"status": "healthy", "service": "AppSense API"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 