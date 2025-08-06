"""
AppSense LLM Service
"""

import logging
from typing import List, Dict, Any
import groq
from core.config import settings
from utils.language_detector import LanguageDetector
import json

logger = logging.getLogger(__name__)

class LLMService:
    """LLM servisi - Groq entegrasyonu"""

    def __init__(self):
        self.client = None
        self.language_detector = LanguageDetector()
        self._initialize_groq()

    def _initialize_groq(self):
        """Groq client'ını başlat"""
        try:
            if not settings.GROQ_API_KEY:
                logger.warning("Groq API key bulunamadı")
                return
            self.client = groq.Groq(api_key=settings.GROQ_API_KEY)
            logger.info("Groq client başarıyla başlatıldı")
        except Exception as e:
            logger.error(f"Groq başlatma hatası: {str(e)}")
            self.client = None

    async def analyze_search_results(
        self,
        query: str,
        search_results: List[Dict[str, Any]],
        detected_language: str = "tr"
    ) -> str:
        """
        Arama sonuçlarını LLM ile analiz edip geliştirilmiş öneri döndürür.
        0 puanlı veya 4.0 altındaki uygulamalar filtrelenir.
        """
        if not self.client:
            logger.warning("Groq client bulunamadı, analiz yapılamıyor")
            return "LLM analizi mevcut değil."

        try:
            # Dil algılama
            if not detected_language or detected_language == "auto":
                detected_language = self.language_detector.detect_language(query)

            # 4.0 altı veya 0 puanlı uygulamaları filtrele
            filtered_results = [
                r for r in search_results
                if (r.get('rating') or 0) >= 4.0
            ]

            if not filtered_results:
                return "Uygun kriterlerde (puanı 4.0 ve üzeri) uygulama bulunamadı."

            # Arama sonuçlarını formatla
            formatted_results = []
            for i, result in enumerate(filtered_results[:10], 1):
                rating = result.get('rating', 0)
                download_count = result.get('download_count', 'Bilinmeyen')
                formatted_results.append(
                    f"{i}. {result.get('name', 'Bilinmeyen')} "
                    f"({result.get('category', 'Bilinmeyen')}) - "
                    f"Puan: {rating:.1f} - İndirme: {download_count}"
                )

            # Kullanıcı prompt'u
            if detected_language == "tr":
                prompt = f"""
Kullanıcı sorgusu: "{query}"

Bulunan uygulamalar (puanı 4.0 ve üzeri):
{chr(10).join(formatted_results)}

Görevin:
1. Kullanıcının ihtiyacını analiz et ve sorgunun gerçek amacını belirle.
2. Sadece puanı 4.0 veya üzeri olan uygulamaları değerlendir (puanı 0 veya 'Bilinmeyen' olanları asla listeleme).
3. Kullanıcının ihtiyacına EN UYGUN 3-4 uygulamayı seç ve numaralandır.
4. Her uygulama için:
   - Adı
   - Kategori
   - Puan
   - İndirme sayısı
   - 1-2 cümlelik kısa açıklama
5. Neden bu uygulamaları seçtiğini açıkla (kategori uyumu, yüksek puan, yüksek indirme sayısı, offline çalışma vb.).
6. Ek öneriler kısmında:
   - Alternatif kategorilerden veya ek özellikleri olan uygulamalardan bahset.
   - Kullanıcının deneyimini geliştirecek ipuçları ver.
7. Empatik bir cümle ile başla (örn. "Evet sizi anlıyorum, bu önemli bir konu...").
8. Yanıtı Türkçe yaz, düzenli paragraflar ve madde işaretleri kullan.
9. Yanıtı tam olarak bitir, asla yarım bırakma.
"""
            else:
                prompt = f"""
User query: "{query}"

Found applications (rating 4.0 and above):
{chr(10).join(formatted_results)}

Your task:
1. Analyze the user's real intent.
2. Only consider apps with a rating of 4.0 or higher (never list apps with rating 0 or unknown).
3. Select the 3-4 MOST relevant apps and number them.
4. For each app, include:
   - Name
   - Category
   - Rating
   - Download count
   - 1-2 sentence short description
5. Explain why you chose these apps (category match, high rating, high downloads, offline support, etc.).
6. In the additional suggestions section:
   - Mention alternative categories or apps with extra features.
   - Give tips to enhance the user's experience.
7. Start with an empathetic sentence.
8. Respond in the query's language, using bullet points and structured paragraphs.
9. Fully complete your answer, never leave it unfinished.
"""

            # LLM çağrısı
            response = self.client.chat.completions.create(
                model=settings.LLM_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": """
Sen AppSense uygulama mağazası asistanısın.
Görevin: Kullanıcının ihtiyacını doğru anlayarak ona en uygun uygulamaları profesyonel, empatik ve düzenli formatta sunmak.

Kurallar:
1. Düzenli, madde işaretli format kullan.
2. Empatik girişle başla.
3. Kullanıcının sorgu dilinde yaz.
4. Gereksiz tekrar ve uzun cümlelerden kaçın.
5. Yanıtı tam olarak bitir, asla yarım bırakma.
"""
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )

            enhanced_response = response.choices[0].message.content
            logger.info(f"LLM analizi: {enhanced_response}")
            return enhanced_response

        except Exception as e:
            logger.error(f"LLM yanıt oluşturma hatası: {str(e)}")
            return "LLM analizi sırasında hata oluştu."

    def _format_simple_response(self, search_results: List[Dict[str, Any]]) -> str:
        """Basit yanıt formatla"""
        if not search_results:
            return "Aradığınız kriterlere uygun uygulama bulunamadı."

        response = "Bulunan uygulamalar:\n\n"
        for i, result in enumerate(search_results[:5], 1):
            response += f"{i}. {result.get('name', 'Bilinmeyen')}\n"
            response += f"   Kategori: {result.get('category', 'Bilinmeyen')}\n"
            response += f"   Puan: {result.get('score', 0):.2f}\n\n"

        return response

    async def generate_app_description(self, app_data: Dict[str, Any]) -> str:
        """Uygulama için açıklayıcı metin oluştur"""
        if not self.client:
            return app_data.get('description', '')

        try:
            prompt = f"""
Aşağıdaki bilgileri kullanarak bu uygulama için kısa, çekici ve kullanıcı dostu bir tanıtım metni oluştur.

Uygulama Adı: {app_data.get('name', '')}
Kategori: {app_data.get('category', '')}
Mevcut Açıklama: {app_data.get('description', '')}
Geliştirici: {app_data.get('developer', '')}
Puan: {app_data.get('rating', 'N/A')}

Kurallar:
1. Maksimum 3-4 cümle yaz.
2. Uygulamanın en önemli özelliklerini vurgula.
3. Akıcı ve anlaşılır ol.
4. Kullanıcının dilinde yaz.
5. Teknik terimlerden kaçın.
6. Yanıtı tam olarak bitir.
"""
            response = self.client.chat.completions.create(
                model=settings.LLM_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "Sen AppSense uygulama mağazası asistanısın. Uygulama açıklamalarını kısa, çekici ve kullanıcı dostu yaz."
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()

        except Exception as e:
            logger.error(f"Açıklama oluşturma hatası: {str(e)}")
            return app_data.get('description', '')

    async def get_search_suggestions(self, query: str) -> List[str]:
        """Arama önerileri oluştur"""
        if not self.client:
            return []

        try:
            prompt = f"""
Bu arama sorgusu için 3 farklı ve ilgili öneri oluştur.

Sorgu: "{query}"

Kurallar:
1. Kullanıcının amacına uygun olsun.
2. Yaratıcı ve çeşitli olsun.
3. Kullanıcının dilinde yaz.
4. JSON formatında döndür:
{{"suggestions": ["öneri1", "öneri2", "öneri3"]}}
5. Yanıtı tam olarak bitir.
"""
            response = self.client.chat.completions.create(
                model=settings.LLM_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "Sen AppSense uygulama mağazası asistanısın. Kullanıcı sorgusuna uygun öneriler üret."
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.7
            )

            start_idx = response.choices[0].message.content.find('{')
            end_idx = response.choices[0].message.content.rfind('}') + 1

            if start_idx != -1 and end_idx != 0:
                json_str = response.choices[0].message.content[start_idx:end_idx]
                parsed = json.loads(json_str)
                return parsed.get('suggestions', [])
            return []

        except Exception as e:
            logger.error(f"Öneri oluşturma hatası: {str(e)}")
            return []
