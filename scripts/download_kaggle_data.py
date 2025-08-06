"""
Kaggle'dan Google Play Store verisi indirme scripti
"""

import os
import pandas as pd
import requests
import zipfile
from pathlib import Path
import logging

# Logging ayarları
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_kaggle_dataset():
    """Kaggle'dan Google Play Store verisi indir"""
    
    # Kaggle dataset URL'leri
    datasets = {
        'google_play_store': {
            'url': 'https://www.kaggle.com/api/v1/datasets/download/lava18/google-play-store-apps',
            'filename': 'google-play-store-apps.zip'
        }
    }
    
    # Data klasörünü oluştur
    data_dir = Path('../data/raw')
    data_dir.mkdir(parents=True, exist_ok=True)
    
    for dataset_name, dataset_info in datasets.items():
        try:
            logger.info(f"{dataset_name} verisi indiriliyor...")
            
            # Dosya yolu
            zip_path = data_dir / dataset_info['filename']
            
            # Eğer dosya zaten varsa, tekrar indirme
            if zip_path.exists():
                logger.info(f"{zip_path} zaten mevcut, indirme atlanıyor.")
                continue
            
            # Veriyi indir
            response = requests.get(dataset_info['url'], stream=True)
            response.raise_for_status()
            
            with open(zip_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            logger.info(f"{dataset_name} başarıyla indirildi: {zip_path}")
            
            # ZIP dosyasını çıkart
            extract_zip(zip_path, data_dir)
            
        except Exception as e:
            logger.error(f"{dataset_name} indirme hatası: {str(e)}")
            continue

def extract_zip(zip_path: Path, extract_dir: Path):
    """ZIP dosyasını çıkart"""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        logger.info(f"ZIP dosyası çıkartıldı: {extract_dir}")
    except Exception as e:
        logger.error(f"ZIP çıkartma hatası: {str(e)}")

def process_google_play_data():
    """Google Play Store verisini işle"""
    try:
        # Veri dosyasını oku
        data_path = Path('../data/raw/googleplaystore.csv')
        
        if not data_path.exists():
            logger.error("Google Play Store veri dosyası bulunamadı!")
            return None
        
        logger.info("Google Play Store verisi okunuyor...")
        df = pd.read_csv(data_path)
        
        # Veri hakkında bilgi
        logger.info(f"Toplam uygulama sayısı: {len(df)}")
        logger.info(f"Sütunlar: {list(df.columns)}")
        
        # Kategorileri ve uygulama sayılarını yazdır
        category_counts = df['Category'].value_counts()
        logger.info("Kategoriler ve uygulama sayıları:")
        for cat, count in category_counts.items():
            print(f"{cat}: {count}")
        
        # İlk birkaç satırı göster
        logger.info("İlk 5 satır:")
        print(df.head())
        
        return df
        
    except Exception as e:
        logger.error(f"Veri işleme hatası: {str(e)}")
        return None

def create_sample_dataset(df: pd.DataFrame, sample_size: int = 2000):
    """Seçili kategorilerden örnek dataset oluştur"""
    try:
        # Seçili kategoriler
        selected_categories = [
            'FAMILY', 'GAME', 'TOOLS', 'PRODUCTIVITY', 
            'FINANCE', 'HEALTH_AND_FITNESS', 'EDUCATION', 'ENTERTAINMENT'
        ]
        
        # Her kategoriden kaç uygulama alacağımızı hesapla
        apps_per_category = sample_size // len(selected_categories)
        
        sample_data = []
        for category in selected_categories:
            category_df = df[df['Category'] == category]
            if len(category_df) > 0:
                # Her kategoriden maksimum apps_per_category kadar al
                category_sample = category_df.sample(
                    n=min(apps_per_category, len(category_df)),
                    random_state=42
                )
                sample_data.append(category_sample)
                logger.info(f"{category}: {len(category_sample)} uygulama seçildi")
            else:
                logger.warning(f"{category} kategorisinde uygulama bulunamadı")
        
        # Tüm örnekleri birleştir
        sample_df = pd.concat(sample_data, ignore_index=True)
        
        # Processed klasörüne kaydet
        processed_dir = Path('../data/processed')
        processed_dir.mkdir(parents=True, exist_ok=True)
        
        output_path = processed_dir / 'sample_apps.csv'
        sample_df.to_csv(output_path, index=False)
        
        logger.info(f"Örnek dataset oluşturuldu: {len(sample_df)} uygulama")
        logger.info(f"Kaydedildi: {output_path}")
        
        return sample_df
        
    except Exception as e:
        logger.error(f"Örnek dataset oluşturma hatası: {str(e)}")
        return None

if __name__ == "__main__":
    logger.info("Kaggle veri indirme işlemi başlıyor...")
    
    # Veriyi indir
    download_kaggle_dataset()
    
    # Veriyi işle
    df = process_google_play_data()
    
    if df is not None:
        # Örnek dataset oluştur
        sample_df = create_sample_dataset(df, sample_size=2000)
        
        if sample_df is not None:
            logger.info("Veri hazırlama tamamlandı!")
        else:
            logger.error("Örnek dataset oluşturulamadı!")
    else:
        logger.error("Veri işleme başarısız!") 