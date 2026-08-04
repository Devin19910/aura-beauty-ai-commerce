'use client';

import { Mail } from 'lucide-react';
import { useState } from 'react';

export default function Newsletter(): React.ReactElement {
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    // TODO: Implement newsletter signup API call
    setTimeout(() => {
      setLoading(false);
      setEmail('');
    }, 1000);
  };

  return (
    <div className="container mx-auto px-4">
      <div className="max-w-2xl mx-auto bg-gradient-to-r from-purple-600 to-pink-600 rounded-lg p-12 text-white text-center">
        <div className="flex justify-center mb-4">
          <Mail className="w-10 h-10" />
        </div>

        <h2 className="text-4xl font-bold mb-4">Get Beauty Tips & Exclusive Offers</h2>
        <p className="mb-8 opacity-90">
          Subscribe to our newsletter for skincare tips, product recommendations, and special
          discounts delivered to your inbox.
        </p>

        <form onSubmit={handleSubmit} className="flex gap-2">
          <input
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="flex-1 px-4 py-3 rounded-lg text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-white"
          />
          <button
            type="submit"
            disabled={loading}
            className="px-8 py-3 bg-white text-purple-600 font-semibold rounded-lg hover:bg-gray-100 transition disabled:opacity-50"
          >
            {loading ? 'Subscribing...' : 'Subscribe'}
          </button>
        </form>
      </div>
    </div>
  );
}
