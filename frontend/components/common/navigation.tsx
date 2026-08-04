import Link from 'next/link';
import { SignInButton, SignUpButton, UserButton } from '@clerk/nextjs';
import { ShoppingCart, Search } from 'lucide-react';

export default function Navigation(): React.ReactElement {
  return (
    <nav className="sticky top-0 z-50 w-full bg-white dark:bg-gray-950 border-b border-gray-200 dark:border-gray-800">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <Link href="/" className="text-2xl font-bold gradient-primary bg-clip-text text-transparent">
          Aura Beauty
        </Link>

        <div className="hidden md:flex gap-8">
          <Link href="/products" className="text-gray-700 dark:text-gray-300 hover:text-purple-600 dark:hover:text-purple-400">
            Products
          </Link>
          <Link href="/blog" className="text-gray-700 dark:text-gray-300 hover:text-purple-600 dark:hover:text-purple-400">
            Blog
          </Link>
          <Link href="/about" className="text-gray-700 dark:text-gray-300 hover:text-purple-600 dark:hover:text-purple-400">
            About
          </Link>
        </div>

        <div className="flex items-center gap-4">
          <button className="p-2 hover:bg-gray-100 dark:hover:bg-gray-900 rounded-lg transition">
            <Search className="w-5 h-5" />
          </button>
          <Link href="/cart" className="relative p-2 hover:bg-gray-100 dark:hover:bg-gray-900 rounded-lg transition">
            <ShoppingCart className="w-5 h-5" />
            <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
          </Link>

          <div className="flex gap-2">
            <SignInButton mode="modal">
              <button className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-900 rounded-lg transition">
                Sign In
              </button>
            </SignInButton>
            <SignUpButton mode="modal">
              <button className="px-4 py-2 text-sm font-medium text-white bg-purple-600 hover:bg-purple-700 rounded-lg transition">
                Sign Up
              </button>
            </SignUpButton>
            <UserButton afterSignOutUrl="/" />
          </div>
        </div>
      </div>
    </nav>
  );
}
