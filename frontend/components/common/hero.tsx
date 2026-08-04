import Link from 'next/link';
import { ArrowRight } from 'lucide-react';

export default function Hero(): React.ReactElement {
  return (
    <div className="gradient-primary py-20">
      <div className="container mx-auto px-4">
        <div className="text-center text-white">
          <h1 className="text-5xl font-bold mb-6">Beauty Meets Intelligence</h1>
          <p className="text-xl mb-8 opacity-90">
            Discover premium beauty products personalized just for you with AI
          </p>
          <div className="flex gap-4 justify-center">
            <Link
              href="/products"
              className="px-8 py-3 bg-white text-purple-600 font-semibold rounded-lg hover:bg-gray-100 transition flex items-center gap-2"
            >
              Shop Now <ArrowRight className="w-4 h-4" />
            </Link>
            <Link
              href="/about"
              className="px-8 py-3 border-2 border-white text-white font-semibold rounded-lg hover:bg-white/10 transition"
            >
              Learn More
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
