'use client'

import { Button } from '@/components/ui/button'

export default function Header() {
  return (
    <header className="sticky top-0 z-50 bg-white shadow-sm">
      <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
        {/* Logo */}
        <div className="flex items-center gap-2">
          <div className="text-3xl">✨</div>
          <h1 className="text-2xl font-bold text-gray-900">Aura Beauty</h1>
        </div>

        {/* Navigation */}
        <nav className="hidden md:flex gap-8 items-center">
          <a
            href="#product"
            className="text-gray-600 hover:text-gray-900 font-medium transition"
          >
            Product
          </a>
          <a
            href="#benefits"
            className="text-gray-600 hover:text-gray-900 font-medium transition"
          >
            Benefits
          </a>
          <a
            href="#testimonials"
            className="text-gray-600 hover:text-gray-900 font-medium transition"
          >
            Reviews
          </a>
          <a
            href="#email"
            className="text-gray-600 hover:text-gray-900 font-medium transition"
          >
            Newsletter
          </a>
        </nav>

        {/* CTA Button */}
        <Button
          className="bg-rose-500 hover:bg-rose-600 text-white px-6 h-10"
          onClick={() => window.open('https://amazon.com', '_blank')}
        >
          Shop Amazon
        </Button>
      </div>
    </header>
  )
}
