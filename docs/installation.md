# 📦 AppSense Installation Guide

This document provides comprehensive installation instructions for the AppSense AI-powered app discovery engine.

## 🎯 Overview

AppSense is a modern web application that combines React frontend with FastAPI backend, using AI technologies for intelligent app recommendations.

## 📋 Prerequisites

### System Requirements
- **Operating System**: Windows 10+, macOS 10.15+, or Linux (Ubuntu 18.04+)
- **Python**: 3.8 or higher
- **Node.js**: 16.0 or higher
- **npm**: 8.0 or higher (comes with Node.js)
- **Git**: Latest version

### API Keys Required
- **Pinecone API Key**: [Get Pinecone API Key](https://www.pinecone.io/)
- **Groq API Key**: [Get Groq API Key](https://console.groq.com/)

## 🚀 Quick Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Baranll0/appsense-ai.git
cd appsense-ai
```

### 2. Backend Setup

#### Create Python Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

#### Configure Environment Variables

```bash
# Copy environment template
cp config/env.example .env

# Edit .env file with your API keys
nano .env  # or use your preferred editor
```

Add your API keys to the `.env` file:

```env
# API Keys
GROQ_API_KEY=your_groq_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENVIRONMENT=gcp-starter

# Model Configuration
LLM_MODEL=llama3-8b-8192
EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Database
DATABASE_URL=sqlite:///./appsense.db

# CORS Settings
BACKEND_CORS_ORIGINS=["http://localhost:3000", "http://127.0.0.1:3000"]
```

### 3. Frontend Setup

#### Install Node.js Dependencies

```bash
cd frontend
npm install
```

#### Verify Installation

```bash
# Check if all dependencies are installed
npm list --depth=0
```

### 4. Data Preparation

#### Collect App Data (Optional)

```bash
cd data/scrapers
python google_play_scraper_library.py
```

This will create a CSV file with app data in `data/processed/google_play_apps_library.csv`.

### 5. Start the Application

#### Start Backend Server

```bash
cd backend
python main.py
```

The backend will start on `http://localhost:8000`

#### Start Frontend Development Server

```bash
cd frontend
npm start
```

The frontend will start on `http://localhost:3000`

## 🔧 Detailed Configuration

### Pinecone Setup

1. **Create Pinecone Account**
   - Visit [Pinecone Console](https://app.pinecone.io/)
   - Sign up for a free account
   - Create a new project

2. **Create Index**
   - Go to your project dashboard
   - Click "Create Index"
   - Use these settings:
     - **Name**: `appsense`
     - **Dimensions**: `384` (for multilingual model)
     - **Metric**: `cosine`
     - **Cloud**: `AWS` or `GCP`

3. **Get API Key**
   - Copy your API key from the console
   - Add it to your `.env` file

### Groq Setup

1. **Create Groq Account**
   - Visit [Groq Console](https://console.groq.com/)
   - Sign up for an account
   - Verify your email

2. **Get API Key**
   - Go to API Keys section
   - Create a new API key
   - Copy the key and add it to your `.env` file

### Environment Variables Explained

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GROQ_API_KEY` | Groq API key for LLM services | Yes | - |
| `PINECONE_API_KEY` | Pinecone API key for vector database | Yes | - |
| `PINECONE_ENVIRONMENT` | Pinecone environment (gcp-starter, us-west1-gcp, etc.) | Yes | gcp-starter |
| `LLM_MODEL` | Groq model name | No | llama3-8b-8192 |
| `EMBEDDING_MODEL` | Sentence transformer model | No | paraphrase-multilingual-MiniLM-L12-v2 |
| `HOST` | Backend server host | No | 0.0.0.0 |
| `PORT` | Backend server port | No | 8000 |

## 🐛 Troubleshooting

### Common Issues

#### 1. Python Dependencies Installation Failed

```bash
# Upgrade pip
pip install --upgrade pip

# Install with verbose output
pip install -r requirements.txt -v
```

#### 2. Node.js Dependencies Installation Failed

```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

#### 3. Pinecone Connection Error

- Verify your API key is correct
- Check if your index exists
- Ensure you're using the correct environment

#### 4. Groq API Error

- Verify your API key is valid
- Check your account has sufficient credits
- Ensure you're using a supported model

#### 5. CORS Errors

- Make sure backend is running on port 8000
- Check CORS settings in `.env` file
- Verify frontend is running on port 3000

### Performance Optimization

#### For Development
```bash
# Backend with auto-reload
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Frontend with fast refresh
cd frontend
npm start
```

#### For Production
```bash
# Backend with multiple workers
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# Frontend build
cd frontend
npm run build
```

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://reactjs.org/docs/)
- [Pinecone Documentation](https://docs.pinecone.io/)
- [Groq Documentation](https://console.groq.com/docs)

## 🤝 Support

If you encounter any issues during installation:

1. **Check the troubleshooting section above**
2. **Search existing issues** on [GitHub Issues](https://github.com/Baranll0/appsense-ai/issues)
3. **Create a new issue** with detailed error information
4. **Join our discussions** on [GitHub Discussions](https://github.com/Baranll0/appsense-ai/discussions)

---

**Need help?** Feel free to reach out to the community or create an issue on GitHub! 