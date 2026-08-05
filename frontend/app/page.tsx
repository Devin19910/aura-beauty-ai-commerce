import { Metadata } from 'next'
import Header from '@/components/Header'
import Hero from '@/components/Hero'
import ProductShowcase from '@/components/ProductShowcase'
import Benefits from '@/components/Benefits'
import EmailSignup from '@/components/EmailSignup'
import Footer from '@/components/Footer'

export const metadata: Metadata = {
  title: 'Lash Growth Serum + Mascara Combo | Aura Beauty',
  description: 'Grow lashes while you wear mascara. 2-in-1 formula, clinically-proven results in 30 days. Waterproof, vegan, cruelty-free.',
}

export default function HomePage() {
  return (
    <>
      <Header />
      <Hero />
      <ProductShowcase />
      <Benefits />
      <EmailSignup />
      <Footer />
    </>
  )
}
