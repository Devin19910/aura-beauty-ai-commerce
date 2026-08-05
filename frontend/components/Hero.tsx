'use client'

import { Button } from '@/components/ui/button'

export default function Hero() {
  return (
    <section className="min-h-screen bg-gradient-to-br from-purple-900 via-purple-800 to-rose-900 flex items-center">
      <div className="max-w-7xl mx-auto px-4 py-20 grid grid-cols-1 md:grid-cols-2 gap-12 items-center w-full">

        {/* Left: Text Content */}
        <div>
          <h1 className="text-5xl md:text-6xl font-bold text-white mb-6 leading-tight">
            Grow Lashes While You Wear Mascara
          </h1>

          <p className="text-xl text-purple-100 mb-8 leading-relaxed">
            The world's first lash serum + mascara combo. Clinically-proven lash growth in just 30 days.
          </p>

          <p className="text-lg text-purple-200 mb-8">
            ✓ 2-in-1 formula grows lashes + delivers makeup
            ✓ Waterproof, smudge-proof, 24-hour wear
            ✓ Vegan, cruelty-free, dermatologist-tested
            ✓ 100% money-back guarantee
          </p>

          <div className="flex flex-col sm:flex-row gap-4">
            <Button
              size="lg"
              className="bg-rose-500 hover:bg-rose-600 text-white px-8 text-lg h-12"
              onClick={() => document.getElementById('product').scrollIntoView({ behavior: 'smooth' })}
            >
              Shop Now on Amazon
            </Button>
            <Button
              size="lg"
              variant="outline"
              className="border-2 border-white text-white hover:bg-white/10 px-8 text-lg h-12"
              onClick={() => document.getElementById('email').scrollIntoView({ behavior: 'smooth' })}
            >
              Get $5 Off
            </Button>
          </div>
        </div>

        {/* Right: Image/Visual */}
        <div className="relative h-96 md:h-full flex items-center justify-center">
          <div className="text-center">
            <div className="text-8xl mb-4">✨</div>
            <div className="text-6xl mb-4">💄</div>
            <p className="text-white text-xl font-semibold">Your lash transformation</p>
            <p className="text-purple-200">Coming soon with your product photos</p>
          </div>
        </div>
      </div>
    </section>
  )
}
