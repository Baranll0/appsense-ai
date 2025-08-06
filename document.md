Hedef: LLM + RAG tabanlı, semantik arama yapabilen bir uygulama mağazası arama motoru

1. Veri Kaynağı:
* https://github.com/JoMingyu/google-play-scraper veya https://github.com/cowboy-bebug/app-store-scraper

ile bir kaç kategori (ör: Fitness, Finance, Education) çekelim.

2. Kaggle'daki hazır datasetler. Örn: https://www.kaggle.com/datasets/lava18/google-play-store-apps

içinde: uygulama adı, açıklama, kategori, rating, review sayısı vb.

Öneri: 1000-2000 uygulamalık küçük ama çeşitli bir dataset seçmek. Hem hız hem de demo kolaylığı için yeterli olur.

2. Metin İşleme (Preprocessing): 
* Uygulama açıklamalarındaki gereksiz HTML taglarını ve emojileri temizle.
* Dilleri tespit et(ör: langdetect ile)
* Çok dilli veri varsa, tek dile (ingilizce) çevir veya çok dilli embedding modeli kullanalım.

3. Vektör Dönüşümü (Embedding):
* Model önerileri:
    Çok dilli: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
    İngilizce: all-MiniLM-L6-v2(daha hızlı)
* App açıklamalarını embeddinge çevirip vektör database yükle. Pinecone kullanacağız.

4. Retrieval (RAG)
* Kullanıcı "koşu için offline gps uygulaması" gibi bir sorgu girdiğinde sorguyu da embeddinge çevir.
Vektör veritabanında benzer uygulamaları bul.
* Bulunan sonuçları LLM'e verip daha açıklayıcı filtrelenmiş sonuçlar üret:
* Örn. "İşte koşu için offline çalışan, 4+ puan almış ve 500K+ indirme sayısına sahip 3 uygulama"

5. LLM entegrasyonu
API olarak: 
    Ücretsiz olarak: Groq Llama 3 vs.
    Yerel: llama-2, Mistral-7B-Instruct
Prompta şunları ekleyebiliriz:
    Kullanıcı sorgusu
    RAG'den gelen en alakalı 5 uygulama
    Çıktıyı "kullanıcıyıa öneri listesi formatında döndürmesi"
6. Arayüz: 
    react ile güzel bir arayüz.
    Kullanıcı dili otomatik algılanıp sonuçlar o dilde döndürülsün.
    
