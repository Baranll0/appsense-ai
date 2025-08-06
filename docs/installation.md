# AppSense Kurulum Talimatları

Bu doküman AppSense projesinin kurulum adımlarını açıklar.

## Gereksinimler

- Python 3.8+
- Node.js 16+
- npm veya yarn
- Pinecone hesabı
- Groq API anahtarı (opsiyonel)

## 1. Proje Klonlama

```bash
git clone <repository-url>
cd AppSense
```

## 2. Backend Kurulumu

### Python Sanal Ortam Oluşturma

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Bağımlılıkları Yükleme

```bash
cd backend
pip install -r requirements.txt
```

### Environment Dosyası Oluşturma

```bash
# config/env.example dosyasını kopyala
cp config/env.example backend/.env

# .env dosyasını düzenle
# Pinecone ve Groq API anahtarlarını ekle
```

### Pinecone Kurulumu

1. [Pinecone](https://www.pinecone.io/) hesabı oluşturun
2. API anahtarınızı alın
3. Environment dosyasına ekleyin:
   ```
   PINECONE_API_KEY=your_api_key_here
   PINECONE_ENVIRONMENT=your_environment_here
   ```

### Groq Kurulumu (Opsiyonel)

1. [Groq](https://console.groq.com/) hesabı oluşturun
2. API anahtarınızı alın
3. Environment dosyasına ekleyin:
   ```
   GROQ_API_KEY=your_api_key_here
   ```

## 3. Frontend Kurulumu

### Bağımlılıkları Yükleme

```bash
cd frontend
npm install
```

### Tailwind CSS Kurulumu

```bash
npx tailwindcss init
```

## 4. Veri Hazırlama

### Örnek Veri Oluşturma

```bash
cd scripts
python create_sample_data.py
```

## 5. Uygulamayı Çalıştırma

### Backend'i Başlatma

```bash
cd backend
python main.py
```

Backend http://localhost:8000 adresinde çalışacak.

### Frontend'i Başlatma

```bash
cd frontend
npm start
```

Frontend http://localhost:3000 adresinde çalışacak.

## 6. API Dokümantasyonu

Backend çalıştıktan sonra API dokümantasyonuna şu adresten erişebilirsiniz:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 7. Test Etme

### Backend Testleri

```bash
cd backend
pytest
```

### Frontend Testleri

```bash
cd frontend
npm test
```

## Sorun Giderme

### Pinecone Bağlantı Sorunu

- API anahtarının doğru olduğundan emin olun
- Environment değerinin doğru olduğunu kontrol edin
- Pinecone hesabınızın aktif olduğunu kontrol edin

### Embedding Model Yükleme Sorunu

- İnternet bağlantınızı kontrol edin
- Model dosyalarının indirilmesi biraz zaman alabilir
- Disk alanınızın yeterli olduğundan emin olun

### Frontend Build Sorunu

- Node.js sürümünüzün güncel olduğundan emin olun
- npm cache'ini temizleyin: `npm cache clean --force`
- node_modules klasörünü silip yeniden yükleyin

## Geliştirme Ortamı

### VS Code Önerilen Eklentiler

- Python
- TypeScript and JavaScript
- Tailwind CSS IntelliSense
- Auto Rename Tag
- Bracket Pair Colorizer

### Debug Ayarları

Backend için `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/backend/main.py",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}/backend"
        }
    ]
}
```

## Deployment

### Docker ile Deployment

```bash
# Docker image oluştur
docker build -t appsense .

# Container çalıştır
docker run -p 8000:8000 appsense
```

### Production Ayarları

Production ortamında şu ayarları yapın:

1. Environment değişkenlerini production değerleriyle güncelleyin
2. CORS ayarlarını production domain'lerine göre düzenleyin
3. Logging seviyesini INFO veya WARNING'e ayarlayın
4. SSL sertifikası ekleyin
5. Rate limiting ekleyin

## Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. 