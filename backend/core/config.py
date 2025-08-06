"""
AppSense Konfigürasyon Ayarları
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # API Ayarları
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AppSense"
    
    # Pinecone Ayarları
    PINECONE_API_KEY: str = ""
    PINECONE_ENVIRONMENT: str = "gcp-starter"
    PINECONE_INDEX_NAME: str = "appsense"
    
    # LLM Ayarları
    GROQ_API_KEY: str = ""
    LLM_MODEL: str = "llama3-8b-8192"
    
    # Embedding Model
    EMBEDDING_MODEL: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    
    # Veritabanı
    DATABASE_URL: str = "sqlite:///./appsense.db"
    
    # CORS
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # Arama Ayarları
    MAX_SEARCH_RESULTS: int = 10
    SIMILARITY_THRESHOLD: float = 0.7
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 