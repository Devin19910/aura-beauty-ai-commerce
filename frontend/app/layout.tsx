import type { Metadata } from 'next';
import { ClerkProvider } from '@clerk/nextjs';
import { ThemeProvider } from '@/components/theme-provider';
import Navigation from '@/components/common/navigation';
import Footer from '@/components/common/footer';
import '@/styles/globals.css';

export const metadata: Metadata = {
  title: {
    default: 'Aura Beauty - Premium Beauty Products',
    template: '%s | Aura Beauty',
  },
  description:
    'Discover premium beauty products with AI-powered personalized recommendations.',
  keywords: [
    'beauty',
    'skincare',
    'cosmetics',
    'makeup',
    'AI recommendations',
  ],
  authors: [
    {
      name: 'Aura Beauty',
      url: 'https://aurabeauty.com',
    },
  ],
  creator: 'Aura Beauty Team',
  publisher: 'Aura Beauty',
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: 'https://aurabeauty.com',
    title: 'Aura Beauty - Premium Beauty Products',
    description:
      'Discover premium beauty products with AI-powered personalized recommendations.',
    siteName: 'Aura Beauty',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Aura Beauty',
    description: 'Premium beauty products with AI personalization',
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  icons: {
    icon: '/favicon.ico',
    apple: '/apple-touch-icon.png',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}): React.ReactElement {
  return (
    <ClerkProvider>
      <html lang="en" suppressHydrationWarning>
        <head />
        <body className="antialiased">
          <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
            <div className="flex flex-col min-h-screen">
              <Navigation />
              <main className="flex-1">{children}</main>
              <Footer />
            </div>
          </ThemeProvider>
        </body>
      </html>
    </ClerkProvider>
  );
}
