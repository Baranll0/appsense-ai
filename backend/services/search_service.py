"""
AppSense Arama Servisi
"""

import logging
from typing import List, Optional, Dict, Any
from models.embeddings.embedding_model import EmbeddingModel
from models.vectorstore.pinecone_store import PineconeStore
from utils.language_detector import LanguageDetector
from core.config import settings

logger = logging.getLogger(__name__)

class SearchService:
    """Uygulama arama servisi"""
    
    def __init__(self):
        self.embedding_model = EmbeddingModel()
        self.vector_store = PineconeStore()
        self.language_detector = LanguageDetector()
        
    async def search_apps(
        self, 
        query: str, 
        language: Optional[str] = None,
        category: Optional[str] = None,
        max_results: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Uygulama arama fonksiyonu
        
        Args:
            query: Arama sorgusu
            language: Dil (opsiyonel)
            category: Kategori filtresi (opsiyonel)
            max_results: Maksimum sonuç sayısı
            
        Returns:
            Uygulama listesi
        """
        try:
            # Dil algılama
            if not language:
                language = self.language_detector.detect_language(query)
            
            # Sorguyu embedding'e çevir
            query_embedding = self.embedding_model.encode(query)
            
            # Vektör veritabanında arama
            search_results = await self.vector_store.search(
                query_embedding=query_embedding,
                top_k=max_results,
                filter_category=category
            )
            
            # Sonuçları formatla
            formatted_results = []
            for result in search_results:
                app_data = {
                    'id': result.get('id'),
                    'name': result.get('name', ''),
                    'description': result.get('description', ''),
                    'category': result.get('category', ''),
                    'rating': result.get('rating'),
                    'review_count': result.get('review_count'),
                    'download_count': result.get('download_count', ''),
                    'price': result.get('price', 'Ücretsiz'),
                    'developer': result.get('developer', ''),
                    'similarity_score': result.get('score', 0.0)
                }
                formatted_results.append(app_data)
            
            logger.info(f"Arama tamamlandı: {len(formatted_results)} sonuç bulundu")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Arama hatası: {str(e)}")
            raise Exception(f"Arama sırasında hata oluştu: {str(e)}")
    
    async def get_categories(self) -> List[str]:
        """Mevcut kategorileri getir"""
        return [
            "Fitness", "Finance", "Education", "Entertainment",
            "Productivity", "Social", "Games", "Health", "Travel"
        ]
    
    async def get_app_by_id(self, app_id: str) -> Optional[Dict[str, Any]]:
        """ID ile uygulama getir"""
        try:
            app_data = await self.vector_store.get_by_id(app_id)
            if app_data:
                return {
                    'id': app_data.get('id'),
                    'name': app_data.get('name', ''),
                    'description': app_data.get('description', ''),
                    'category': app_data.get('category', ''),
                    'rating': app_data.get('rating'),
                    'review_count': app_data.get('review_count'),
                    'download_count': app_data.get('download_count', ''),
                    'price': app_data.get('price', 'Ücretsiz'),
                    'developer': app_data.get('developer', ''),
                    'similarity_score': 1.0
                }
            return None
        except Exception as e:
            logger.error(f"Uygulama getirme hatası: {str(e)}")
            return None 