'use client';

import { Star, Heart } from 'lucide-react';
import Link from 'next/link';

export default function FeaturedProducts(): React.ReactElement {
  const products = [
    {
      id: 1,
      name: 'Luxury Face Serum',
      price: 89.99,
      rating: 4.8,
      reviews: 245,
      image: '/images/serum-1.jpg',
    },
    {
      id: 2,
      name: 'Hydrating Night Cream',
      price: 79.99,
      rating: 4.9,
      reviews: 312,
      image: '/images/cream-1.jpg',
    },
    {
      id: 3,
      name: 'Vitamin C Cleanser',
      price: 39.99,
      rating: 4.7,
      reviews: 189,
      image: '/images/cleanser-1.jpg',
    },
    {
      id: 4,
      name: 'SPF 50+ Sunscreen',
      price: 49.99,
      rating: 4.8,
      reviews: 267,
      image: '/images/sunscreen-1.jpg',
    },
  ];

  return (
    <div className="py-12">
      <h2 className="text-4xl font-bold mb-4">Featured Products</h2>
      <p className="text-gray-600 dark:text-gray-400 mb-8">
        Handpicked beauty products recommended by our AI
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {products.map((product) => (
          <Link key={product.id} href={`/products/${product.id}`}>
            <div className="bg-white dark:bg-gray-800 rounded-lg overflow-hidden shadow hover:shadow-lg transition cursor-pointer group">
              <div className="relative overflow-hidden bg-gray-100 dark:bg-gray-700 h-64">
                <div className="w-full h-full bg-gradient-to-br from-purple-100 to-pink-100 dark:from-purple-900 dark:to-pink-900 flex items-center justify-center">
                  <span className="text-4xl opacity-20">🧴</span>
                </div>
                <button className="absolute top-4 right-4 p-2 bg-white dark:bg-gray-800 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700 transition">
                  <Heart className="w-5 h-5" />
                </button>
              </div>

              <div className="p-4">
                <h3 className="font-semibold text-lg mb-2 dark:text-white">{product.name}</h3>
                <div className="flex items-center gap-1 mb-2">
                  <div className="flex">
                    {Array(5)
                      .fill(0)
                      .map((_, i) => (
                        <Star
                          key={i}
                          className={`w-4 h-4 ${
                            i < Math.floor(product.rating) ? 'fill-yellow-400 text-yellow-400' : 'text-gray-300'
                          }`}
                        />
                      ))}
                  </div>
                  <span className="text-sm text-gray-600 dark:text-gray-400">
                    ({product.reviews})
                  </span>
                </div>
                <div className="text-xl font-bold text-purple-600 dark:text-purple-400">
                  ${product.price}
                </div>
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
