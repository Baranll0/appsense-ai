"""
AppSense Dil Algılama Yardımcısı
"""

import logging
from typing import Optional
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

logger = logging.getLogger(__name__)

class LanguageDetector:
    """Dil algılama yardımcı sınıfı"""
    
    def __init__(self):
        # LangDetect için seed ayarla (tutarlılık için)
        DetectorFactory.seed = 0
        
        # Desteklenen diller
        self.supported_languages = {
            'tr': 'Türkçe',
            'en': 'İngilizce',
            'de': 'Almanca',
            'fr': 'Fransızca',
            'es': 'İspanyolca',
            'it': 'İtalyanca',
            'pt': 'Portekizce',
            'ru': 'Rusça',
            'ja': 'Japonca',
            'ko': 'Korece',
            'zh': 'Çince'
        }
    
    def detect_language(self, text: str) -> str:
        """
        Metnin dilini algıla
        
        Args:
            text: Algılanacak metin
            
        Returns:
            Dil kodu (örn: 'tr', 'en')
        """
        try:
            if not text or not text.strip():
                return 'en'  # Varsayılan dil
            
            # LangDetect ile dil algıla
            detected_lang = detect(text)
            
            # Desteklenen dil mi kontrol et
            if detected_lang in self.supported_languages:
                logger.info(f"Dil algılandı: {detected_lang} ({self.supported_languages[detected_lang]})")
                return detected_lang
            else:
                logger.warning(f"Desteklenmeyen dil algılandı: {detected_lang}, varsayılan dil kullanılıyor")
                return 'en'
                
        except LangDetectException as e:
            logger.error(f"Dil algılama hatası: {str(e)}")
            return 'en'
        except Exception as e:
            logger.error(f"Beklenmeyen dil algılama hatası: {str(e)}")
            return 'en'
    
    def get_language_name(self, lang_code: str) -> str:
        """
        Dil kodundan dil adını getir
        
        Args:
            lang_code: Dil kodu
            
        Returns:
            Dil adı
        """
        return self.supported_languages.get(lang_code, 'Bilinmeyen')
    
    def is_supported_language(self, lang_code: str) -> bool:
        """
        Dil destekleniyor mu kontrol et
        
        Args:
            lang_code: Dil kodu
            
        Returns:
            Destekleniyor mu
        """
        return lang_code in self.supported_languages
    
    def get_supported_languages(self) -> dict:
        """
        Desteklenen dilleri getir
        
        Returns:
            Dil kodu -> dil adı mapping'i
        """
        return self.supported_languages.copy()
    
    def detect_multiple_languages(self, texts: list) -> list:
        """
        Birden fazla metnin dilini algıla
        
        Args:
            texts: Metin listesi
            
        Returns:
            Dil kodları listesi
        """
        results = []
        for text in texts:
            lang_code = self.detect_language(text)
            results.append(lang_code)
        return results 