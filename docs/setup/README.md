# ⚙️ AppSense Setup Guide

This guide provides step-by-step instructions for setting up the AppSense development environment and configuring all necessary services.

## 🎯 Quick Setup

### Prerequisites Check

Before starting, ensure you have the following installed:

```bash
# Check Python version (3.8+ required)
python --version

# Check Node.js version (16+ required)
node --version

# Check npm version
npm --version

# Check Git version
git --version
```

## 🚀 Step-by-Step Setup

### 1. Repository Setup

```bash
# Clone the repository
git clone https://github.com/Baranll0/appsense-ai.git
cd appsense-ai

# Check the project structure
ls -la
```

### 2. Backend Setup

#### Python Environment

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

#### Environment Configuration

```bash
# Copy environment template
cp config/env.example .env

# Edit environment file
# On Windows:
notepad .env
# On macOS/Linux:
nano .env
```

Add your API keys to `.env`:

```env
# API Keys (Required)
GROQ_API_KEY=your_groq_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENVIRONMENT=gcp-starter

# Model Configuration (Optional)
LLM_MODEL=llama3-8b-8192
EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2

# Server Configuration (Optional)
HOST=0.0.0.0
PORT=8000

# CORS Settings (Optional)
BACKEND_CORS_ORIGINS=["http://localhost:3000", "http://127.0.0.1:3000"]
```

#### Test Backend

```bash
# Test the backend
python main.py

# In another terminal, test the API
curl http://localhost:8000/api/v1/health
```

### 3. Frontend Setup

#### Node.js Dependencies

```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
npm install

# Verify installation
npm list --depth=0
```

#### Environment Configuration

```bash
# Create environment file
echo "REACT_APP_API_URL=http://localhost:8000" > .env

# Or manually create .env file with:
# REACT_APP_API_URL=http://localhost:8000
```

#### Test Frontend

```bash
# Start development server
npm start

# The frontend should open at http://localhost:3000
```

### 4. API Keys Setup

#### Pinecone Setup

1. **Create Pinecone Account**
   - Visit [Pinecone Console](https://app.pinecone.io/)
   - Sign up for a free account
   - Verify your email

2. **Create Project**
   - Click "Create Project"
   - Enter project name: `AppSense`
   - Choose cloud provider (AWS or GCP)

3. **Create Index**
   - Click "Create Index"
   - Use these settings:
     - **Name**: `appsense`
     - **Dimensions**: `384`
     - **Metric**: `cosine`
     - **Cloud**: `AWS` or `GCP`

4. **Get API Key**
   - Go to API Keys section
   - Copy your API key
   - Add to `.env` file

#### Groq Setup

1. **Create Groq Account**
   - Visit [Groq Console](https://console.groq.com/)
   - Sign up for an account
   - Verify your email

2. **Get API Key**
   - Go to API Keys section
   - Click "Create API Key"
   - Copy the key
   - Add to `.env` file

### 5. Data Setup

#### Collect Sample Data

```bash
# Navigate to scrapers directory
cd ../data/scrapers

# Run the scraper to collect app data
python google_play_scraper_library.py

# Check the generated data
ls -la ../processed/
```

#### Prepare Embeddings

```bash
# Navigate to scripts directory
cd ../../scripts

# Run embedding preparation script
python prepare_embeddings.py

# This will create embeddings and upload to Pinecone
```

### 6. Testing the Complete Setup

#### Start Both Services

```bash
# Terminal 1: Start Backend
cd backend
python main.py

# Terminal 2: Start Frontend
cd frontend
npm start
```

#### Test the Application

1. **Open Browser**: Navigate to `http://localhost:3000`
2. **Test Search**: Try searching for "fitness app"
3. **Check API**: Visit `http://localhost:8000/docs` for API documentation

## 🔧 Configuration Options

### Backend Configuration

#### Advanced Environment Variables

```env
# Development Settings
DEBUG=True
LOG_LEVEL=DEBUG

# Production Settings
DEBUG=False
LOG_LEVEL=INFO

# Database Settings
DATABASE_URL=sqlite:///./appsense.db

# Cache Settings
REDIS_URL=redis://localhost:6379

# Security Settings
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

#### CORS Configuration

```python
# backend/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://your-frontend-domain.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Frontend Configuration

#### Environment Variables

```env
# API Configuration
REACT_APP_API_URL=http://localhost:8000
REACT_APP_API_VERSION=v1

# Feature Flags
REACT_APP_ENABLE_ANALYTICS=false
REACT_APP_ENABLE_DEBUG=true

# UI Configuration
REACT_APP_DEFAULT_LANGUAGE=en
REACT_APP_THEME=light
```

#### Tailwind Configuration

```javascript
// frontend/tailwind.config.js
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#3B82F6',
        secondary: '#06B6D4',
      },
    },
  },
  plugins: [],
}
```

## 🐛 Troubleshooting

### Common Setup Issues

#### 1. Python Dependencies Installation Failed

```bash
# Upgrade pip
pip install --upgrade pip

# Clear pip cache
pip cache purge

# Install with verbose output
pip install -r requirements.txt -v

# If still failing, try:
pip install --no-cache-dir -r requirements.txt
```

#### 2. Node.js Dependencies Installation Failed

```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# If using yarn:
yarn cache clean
rm -rf node_modules yarn.lock
yarn install
```

#### 3. Pinecone Connection Issues

```bash
# Test Pinecone connection
python -c "
import pinecone
pinecone.init(api_key='your-api-key', environment='gcp-starter')
print('Pinecone connection successful')
"
```

#### 4. Groq API Issues

```bash
# Test Groq API
python -c "
import groq
client = groq.Groq(api_key='your-api-key')
print('Groq API connection successful')
"
```

#### 5. CORS Issues

```bash
# Check if backend is running
curl http://localhost:8000/api/v1/health

# Check CORS headers
curl -H "Origin: http://localhost:3000" \
     -H "Access-Control-Request-Method: GET" \
     -H "Access-Control-Request-Headers: X-Requested-With" \
     -X OPTIONS http://localhost:8000/api/v1/search
```

### Debug Commands

#### Backend Debug

```bash
# Check Python environment
which python
pip list

# Test imports
python -c "import fastapi, pinecone, groq; print('All imports successful')"

# Check environment variables
python -c "import os; print('GROQ_API_KEY:', 'SET' if os.getenv('GROQ_API_KEY') else 'NOT SET')"
```

#### Frontend Debug

```bash
# Check Node.js environment
node --version
npm --version

# Test React build
npm run build

# Check environment variables
echo $REACT_APP_API_URL
```

## 📊 Verification Checklist

### Backend Verification

- [ ] Python virtual environment activated
- [ ] All dependencies installed (`pip list`)
- [ ] Environment variables set (`.env` file)
- [ ] Pinecone API key configured
- [ ] Groq API key configured
- [ ] Backend starts without errors (`python main.py`)
- [ ] Health endpoint responds (`curl http://localhost:8000/api/v1/health`)
- [ ] API documentation accessible (`http://localhost:8000/docs`)

### Frontend Verification

- [ ] Node.js dependencies installed (`npm list`)
- [ ] Environment variables set (`.env` file)
- [ ] Frontend starts without errors (`npm start`)
- [ ] Application loads in browser (`http://localhost:3000`)
- [ ] Search functionality works
- [ ] API calls successful (check browser network tab)

### Data Verification

- [ ] Sample data collected (`data/processed/google_play_apps_library.csv`)
- [ ] Embeddings generated (`scripts/prepare_embeddings.py`)
- [ ] Pinecone index populated
- [ ] Search returns results

## 🔄 Development Workflow

### Daily Development

```bash
# Start development environment
cd backend && python main.py &
cd frontend && npm start &

# Make changes and test
# Backend auto-reloads with uvicorn --reload
# Frontend auto-reloads with React fast refresh
```

### Testing Changes

```bash
# Test backend changes
cd backend
python -m pytest

# Test frontend changes
cd frontend
npm test

# Test complete application
# 1. Start both services
# 2. Open browser
# 3. Test search functionality
# 4. Check API responses
```

## 📚 Additional Resources

### Documentation Links

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://reactjs.org/docs/)
- [Pinecone Documentation](https://docs.pinecone.io/)
- [Groq Documentation](https://console.groq.com/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)

### Community Support

- [GitHub Issues](https://github.com/Baranll0/appsense-ai/issues)
- [GitHub Discussions](https://github.com/Baranll0/appsense-ai/discussions)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/fastapi+react)

---

**Need help with setup?** Check the troubleshooting section or create an issue on GitHub! 