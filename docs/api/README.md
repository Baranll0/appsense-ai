# 🔌 AppSense API Documentation

This document provides comprehensive API documentation for the AppSense backend services.

## 📋 Overview

The AppSense API is built with FastAPI and provides RESTful endpoints for app discovery, search, and AI-powered recommendations.

**Base URL**: `http://localhost:8000/api/v1`

## 🔐 Authentication

Currently, the API doesn't require authentication for basic operations. However, rate limiting is implemented to prevent abuse.

## 📊 Response Format

All API responses follow this standard format:

```json
{
  "query": "string",
  "results": [
    {
      "id": "string",
      "name": "string",
      "description": "string",
      "category": "string",
      "rating": "number",
      "review_count": "number",
      "download_count": "string",
      "price": "string",
      "developer": "string",
      "similarity_score": "number"
    }
  ],
  "total_found": "number",
  "processing_time": "number",
  "language_detected": "string",
  "llm_analysis": "string"
}
```

## 🚀 Endpoints

### 1. Search Applications

Search for applications using natural language queries.

**Endpoint**: `GET /search`

**Query Parameters**:
- `query` (required): Search query string
- `category` (optional): Filter by category
- `max_results` (optional): Maximum number of results (default: 10)

**Example Request**:
```bash
GET /api/v1/search?query=fitness%20app%20with%20workout%20plans&category=Fitness&max_results=5
```

**Example Response**:
```json
{
  "query": "fitness app with workout plans",
  "results": [
    {
      "id": "com.fitness.app",
      "name": "Fitness Tracker Pro",
      "description": "Comprehensive fitness app with workout plans and tracking",
      "category": "Fitness",
      "rating": 4.5,
      "review_count": 1250,
      "download_count": "1M+",
      "price": "Free",
      "developer": "Fitness Inc.",
      "similarity_score": 0.92
    }
  ],
  "total_found": 1,
  "processing_time": 0.15,
  "language_detected": "en",
  "llm_analysis": "Based on your search for a fitness app with workout plans..."
}
```

### 2. Search Applications (POST)

Search for applications using POST method with JSON body.

**Endpoint**: `POST /search`

**Request Body**:
```json
{
  "query": "string",
  "category": "string",
  "max_results": "number",
  "language": "string"
}
```

**Example Request**:
```bash
POST /api/v1/search
Content-Type: application/json

{
  "query": "note taking app with cloud sync",
  "category": "Productivity",
  "max_results": 10,
  "language": "en"
}
```

### 3. Get Categories

Retrieve available application categories.

**Endpoint**: `GET /categories`

**Example Request**:
```bash
GET /api/v1/categories
```

**Example Response**:
```json
[
  "Fitness",
  "Productivity",
  "Entertainment",
  "Education",
  "Social",
  "Games",
  "Health",
  "Travel",
  "Finance",
  "Tools"
]
```

### 4. Health Check

Check API health and status.

**Endpoint**: `GET /health`

**Example Request**:
```bash
GET /api/v1/health
```

**Example Response**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0",
  "services": {
    "pinecone": "connected",
    "groq": "available",
    "embedding_model": "loaded"
  }
}
```

## 🔍 Search Parameters

### Query Types

1. **Natural Language Queries**
   ```
   "Find me a good fitness app"
   "I need a note-taking app with cloud sync"
   "Show me popular music streaming apps"
   ```

2. **Specific Feature Queries**
   ```
   "app with offline support"
   "free app with no ads"
   "app with dark mode"
   ```

3. **Category-Based Queries**
   ```
   "fitness apps"
   "productivity tools"
   "entertainment apps"
   ```

### Category Filtering

Available categories:
- `Fitness`
- `Productivity`
- `Entertainment`
- `Education`
- `Social`
- `Games`
- `Health`
- `Travel`
- `Finance`
- `Tools`

## 🤖 AI Analysis

The API provides AI-powered analysis of search results using LLM technology.

### Analysis Features

1. **Intent Recognition**: Understands user search intent
2. **Smart Filtering**: Filters results based on relevance
3. **Personalized Recommendations**: Provides tailored suggestions
4. **Multi-language Support**: Analyzes queries in multiple languages

### Analysis Response Format

```json
{
  "llm_analysis": "Based on your search for a fitness app with workout plans, I've found several excellent options that match your needs. Here are the top recommendations...",
  "recommended_apps": [
    {
      "name": "App Name",
      "reason": "Why this app is recommended",
      "rating": 4.5,
      "features": ["feature1", "feature2"]
    }
  ],
  "additional_suggestions": "Consider also looking at...",
  "search_tips": "For better results, try searching for..."
}
```

## 📈 Rate Limiting

- **Rate Limit**: 100 requests per minute per IP
- **Burst Limit**: 10 requests per second
- **Headers**: Rate limit information is included in response headers

## 🐛 Error Handling

### Error Response Format

```json
{
  "error": "string",
  "detail": "string",
  "status_code": "number",
  "timestamp": "string"
}
```

### Common Error Codes

| Status Code | Error Type | Description |
|-------------|------------|-------------|
| 400 | Bad Request | Invalid query parameters |
| 404 | Not Found | No results found |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |

### Example Error Response

```json
{
  "error": "No results found",
  "detail": "No applications match your search criteria",
  "status_code": 404,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MAX_SEARCH_RESULTS` | Maximum results per query | 10 |
| `SIMILARITY_THRESHOLD` | Minimum similarity score | 0.7 |
| `LLM_MODEL` | Groq model name | llama3-8b-8192 |
| `EMBEDDING_MODEL` | Sentence transformer model | paraphrase-multilingual-MiniLM-L12-v2 |

## 📚 SDK Examples

### Python Example

```python
import requests

# Search for apps
response = requests.get(
    "http://localhost:8000/api/v1/search",
    params={
        "query": "fitness app with workout plans",
        "category": "Fitness",
        "max_results": 5
    }
)

data = response.json()
print(f"Found {data['total_found']} apps")
for app in data['results']:
    print(f"- {app['name']} ({app['rating']} stars)")
```

### JavaScript Example

```javascript
// Search for apps
const response = await fetch(
    'http://localhost:8000/api/v1/search?query=fitness%20app&category=Fitness'
);
const data = await response.json();

console.log(`Found ${data.total_found} apps`);
data.results.forEach(app => {
    console.log(`- ${app.name} (${app.rating} stars)`);
});
```

### cURL Example

```bash
# Search for apps
curl -X GET "http://localhost:8000/api/v1/search?query=fitness%20app&category=Fitness"

# Get categories
curl -X GET "http://localhost:8000/api/v1/categories"

# Health check
curl -X GET "http://localhost:8000/api/v1/health"
```

## 🔗 Interactive Documentation

When the backend is running, you can access interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🤝 Support

For API-related issues:

1. Check the error response for details
2. Verify your request format
3. Check rate limiting headers
4. Create an issue on GitHub with request/response examples

---

**Need help with the API?** Check the interactive documentation or create an issue on GitHub! 