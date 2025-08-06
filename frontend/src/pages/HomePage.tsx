import React from 'react';
import { Link } from 'react-router-dom';
import { Search, Brain, Zap, Globe } from 'lucide-react';

const HomePage: React.FC = () => {
  return (
    <div className="space-y-16">
      {/* Hero Section */}
      <section className="text-center py-16">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-5xl md:text-6xl font-bold text-gray-800 mb-6">
            Akıllı Uygulama
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600">
              {' '}Arama Motoru
            </span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            LLM + RAG teknolojisi ile doğal dil kullanarak uygulama mağazalarından 
            en uygun uygulamaları bulun. "Koşu için offline GPS uygulaması" gibi 
            sorgularla akıllı sonuçlar alın.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/search"
              className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-4 rounded-lg font-semibold hover:shadow-lg transition-all duration-200 flex items-center justify-center space-x-2"
            >
              <Search className="w-5 h-5" />
              <span>Hemen Ara</span>
            </Link>
            <button className="border-2 border-gray-300 text-gray-700 px-8 py-4 rounded-lg font-semibold hover:border-blue-600 hover:text-blue-600 transition-all duration-200">
              Demo İzle
            </button>
          </div>
        </div>
      </section>

      {/* Özellikler */}
      <section className="py-16">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center text-gray-800 mb-12">
            Neden AppSense?
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center p-6 bg-white rounded-xl shadow-lg">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Brain className="w-8 h-8 text-blue-600" />
              </div>
              <h3 className="text-xl font-semibold mb-3">AI Destekli Arama</h3>
              <p className="text-gray-600">
                LLM teknolojisi ile anlamlı ve kişiselleştirilmiş uygulama önerileri
              </p>
            </div>
            
            <div className="text-center p-6 bg-white rounded-xl shadow-lg">
              <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Zap className="w-8 h-8 text-purple-600" />
              </div>
              <h3 className="text-xl font-semibold mb-3">Hızlı Sonuçlar</h3>
              <p className="text-gray-600">
                Vektör veritabanı ile milisaniyeler içinde benzer uygulamalar bulun
              </p>
            </div>
            
            <div className="text-center p-6 bg-white rounded-xl shadow-lg">
              <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Globe className="w-8 h-8 text-green-600" />
              </div>
              <h3 className="text-xl font-semibold mb-3">Çok Dilli Destek</h3>
              <p className="text-gray-600">
                Otomatik dil algılama ile her dilde arama yapabilirsiniz
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Nasıl Çalışır */}
      <section className="py-16 bg-white rounded-xl shadow-lg">
        <div className="max-w-4xl mx-auto px-6">
          <h2 className="text-3xl font-bold text-center text-gray-800 mb-12">
            Nasıl Çalışır?
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-12 h-12 bg-blue-600 text-white rounded-full flex items-center justify-center mx-auto mb-4 font-bold">
                1
              </div>
              <h3 className="text-lg font-semibold mb-2">Sorgu Girin</h3>
              <p className="text-gray-600">
                "Fitness için kalori takip uygulaması" gibi doğal dil sorguları yazın
              </p>
            </div>
            
            <div className="text-center">
              <div className="w-12 h-12 bg-purple-600 text-white rounded-full flex items-center justify-center mx-auto mb-4 font-bold">
                2
              </div>
              <h3 className="text-lg font-semibold mb-2">AI Analiz</h3>
              <p className="text-gray-600">
                Sistem sorgunuzu analiz eder ve benzer uygulamaları bulur
              </p>
            </div>
            
            <div className="text-center">
              <div className="w-12 h-12 bg-green-600 text-white rounded-full flex items-center justify-center mx-auto mb-4 font-bold">
                3
              </div>
              <h3 className="text-lg font-semibold mb-2">Sonuçları Alın</h3>
              <p className="text-gray-600">
                LLM ile iyileştirilmiş, açıklayıcı öneriler alın
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default HomePage; 