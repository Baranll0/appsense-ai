"""
AppSense Pinecone Vector Store
"""

import logging
from typing import List, Dict, Any, Optional
from pinecone import Pinecone
from core.config import settings

logger = logging.getLogger(__name__)

class PineconeStore:
    """Pinecone vektör veritabanı işlemleri"""
    
    def __init__(self):
        self.index = None
        self.pc = None
        self._initialize_pinecone()
    
    def _initialize_pinecone(self):
        """Pinecone'u başlat"""
        try:
            if not settings.PINECONE_API_KEY:
                logger.warning("Pinecone API key bulunamadı")
                return
            
            # Yeni Pinecone API'si
            self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
            
            # Index'i kontrol et/oluştur
            index_name = settings.PINECONE_INDEX_NAME
            if index_name not in self.pc.list_indexes().names():
                logger.info(f"Pinecone index oluşturuluyor: {index_name}")
                self.pc.create_index(
                    name=index_name,
                    dimension=384,  # sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
                    metric="cosine"
                )
            
            self.index = self.pc.Index(index_name)
            logger.info("Pinecone başarıyla başlatıldı")
            
        except Exception as e:
            logger.error(f"Pinecone başlatma hatası: {str(e)}")
            self.index = None
    
    async def upsert_apps(self, apps_data: List[Dict[str, Any]]) -> bool:
        """
        Uygulamaları vektör veritabanına ekle/güncelle
        
        Args:
            apps_data: Uygulama verileri listesi
            
        Returns:
            Başarı durumu
        """
        if not self.index:
            logger.error("Pinecone index bulunamadı")
            return False
        
        try:
            vectors = []
            for app in apps_data:
                # Embedding'i hazırla
                embedding = app.get('embedding')
                if not embedding:
                    continue
                
                # Metadata'yı hazırla
                metadata = {
                    'name': app.get('name', ''),
                    'description': app.get('description', ''),
                    'category': app.get('category', ''),
                    'rating': app.get('rating'),
                    'review_count': app.get('review_count'),
                    'download_count': app.get('download_count', ''),
                    'price': app.get('price', 'Ücretsiz'),
                    'developer': app.get('developer', ''),
                    'app_id': app.get('id', '')
                }
                
                vectors.append({
                    'id': app.get('id'),
                    'values': embedding,
                    'metadata': metadata
                })
            
            if vectors:
                self.index.upsert(vectors=vectors)
                logger.info(f"{len(vectors)} uygulama vektör veritabanına eklendi")
                return True
            else:
                logger.warning("Eklenecek vektör bulunamadı")
                return False
                
        except Exception as e:
            logger.error(f"Vektör ekleme hatası: {str(e)}")
            return False
    
    async def search(
        self, 
        query_embedding: List[float], 
        top_k: int = 10,
        filter_category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Vektör veritabanında arama yap
        
        Args:
            query_embedding: Sorgu embedding'i
            top_k: Maksimum sonuç sayısı
            filter_category: Kategori filtresi
            
        Returns:
            Arama sonuçları
        """
        if not self.index:
            logger.error("Pinecone index bulunamadı")
            return []
        
        try:
            # Filtre oluştur
            filter_dict = {}
            if filter_category:
                filter_dict['category'] = filter_category
            
            # Arama yap
            search_results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True,
                filter=filter_dict if filter_dict else None
            )
            
            # Sonuçları formatla
            formatted_results = []
            for match in search_results.matches:
                result = {
                    'id': match.id,
                    'score': match.score,
                    **match.metadata
                }
                formatted_results.append(result)
            
            logger.info(f"Arama tamamlandı: {len(formatted_results)} sonuç bulundu")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Arama hatası: {str(e)}")
            return []
    
    async def get_by_id(self, app_id: str) -> Optional[Dict[str, Any]]:
        """ID ile uygulama getir"""
        if not self.index:
            return None
        
        try:
            fetch_results = self.index.fetch(ids=[app_id])
            if app_id in fetch_results.vectors:
                vector = fetch_results.vectors[app_id]
                return {
                    'id': vector.id,
                    **vector.metadata
                }
            return None
            
        except Exception as e:
            logger.error(f"ID ile getirme hatası: {str(e)}")
            return None
    
    async def delete_app(self, app_id: str) -> bool:
        """Uygulamayı sil"""
        if not self.index:
            return False
        
        try:
            self.index.delete(ids=[app_id])
            logger.info(f"Uygulama silindi: {app_id}")
            return True
            
        except Exception as e:
            logger.error(f"Silme hatası: {str(e)}")
            return False
    
    async def get_index_stats(self) -> Dict[str, Any]:
        """Index istatistiklerini getir"""
        if not self.index:
            return {"error": "Index bulunamadı"}
        
        try:
            stats = self.index.describe_index_stats()
            return {
                "total_vector_count": stats.total_vector_count,
                "dimension": stats.dimension,
                "index_fullness": stats.index_fullness,
                "namespaces": stats.namespaces
            }
            
        except Exception as e:
            logger.error(f"İstatistik alma hatası: {str(e)}")
            return {"error": str(e)} 