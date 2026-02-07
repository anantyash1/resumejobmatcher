import React from 'react';

const Footer = () => {
  return (
    <footer className="bg-gray-800 text-white py-8 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <p className="text-gray-400">
            © 2026 JobMatch. Built with Classical ML & NLP.
          </p>
          <p className="text-gray-500 text-sm mt-2">
            TF-IDF • Cosine Similarity • Explainable AI
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;