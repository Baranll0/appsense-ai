"""
AppSense Embedding Hazırlama Scripti
Veri temizleme, embedding oluşturma ve Pinecone'a yükleme
"""

import pandas as pd
import numpy as np
import logging
import re
from pathlib import Path
import sys
import os

# Backend klasörünü Python path'ine ekle
sys.path.append(str(Path(__file__).parent.parent / 'backend'))

from models.embeddings.embedding_model import EmbeddingModel
from models.vectorstore.pinecone_store import PineconeStore
from utils.language_detector import LanguageDetector
from core.config import settings

# Logging ayarları
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def clean_text(text):
    """Metni temizle"""
    if pd.isna(text) or text == '':
        return ''
    
    # HTML taglarını temizle
    text = re.sub(r'<[^>]+>', '', str(text))
    
    # Özel karakterleri temizle
    text = re.sub(r'[^\w\s\.\,\!\?\-]', '', text)
    
    # Fazla boşlukları temizle
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def prepare_app_data(df):
    """Uygulama verilerini hazırla"""
    logger.info("Uygulama verileri hazırlanıyor...")
    
    # Eksik değerleri temizle
    df = df.dropna(subset=['App', 'Category'])
    
    # Metin alanlarını temizle
    df['App'] = df['App'].apply(clean_text)
    df['Category'] = df['Category'].apply(clean_text)
    
    # Description oluştur (App adı + Category + diğer bilgiler)
    def create_description(row):
        desc_parts = []
        
        if row['App']:
            desc_parts.append(f"App: {row['App']}")
        
        if row['Category']:
            desc_parts.append(f"Category: {row['Category']}")
        
        if pd.notna(row['Rating']):
            desc_parts.append(f"Rating: {row['Rating']}")
        
        if pd.notna(row['Reviews']) and row['Reviews'] > 0:
            desc_parts.append(f"Reviews: {row['Reviews']}")
        
        if pd.notna(row['Installs']):
            desc_parts.append(f"Installs: {row['Installs']}")
        
        if pd.notna(row['Type']):
            desc_parts.append(f"Type: {row['Type']}")
        
        if pd.notna(row['Price']):
            desc_parts.append(f"Price: {row['Price']}")
        
        return ' | '.join(desc_parts)
    
    df['description'] = df.apply(create_description, axis=1)
    
    # Unique ID oluştur
    df['id'] = df['App'].str.lower().str.replace(' ', '-').str.replace('[^\w\-]', '') + '-' + df.index.astype(str)
    
    logger.info(f"Veri hazırlama tamamlandı: {len(df)} uygulama")
    return df

def create_embeddings(df, embedding_model):
    """Embedding'leri oluştur"""
    logger.info("Embedding'ler oluşturuluyor...")
    
    # Açıklamaları embedding'e çevir
    descriptions = df['description'].tolist()
    
    try:
        embeddings = embedding_model.encode(descriptions)
        logger.info(f"Embedding'ler oluşturuldu: {len(embeddings)} vektör")
        return embeddings
    except Exception as e:
        logger.error(f"Embedding oluşturma hatası: {str(e)}")
        return None

async def upload_to_pinecone(df, embeddings, pinecone_store):
    """Pinecone'a yükle"""
    logger.info("Pinecone'a yükleniyor...")
    
    try:
        # Veriyi Pinecone formatına çevir
        apps_data = []
        for i, (_, row) in enumerate(df.iterrows()):
            # NaN değerleri temizle
            rating = row.get('Rating')
            if pd.isna(rating):
                rating = 0.0
            
            review_count = row.get('Reviews')
            if pd.isna(review_count):
                review_count = 0
            
            download_count = row.get('Installs')
            if pd.isna(download_count):
                download_count = '0'
            
            price = row.get('Price')
            if pd.isna(price):
                price = 'Ücretsiz'
            
            # ID'yi ASCII karakterlere çevir
            app_id = str(row['id'])
            # Türkçe karakterleri ve özel karakterleri temizle
            import re
            app_id = re.sub(r'[^a-zA-Z0-9\-_]', '-', app_id)
            app_id = re.sub(r'-+', '-', app_id)  # Birden fazla tire'yi tek tire yap
            app_id = app_id.strip('-')  # Baş ve sondaki tire'leri kaldır
            
            app_data = {
                'id': app_id,
                'name': str(row['App']),
                'description': str(row['description']),
                'category': str(row['Category']),
                'rating': float(rating),
                'review_count': int(review_count),
                'download_count': str(download_count),
                'price': str(price),
                'developer': 'Unknown',  # Veri setinde developer bilgisi yok
                'embedding': embeddings[i] if embeddings else None
            }
            apps_data.append(app_data)
        
        # Verileri küçük parçalar halinde yükle (Pinecone 2MB limit)
        batch_size = 100  # Her seferde 100 uygulama
        total_uploaded = 0
        
        for i in range(0, len(apps_data), batch_size):
            batch = apps_data[i:i + batch_size]
            logger.info(f"Batch {i//batch_size + 1} yükleniyor: {len(batch)} uygulama")
            
            success = await pinecone_store.upsert_apps(batch)
            if success:
                total_uploaded += len(batch)
                logger.info(f"Batch {i//batch_size + 1} başarıyla yüklendi")
            else:
                logger.error(f"Batch {i//batch_size + 1} yükleme başarısız")
                return False
        
        if total_uploaded == len(apps_data):
            logger.info(f"Pinecone'a başarıyla yüklendi: {total_uploaded} uygulama")
            return True
        else:
            logger.error(f"Yükleme tamamlanamadı: {total_uploaded}/{len(apps_data)}")
            return False
            
    except Exception as e:
        logger.error(f"Pinecone yükleme hatası: {str(e)}")
        return False

async def main():
    """Ana fonksiyon"""
    logger.info("AppSense Embedding Hazırlama başlıyor...")
    
    try:
        # Veri dosyasını oku
        data_path = Path('../data/processed/sample_apps.csv')
        if not data_path.exists():
            logger.error("Veri dosyası bulunamadı!")
            return False
        
        logger.info("Veri dosyası okunuyor...")
        df = pd.read_csv(data_path)
        logger.info(f"Veri yüklendi: {len(df)} uygulama")
        
        # Veriyi hazırla
        df = prepare_app_data(df)
        
        # Embedding modelini yükle
        logger.info("Embedding modeli yükleniyor...")
        embedding_model = EmbeddingModel()
        
        # Embedding'leri oluştur
        embeddings = create_embeddings(df, embedding_model)
        if not embeddings:
            logger.error("Embedding oluşturulamadı!")
            return False
        
        # Pinecone'u başlat
        logger.info("Pinecone başlatılıyor...")
        pinecone_store = PineconeStore()
        
        # Pinecone'a yükle
        success = await upload_to_pinecone(df, embeddings, pinecone_store)
        
        if success:
            logger.info("✅ Embedding hazırlama başarıyla tamamlandı!")
            return True
        else:
            logger.error("❌ Pinecone'a yükleme başarısız!")
            return False
            
    except Exception as e:
        logger.error(f"Genel hata: {str(e)}")
        return False

if __name__ == "__main__":
    import asyncio
    success = asyncio.run(main())
    if success:
        print("\n🎉 Embedding hazırlama tamamlandı!")
        print("Artık arama sistemi kullanıma hazır!")
    else:
        print("\n❌ Embedding hazırlama başarısız!")
        print("Hata loglarını kontrol edin.") 