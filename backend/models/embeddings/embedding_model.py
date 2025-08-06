"""
AppSense Embedding Model
"""

import logging
from typing import List, Union
from sentence_transformers import SentenceTransformer
from core.config import settings

logger = logging.getLogger(__name__)

class EmbeddingModel:
    """Sentence Transformers tabanlı embedding modeli"""
    
    def __init__(self):
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Embedding modelini yükle"""
        try:
            model_name = settings.EMBEDDING_MODEL
            logger.info(f"Embedding modeli yükleniyor: {model_name}")
            
            self.model = SentenceTransformer(model_name)
            logger.info("Embedding modeli başarıyla yüklendi")
            
        except Exception as e:
            logger.error(f"Embedding modeli yükleme hatası: {str(e)}")
            raise Exception(f"Embedding modeli yüklenemedi: {str(e)}")
    
    def encode(self, text: Union[str, List[str]]) -> Union[List[float], List[List[float]]]:
        """
        Metni embedding'e çevir
        
        Args:
            text: Tek metin veya metin listesi
            
        Returns:
            Embedding vektörü veya vektör listesi
        """
        try:
            if not self.model:
                raise Exception("Embedding modeli yüklenmemiş")
            
            embeddings = self.model.encode(text)
            
            # Tek metin için liste döndür
            if isinstance(text, str):
                return embeddings.tolist()
            else:
                return embeddings.tolist()
                
        except Exception as e:
            logger.error(f"Embedding oluşturma hatası: {str(e)}")
            raise Exception(f"Embedding oluşturulamadı: {str(e)}")
    
    def encode_batch(self, texts: List[str], batch_size: int = 32) -> List[List[float]]:
        """
        Toplu embedding oluştur
        
        Args:
            texts: Metin listesi
            batch_size: Batch boyutu
            
        Returns:
            Embedding vektör listesi
        """
        try:
            if not self.model:
                raise Exception("Embedding modeli yüklenmemiş")
            
            embeddings = self.model.encode(texts, batch_size=batch_size)
            return embeddings.tolist()
            
        except Exception as e:
            logger.error(f"Toplu embedding oluşturma hatası: {str(e)}")
            raise Exception(f"Toplu embedding oluşturulamadı: {str(e)}")
    
    def get_model_info(self) -> dict:
        """Model bilgilerini getir"""
        if not self.model:
            return {"error": "Model yüklenmemiş"}
        
        return {
            "model_name": settings.EMBEDDING_MODEL,
            "max_seq_length": self.model.max_seq_length,
            "embedding_dimension": self.model.get_sentence_embedding_dimension()
        } 