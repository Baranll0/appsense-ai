# 🚀 AppSense Deployment Guide

This guide covers various deployment options for the AppSense application, from local development to production environments.

## 📋 Prerequisites

Before deploying, ensure you have:

- **API Keys**: Pinecone and Groq API keys
- **Domain**: A domain name for production (optional)
- **SSL Certificate**: For HTTPS in production
- **Server Resources**: Minimum 2GB RAM, 1 CPU core

## 🏠 Local Development

### Quick Start

```bash
# Clone repository
git clone https://github.com/Baranll0/appsense-ai.git
cd appsense-ai

# Backend setup
cd backend
pip install -r requirements.txt
python main.py

# Frontend setup (new terminal)
cd frontend
npm install
npm start
```

**Access URLs**:
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`

## ☁️ Cloud Deployment Options

### 1. Vercel (Frontend) + Railway (Backend)

#### Frontend Deployment on Vercel

1. **Connect to Vercel**
```bash
npm install -g vercel
vercel login
```

2. **Deploy Frontend**
```bash
cd frontend
vercel --prod
```

3. **Configure Environment Variables**
   - Go to Vercel Dashboard
   - Add environment variables:
     ```
     REACT_APP_API_URL=https://your-backend-url.railway.app
     ```

#### Backend Deployment on Railway

1. **Connect to Railway**
```bash
npm install -g @railway/cli
railway login
```

2. **Deploy Backend**
```bash
cd backend
railway init
railway up
```

3. **Configure Environment Variables**
   - Go to Railway Dashboard
   - Add environment variables:
     ```
     GROQ_API_KEY=your_groq_api_key
     PINECONE_API_KEY=your_pinecone_api_key
     PINECONE_ENVIRONMENT=gcp-starter
     ```

### 2. Heroku Deployment

#### Backend on Heroku

1. **Create Heroku App**
```bash
heroku create your-appsense-backend
```

2. **Deploy Backend**
```bash
cd backend
git init
git add .
git commit -m "Initial commit"
heroku git:remote -a your-appsense-backend
git push heroku main
```

3. **Configure Environment Variables**
```bash
heroku config:set GROQ_API_KEY=your_groq_api_key
heroku config:set PINECONE_API_KEY=your_pinecone_api_key
heroku config:set PINECONE_ENVIRONMENT=gcp-starter
```

#### Frontend on Heroku

1. **Create Buildpack**
```bash
heroku create your-appsense-frontend
heroku buildpacks:set mars/create-react-app
```

2. **Deploy Frontend**
```bash
cd frontend
git init
git add .
git commit -m "Initial commit"
heroku git:remote -a your-appsense-frontend
git push heroku main
```

### 3. Docker Deployment

#### Create Dockerfile for Backend

```dockerfile
# backend/Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Create Dockerfile for Frontend

```dockerfile
# frontend/Dockerfile
FROM node:16-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
```

#### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
      - PINECONE_API_KEY=${PINECONE_API_KEY}
      - PINECONE_ENVIRONMENT=${PINECONE_ENVIRONMENT}

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:8000
    depends_on:
      - backend
```

#### Deploy with Docker

```bash
# Build and run
docker-compose up --build

# Run in background
docker-compose up -d
```

### 4. AWS Deployment

#### EC2 Instance Setup

1. **Launch EC2 Instance**
   - Ubuntu 20.04 LTS
   - t2.micro (free tier) or t2.small
   - Security Group: Allow ports 22, 80, 443, 3000, 8000

2. **Install Dependencies**
```bash
sudo apt update
sudo apt install python3-pip nodejs npm nginx
```

3. **Deploy Backend**
```bash
cd backend
pip3 install -r requirements.txt
sudo systemctl enable appsense-backend
sudo systemctl start appsense-backend
```

4. **Deploy Frontend**
```bash
cd frontend
npm install
npm run build
sudo cp -r build/* /var/www/html/
```

5. **Configure Nginx**
```nginx
# /etc/nginx/sites-available/appsense
server {
    listen 80;
    server_name your-domain.com;

    location / {
        root /var/www/html;
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 5. Google Cloud Platform

#### App Engine Deployment

1. **Backend (Python)**
```yaml
# backend/app.yaml
runtime: python39
entrypoint: uvicorn main:app --host 0.0.0.0 --port $PORT

env_variables:
  GROQ_API_KEY: "your_groq_api_key"
  PINECONE_API_KEY: "your_pinecone_api_key"
  PINECONE_ENVIRONMENT: "gcp-starter"
```

```bash
cd backend
gcloud app deploy
```

2. **Frontend (Static)**
```bash
cd frontend
npm run build
gcloud app deploy --version frontend
```

## 🔧 Production Configuration

### Environment Variables

```env
# Production Settings
NODE_ENV=production
REACT_APP_API_URL=https://your-backend-domain.com

# Security
CORS_ORIGINS=["https://your-frontend-domain.com"]
RATE_LIMIT=100
RATE_LIMIT_WINDOW=60

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/appsense/app.log

# Database
DATABASE_URL=postgresql://user:password@localhost/appsense
```

### Security Best Practices

1. **HTTPS Only**
```nginx
# Force HTTPS
server {
    listen 80;
    return 301 https://$server_name$request_uri;
}
```

2. **Rate Limiting**
```python
# backend/middleware/rate_limit.py
from fastapi import HTTPException
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
```

3. **CORS Configuration**
```python
# backend/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Monitoring and Logging

#### Application Monitoring

```python
# backend/monitoring.py
import logging
from prometheus_client import Counter, Histogram

# Metrics
request_count = Counter('http_requests_total', 'Total HTTP requests')
request_duration = Histogram('http_request_duration_seconds', 'HTTP request duration')

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/appsense/app.log'),
        logging.StreamHandler()
    ]
)
```

#### Health Checks

```python
# backend/health.py
from fastapi import APIRouter
import psutil

router = APIRouter()

@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "memory_usage": psutil.virtual_memory().percent,
        "cpu_usage": psutil.cpu_percent(),
        "disk_usage": psutil.disk_usage('/').percent
    }
```

## 📊 Performance Optimization

### Backend Optimization

1. **Database Connection Pooling**
```python
# backend/database.py
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=30,
    pool_pre_ping=True
)
```

2. **Caching**
```python
# backend/cache.py
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="appsense-cache")
```

### Frontend Optimization

1. **Code Splitting**
```javascript
// frontend/src/components/LazyComponent.js
import React, { Suspense } from 'react';

const LazyComponent = React.lazy(() => import('./HeavyComponent'));

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <LazyComponent />
    </Suspense>
  );
}
```

2. **Service Worker**
```javascript
// frontend/public/sw.js
const CACHE_NAME = 'appsense-v1';
const urlsToCache = [
  '/',
  '/static/js/bundle.js',
  '/static/css/main.css'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});
```

## 🔄 CI/CD Pipeline

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy AppSense

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Test Backend
        run: |
          cd backend
          pip install -r requirements.txt
          python -m pytest
      - name: Test Frontend
        run: |
          cd frontend
          npm install
          npm test

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Production
        run: |
          # Your deployment commands
          echo "Deploying to production..."
```

## 🚨 Troubleshooting

### Common Issues

1. **CORS Errors**
   - Check CORS configuration
   - Verify frontend URL in backend settings
   - Clear browser cache

2. **API Key Issues**
   - Verify API keys are correct
   - Check account limits and billing
   - Ensure keys are properly set in environment

3. **Performance Issues**
   - Monitor server resources
   - Check database connection pool
   - Optimize queries and caching

### Debug Commands

```bash
# Check backend logs
tail -f /var/log/appsense/app.log

# Check system resources
htop
df -h
free -h

# Test API endpoints
curl -X GET "https://your-api-domain.com/api/v1/health"

# Check SSL certificate
openssl s_client -connect your-domain.com:443
```

## 📞 Support

For deployment issues:

1. **Check logs** for error messages
2. **Verify configuration** files
3. **Test locally** before deploying
4. **Create issue** on GitHub with details

---

**Need help with deployment?** Check the troubleshooting section or create an issue on GitHub! 