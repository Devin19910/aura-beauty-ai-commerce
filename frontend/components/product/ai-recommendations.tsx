'use client';

import { Sparkles } from 'lucide-react';

export function AIRecommendations(): React.ReactElement {
  return (
    <div className="max-w-4xl mx-auto text-center">
      <div className="flex items-center justify-center gap-2 mb-4">
        <Sparkles className="w-5 h-5 text-purple-600" />
        <span className="text-purple-600 font-semibold">AI Powered</span>
      </div>

      <h2 className="text-4xl font-bold mb-4 dark:text-white">
        Personalized Just for You
      </h2>
      <p className="text-gray-600 dark:text-gray-400 text-lg mb-8">
        Our AI analyzes your skin type, preferences, and beauty goals to recommend the
        perfect products. Get personalized skincare routines and makeup tips.
      </p>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-6 bg-white dark:bg-gray-800 rounded-lg">
          <div className="text-3xl mb-2">🤖</div>
          <h3 className="font-semibold mb-2 dark:text-white">Smart Analysis</h3>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Advanced AI analyzes your skin and preferences
          </p>
        </div>

        <div className="p-6 bg-white dark:bg-gray-800 rounded-lg">
          <div className="text-3xl mb-2">💎</div>
          <h3 className="font-semibold mb-2 dark:text-white">Quality Products</h3>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Handpicked premium brands trusted by professionals
          </p>
        </div>

        <div className="p-6 bg-white dark:bg-gray-800 rounded-lg">
          <div className="text-3xl mb-2">⚡</div>
          <h3 className="font-semibold mb-2 dark:text-white">Fast Shipping</h3>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Get your beauty products delivered within 2 days
          </p>
        </div>
      </div>
    </div>
  );
}
