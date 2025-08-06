import React from 'react';
import { Brain, Database, Globe, Zap, Code, Users } from 'lucide-react';

const AboutPage: React.FC = () => {
  return (
    <div className="max-w-4xl mx-auto space-y-12">
      {/* Hero Section */}
      <section className="text-center py-8">
        <h1 className="text-4xl font-bold text-gray-800 mb-6">
          AppSense Hakkında
        </h1>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
          LLM + RAG teknolojisi ile güçlendirilmiş, akıllı uygulama arama motoru. 
          Doğal dil ile uygulama mağazalarından en uygun uygulamaları bulun.
        </p>
      </section>

      {/* Teknoloji */}
      <section className="bg-white rounded-xl shadow-lg p-8">
        <h2 className="text-2xl font-bold text-gray-800 mb-6">Teknolojiler</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="flex items-start space-x-4">
            <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
              <Brain className="w-6 h-6 text-blue-600" />
            </div>
            <div>
              <h3 className="text-lg font-semibold mb-2">LLM (Large Language Model)</h3>
              <p className="text-gray-600">
                Groq ve Llama 3 gibi gelişmiş dil modelleri ile doğal dil anlama 
                ve akıllı öneriler sunma.
              </p>
            </div>
          </div>

          <div className="flex items-start space-x-4">
            <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
              <Database className="w-6 h-6 text-purple-600" />
            </div>
            <div>
              <h3 className="text-lg font-semibold mb-2">RAG (Retrieval Augmented Generation)</h3>
              <p className="text-gray-600">
                Vektör veritabanı ile hızlı benzerlik arama ve LLM ile 
                sonuçları iyileştirme.
              </p>
            </div>
          </div>

          <div className="flex items-start space-x-4">
            <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
              <Globe className="w-6 h-6 text-green-600" />
            </div>
            <div>
              <h3 className="text-lg font-semibold mb-2">Çok Dilli Destek</h3>
              <p className="text-gray-600">
                Otomatik dil algılama ve çok dilli embedding modelleri ile 
                her dilde arama yapabilme.
              </p>
            </div>
          </div>

          <div className="flex items-start space-x-4">
            <div className="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center">
              <Zap className="w-6 h-6 text-yellow-600" />
            </div>
            <div>
              <h3 className="text-lg font-semibold mb-2">Hızlı Arama</h3>
              <p className="text-gray-600">
                Pinecone vektör veritabanı ile milisaniyeler içinde 
                benzer uygulamalar bulma.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Özellikler */}
      <section className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl p-8">
        <h2 className="text-2xl font-bold text-gray-800 mb-6">Özellikler</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-800">Arama Özellikleri</h3>
            <ul className="space-y-2 text-gray-600">
              <li>• Doğal dil ile arama</li>
              <li>• Kategori bazlı filtreleme</li>
              <li>• Benzerlik skorları</li>
              <li>• Çok dilli sonuçlar</li>
            </ul>
          </div>

          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-800">AI Özellikleri</h3>
            <ul className="space-y-2 text-gray-600">
              <li>• LLM destekli öneriler</li>
              <li>• Akıllı sonuç sıralama</li>
              <li>• Kişiselleştirilmiş öneriler</li>
              <li>• Açıklayıcı sonuçlar</li>
            </ul>
          </div>
        </div>
      </section>

      {/* Geliştirme */}
      <section className="bg-white rounded-xl shadow-lg p-8">
        <h2 className="text-2xl font-bold text-gray-800 mb-6">Geliştirme</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center">
            <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Code className="w-8 h-8 text-blue-600" />
            </div>
            <h3 className="text-lg font-semibold mb-2">Backend</h3>
            <p className="text-gray-600 text-sm">
              Python, FastAPI, Pinecone, Sentence Transformers
            </p>
          </div>

          <div className="text-center">
            <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Globe className="w-8 h-8 text-purple-600" />
            </div>
            <h3 className="text-lg font-semibold mb-2">Frontend</h3>
            <p className="text-gray-600 text-sm">
              React, TypeScript, Tailwind CSS, Framer Motion
            </p>
          </div>

          <div className="text-center">
            <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Users className="w-8 h-8 text-green-600" />
            </div>
            <h3 className="text-lg font-semibold mb-2">Kullanıcı Deneyimi</h3>
            <p className="text-gray-600 text-sm">
              Modern UI/UX, responsive design, accessibility
            </p>
          </div>
        </div>
      </section>

      {/* İletişim */}
      <section className="bg-gray-50 rounded-xl p-8">
        <h2 className="text-2xl font-bold text-gray-800 mb-6">İletişim</h2>
        <div className="text-center">
          <p className="text-gray-600 mb-4">
            AppSense projesi hakkında sorularınız veya önerileriniz için:
          </p>
          <div className="flex justify-center space-x-4">
            <a 
              href="https://github.com" 
              className="text-blue-600 hover:text-blue-800 font-medium"
              target="_blank"
              rel="noopener noreferrer"
            >
              GitHub
            </a>
            <a 
              href="mailto:contact@appsense.com" 
              className="text-blue-600 hover:text-blue-800 font-medium"
            >
              E-posta
            </a>
          </div>
        </div>
      </section>
    </div>
  );
};

export default AboutPage; 