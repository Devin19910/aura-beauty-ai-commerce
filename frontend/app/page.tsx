import { Metadata } from 'next';
import Hero from '@/components/common/hero';
import FeaturedProducts from '@/components/product/featured-products';
import { AIRecommendations } from '@/components/product/ai-recommendations';
import Newsletter from '@/components/common/newsletter';

export const metadata: Metadata = {
  title: 'Home - Aura Beauty',
  description:
    'Discover premium beauty products with AI-powered personalized recommendations. Shop skincare, makeup, and more.',
};

export default function HomePage(): React.ReactElement {
  return (
    <>
      <Hero />
      <div className="container mx-auto px-4 py-12">
        <FeaturedProducts />
      </div>
      <div className="bg-gradient-to-r from-purple-50 to-pink-50 dark:from-gray-900 dark:to-gray-800 py-12">
        <div className="container mx-auto px-4">
          <AIRecommendations />
        </div>
      </div>
      <div className="py-12">
        <Newsletter />
      </div>
    </>
  );
}
