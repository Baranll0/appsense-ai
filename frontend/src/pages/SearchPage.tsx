import React, { useState } from 'react';
import { Search, Filter, Star, Download, Globe } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

interface AppResult {
  id: string;
  name: string;
  description: string;
  category: string;
  rating?: number;
  review_count?: number;
  download_count?: string;
  price?: string;
  developer: string;
  similarity_score: number;
}

interface SearchResponse {
  query: string;
  results: AppResult[];
  total_found: number;
  processing_time: number;
  language_detected: string;
  llm_analysis?: string;
}

const SearchPage: React.FC = () => {
  const [query, setQuery] = useState('');
  const [category, setCategory] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState<AppResult[]>([]);
  const [llmAnalysis, setLlmAnalysis] = useState<string>('');

  const categories = [
    'Tümü', 'Fitness', 'Finance', 'Education', 'Entertainment',
    'Productivity', 'Social', 'Games', 'Health', 'Travel'
  ];

  const handleSearch = async () => {
    if (!query.trim()) return;

    setIsLoading(true);
    try {
      // Gerçek API çağrısı
      const response = await fetch(`/api/v1/search?query=${encodeURIComponent(query)}&category=${encodeURIComponent(category)}`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data: SearchResponse = await response.json();
      setResults(data.results || []);
      setLlmAnalysis(data.llm_analysis || '');
    } catch (error) {
      console.error('Arama hatası:', error);
      // Hata durumunda boş sonuç göster
      setResults([]);
      setLlmAnalysis('');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Arama Formu */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h1 className="text-3xl font-bold text-gray-800 mb-6">
          Uygulama Ara
        </h1>
        
        <div className="space-y-4">
          {/* Arama Kutusu */}
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Örn: Koşu için offline GPS uygulaması..."
              className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
            />
          </div>

          {/* Filtreler */}
          <div className="flex flex-wrap gap-4 items-center">
            <div className="flex items-center space-x-2">
              <Filter className="w-4 h-4 text-gray-500" />
              <span className="text-sm font-medium text-gray-700">Kategori:</span>
            </div>
            <select
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              {categories.map((cat) => (
                <option key={cat} value={cat === 'Tümü' ? '' : cat}>
                  {cat}
                </option>
              ))}
            </select>
          </div>

          {/* Arama Butonu */}
          <button
            onClick={handleSearch}
            disabled={isLoading || !query.trim()}
            className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-3 rounded-lg font-semibold hover:shadow-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
          >
            {isLoading ? (
              <>
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                <span>Aranıyor...</span>
              </>
            ) : (
              <>
                <Search className="w-5 h-5" />
                <span>Ara</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* LLM Analizi */}
      {llmAnalysis && (
        <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-xl shadow-lg p-6 border-l-4 border-purple-500">
          <h3 className="text-lg font-semibold text-gray-800 mb-3 flex items-center">
            <span className="mr-2">🤖</span>
            AI Analizi
          </h3>
          <div className="text-gray-700 leading-relaxed prose prose-sm max-w-none">
            <ReactMarkdown>
              {llmAnalysis}
            </ReactMarkdown>
          </div>
        </div>
      )}

      {/* Sonuçlar */}
      {results.length > 0 && (
        <div className="space-y-4">
          <h2 className="text-xl font-semibold text-gray-800">
            {results.length} sonuç bulundu
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {results.map((app) => (
              <div key={app.id} className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h3 className="text-lg font-semibold text-gray-800 mb-1">
                      {app.name}
                    </h3>
                    <p className="text-sm text-gray-500">{app.developer}</p>
                  </div>
                  <div className="flex items-center space-x-1">
                    <Star className="w-4 h-4 text-yellow-400 fill-current" />
                    <span className="text-sm font-medium">{app.rating}</span>
                  </div>
                </div>

                <p className="text-gray-600 text-sm mb-4 line-clamp-3">
                  {app.description}
                </p>

                <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
                  <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs">
                    {app.category}
                  </span>
                  <div className="flex items-center space-x-1">
                    <Download className="w-4 h-4" />
                    <span>{app.download_count}</span>
                  </div>
                </div>

                <div className="flex items-center justify-between">
                  <span className="text-green-600 font-medium">{app.price}</span>
                  <div className="flex items-center space-x-1 text-xs text-gray-500">
                    <Globe className="w-3 h-3" />
                    <span>%{Math.round(app.similarity_score * 100)} eşleşme</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Örnek Sorgular */}
      {results.length === 0 && !isLoading && (
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">
            Örnek Arama Sorguları
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {[
              'Fitness için kalori takip uygulaması',
              'Offline çalışan GPS navigasyon',
              'Bütçe yönetimi ve tasarruf uygulaması',
              'İngilizce öğrenme için oyun',
              'Sosyal medya fotoğraf düzenleme'
            ].map((example, index) => (
              <button
                key={index}
                onClick={() => setQuery(example)}
                className="text-left p-3 border border-gray-200 rounded-lg hover:border-blue-500 hover:bg-blue-50 transition-colors"
              >
                <span className="text-gray-600">{example}</span>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default SearchPage; 