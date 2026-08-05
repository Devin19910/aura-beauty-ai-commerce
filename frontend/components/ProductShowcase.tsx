'use client'

import { Button } from '@/components/ui/button'

export default function ProductShowcase() {
  return (
    <section id="product" className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4">
        <h2 className="text-4xl font-bold text-gray-900 mb-12 text-center">
          2-IN-1 Innovation
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
          {/* Left: Product Info */}
          <div>
            <h3 className="text-3xl font-bold text-gray-900 mb-6">
              Lash Growth Serum + Waterproof Mascara Combo
            </h3>

            <p className="text-lg text-gray-700 mb-8 leading-relaxed">
              Forget choosing between lash health and beautiful makeup. Our revolutionary 2-in-1 formula grows your lashes while delivering professional-grade waterproof coverage.
            </p>

            {/* Key Benefits */}
            <div className="space-y-4 mb-8">
              <div className="flex gap-4">
                <div className="text-3xl">✓</div>
                <div>
                  <h4 className="font-semibold text-gray-900">Clinically-Proven Lash Growth</h4>
                  <p className="text-gray-600">See visibly fuller, longer lashes in just 30 days</p>
                </div>
              </div>

              <div className="flex gap-4">
                <div className="text-3xl">✓</div>
                <div>
                  <h4 className="font-semibold text-gray-900">Waterproof 24-Hour Wear</h4>
                  <p className="text-gray-600">Smudge-proof, sweat-proof, tear-proof performance</p>
                </div>
              </div>

              <div className="flex gap-4">
                <div className="text-3xl">✓</div>
                <div>
                  <h4 className="font-semibold text-gray-900">Vegan & Cruelty-Free</h4>
                  <p className="text-gray-600">Safe for sensitive eyes, dermatologist-tested</p>
                </div>
              </div>

              <div className="flex gap-4">
                <div className="text-3xl">✓</div>
                <div>
                  <h4 className="font-semibold text-gray-900">Dramatic Volume Without Clumps</h4>
                  <p className="text-gray-600">Professional-grade brush, builds naturally</p>
                </div>
              </div>

              <div className="flex gap-4">
                <div className="text-3xl">✓</div>
                <div>
                  <h4 className="font-semibold text-gray-900">100% Money-Back Guarantee</h4>
                  <p className="text-gray-600">Love it or full refund, no questions asked</p>
                </div>
              </div>
            </div>

            {/* Pricing */}
            <div className="bg-purple-50 p-6 rounded-lg mb-8">
              <p className="text-gray-600 mb-2">Price</p>
              <p className="text-4xl font-bold text-purple-900 mb-4">$34.99</p>
              <p className="text-sm text-gray-600">Available now on Amazon with free shipping</p>
            </div>

            {/* CTA */}
            <Button
              size="lg"
              className="w-full bg-rose-500 hover:bg-rose-600 text-white px-8 text-lg h-12"
              onClick={() => window.open('https://amazon.com', '_blank')}
            >
              Shop Now on Amazon
            </Button>

            <p className="text-center text-sm text-gray-500 mt-4">
              [Amazon link will be added once product launches]
            </p>
          </div>

          {/* Right: Product Visual */}
          <div className="bg-gradient-to-br from-purple-100 to-rose-100 rounded-lg p-12 flex items-center justify-center min-h-96">
            <div className="text-center">
              <div className="text-9xl mb-4">💄</div>
              <h4 className="text-2xl font-bold text-gray-900 mb-2">Your Product Photo</h4>
              <p className="text-gray-600 mb-6">Professional product images will go here</p>
              <p className="text-sm text-gray-500">
                [Images from your 5-image specification list]
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
