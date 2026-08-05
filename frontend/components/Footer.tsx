'use client'

export default function Footer() {
  return (
    <footer className="bg-gray-900 text-gray-300 py-12">
      <div className="max-w-7xl mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          {/* About */}
          <div>
            <h3 className="text-white font-bold mb-4">Aura Beauty</h3>
            <p className="text-sm text-gray-400">
              Growing lashes while delivering beautiful makeup. One innovative product at a time.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-white font-semibold mb-4">Shop</h4>
            <ul className="space-y-2 text-sm">
              <li>
                <a href="#product" className="hover:text-white transition">
                  Our Products
                </a>
              </li>
              <li>
                <a
                  href="https://amazon.com"
                  target="_blank"
                  className="hover:text-white transition"
                >
                  Amazon Store
                </a>
              </li>
              <li>
                <a href="#email" className="hover:text-white transition">
                  Subscribe & Save
                </a>
              </li>
            </ul>
          </div>

          {/* Support */}
          <div>
            <h4 className="text-white font-semibold mb-4">Support</h4>
            <ul className="space-y-2 text-sm">
              <li>
                <a href="#email" className="hover:text-white transition">
                  Contact Us
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-white transition">
                  FAQ
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-white transition">
                  Returns
                </a>
              </li>
            </ul>
          </div>

          {/* Legal */}
          <div>
            <h4 className="text-white font-semibold mb-4">Legal</h4>
            <ul className="space-y-2 text-sm">
              <li>
                <a href="#" className="hover:text-white transition">
                  Privacy Policy
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-white transition">
                  Terms & Conditions
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-white transition">
                  Shipping Policy
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom */}
        <div className="border-t border-gray-800 pt-8 text-center text-sm text-gray-400">
          <p>&copy; 2026 Aura Beauty. All rights reserved.</p>
          <p className="mt-2">
            Follow us on
            <a href="#" className="text-gray-300 hover:text-white ml-2">
              Instagram
            </a>
            {' | '}
            <a href="#" className="text-gray-300 hover:text-white ml-2">
              TikTok
            </a>
            {' | '}
            <a href="#" className="text-gray-300 hover:text-white ml-2">
              Facebook
            </a>
          </p>
        </div>
      </div>
    </footer>
  )
}
