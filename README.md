# 🚀 AppSense - AI-Powered App Discovery Engine

> Semantic search with LLM + RAG technology for intelligent app recommendations

*"Is there an app that does this?"*

![Think](https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExbWhtZTJmdHA5bzdnc3FybnNrbnl4dGthbjg4MW93Z29reXYzdmpqNiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/y3QOvy7xxMwKI/giphy.gif)

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![React](https://img.shields.io/badge/React-18+-blue.svg)](https://reactjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

AppSense is an intelligent app discovery platform that uses advanced AI technologies to help users find the perfect applications. With semantic search capabilities and LLM-powered recommendations, it provides a modern, user-friendly experience for discovering apps across multiple categories.

## ✨ Features

- **🤖 AI-Powered Search**: LLM + RAG technology for intelligent recommendations
- **🔍 Semantic Search**: Natural language processing for better results
- **🌍 Multi-Language Support**: Automatic language detection and responses
- **⚡ Real-time Analysis**: Instant AI-powered app analysis
- **📱 Modern UI**: React-based user-friendly interface
- **🔗 Vector Database**: Pinecone for fast similarity search
- **🎯 Smart Filtering**: Category-based and rating-based filtering
- **📊 Rich Data**: Comprehensive app information and statistics

## 🛠️ Tech Stack

### Backend
- **Python 3.8+** - Core programming language
- **FastAPI** - Modern, fast web framework
- **Pinecone** - Vector database for similarity search
- **Groq LLM** - High-performance language model
- **Sentence Transformers** - Embedding generation
- **Pydantic** - Data validation and settings management

### Frontend
- **React 18** - Modern UI framework
- **TypeScript** - Type safety and better development experience
- **Tailwind CSS** - Utility-first CSS framework
- **React Router** - Client-side routing
- **Axios** - HTTP client for API calls

## 📁 Project Structure

```
AppSense/
├── backend/                 # Python FastAPI backend
│   ├── api/                # API routes and endpoints
│   ├── core/               # Configuration and settings
│   ├── models/             # Data models and schemas
│   ├── services/           # Business logic and services
│   └── utils/              # Utility functions
├── frontend/               # React frontend application
│   ├── src/
│   │   ├── components/     # Reusable React components
│   │   ├── pages/          # Page components
│   │   ├── types/          # TypeScript type definitions
│   │   └── utils/          # Frontend utilities
│   └── public/             # Static assets
├── data/                   # Data collection and processing
│   ├── processed/          # Processed datasets
│   └── scrapers/           # Data collection scripts
├── scripts/                # Utility and automation scripts
├── docs/                   # Documentation
└── config/                 # Configuration files
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** - [Download Python](https://python.org/downloads/)
- **Node.js 16+** - [Download Node.js](https://nodejs.org/)
- **Pinecone API Key** - [Get Pinecone API Key](https://www.pinecone.io/)
- **Groq API Key** - [Get Groq API Key](https://console.groq.com/)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Baranll0/appsense-ai.git
cd appsense-ai
```

2. **Backend Setup**
```bash
cd backend
pip install -r requirements.txt
```

3. **Frontend Setup**
```bash
cd frontend
npm install
```

4. **Environment Configuration**
```bash
# Copy environment template
cp config/env.example .env

# Edit .env file with your API keys
GROQ_API_KEY=your_groq_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENVIRONMENT=your_pinecone_environment
```

5. **Run the Application**
```bash
# Start Backend (Terminal 1)
cd backend
python main.py

# Start Frontend (Terminal 2)
cd frontend
npm start
```

Visit `http://localhost:3000` to use the application.

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

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

### API Endpoints

- `GET /api/v1/search` - Search applications
- `GET /api/v1/categories` - Get available categories
- `GET /api/v1/health` - Health check

## 📊 Data Collection

The project includes scripts for collecting app data from Google Play Store:

```bash
cd data/scrapers
python google_play_scraper_library.py
```

This will collect app data and save it to `data/processed/google_play_apps_library.csv`.

## 🎯 Usage Examples

### Search for Fitness Apps
```
"Find me a good fitness app with workout plans"
```

### Search for Productivity Tools
```
"I need a note-taking app with cloud sync"
```

### Search for Entertainment
```
"Show me popular music streaming apps"
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 for Python code
- Use TypeScript for frontend development
- Write meaningful commit messages
- Add tests for new features
- Update documentation as needed

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Google Play Scraper](https://github.com/JoMingyu/google-play-scraper) - Data collection library
- [Pinecone](https://www.pinecone.io/) - Vector database service
- [Groq](https://groq.com/) - High-performance LLM services
- [Sentence Transformers](https://www.sbert.net/) - Embedding models
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [React](https://reactjs.org/) - UI library

## 📞 Contact & Support

- **Repository**: [https://github.com/Baranll0/appsense-ai](https://github.com/Baranll0/appsense-ai)
- **Issues**: [https://github.com/Baranll0/appsense-ai/issues](https://github.com/Baranll0/appsense-ai/issues)
- **Discussions**: [https://github.com/Baranll0/appsense-ai/discussions](https://github.com/Baranll0/appsense-ai/discussions)

## 🚀 Roadmap

- [ ] Mobile app development
- [ ] Advanced filtering options
- [ ] User reviews and ratings
- [ ] App comparison feature
- [ ] Personalized recommendations
- [ ] Dark mode support
- [ ] Multi-language UI
- [ ] Advanced analytics dashboard

---

⭐ **If you find this project helpful, please give it a star!**

Made with ❤️ by [Baranll0](https://github.com/Baranll0)