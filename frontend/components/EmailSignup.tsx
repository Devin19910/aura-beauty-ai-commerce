'use client'

import { useState } from 'react'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'

export default function EmailSignup() {
  const [email, setEmail] = useState('')
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      const response = await fetch('/api/v1/emails/subscribe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email })
      })

      if (response.ok) {
        setSuccess(true)
        setEmail('')
        setTimeout(() => setSuccess(false), 5000)
      } else {
        setError('Something went wrong. Please try again.')
      }
    } catch (err) {
      console.error('Signup error:', err)
      setError('Unable to subscribe. Please check your connection.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <section id="email" className="bg-gradient-to-r from-purple-100 to-rose-100 py-20">
      <div className="max-w-2xl mx-auto px-4 text-center">
        <h2 className="text-4xl font-bold text-gray-900 mb-4">
          Get $5 Off Your First Order
        </h2>

        <p className="text-xl text-gray-700 mb-2">
          Join our lash community and get:
        </p>

        <ul className="text-lg text-gray-600 mb-8">
          <li>✓ $5 off your first purchase</li>
          <li>✓ Weekly beauty tips & tricks</li>
          <li>✓ Exclusive deals & discounts</li>
          <li>✓ New product alerts</li>
        </ul>

        {success ? (
          <div className="bg-green-100 border border-green-400 text-green-800 px-6 py-4 rounded-lg mb-6">
            <p className="font-semibold">✓ Check your email!</p>
            <p className="text-sm mt-1">Your $5 discount code is on the way.</p>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-3 mb-6">
            <Input
              type="email"
              placeholder="your@email.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              disabled={loading}
              className="flex-1 h-12 text-lg"
            />
            <Button
              type="submit"
              disabled={loading || !email}
              className="bg-rose-500 hover:bg-rose-600 text-white px-8 text-lg h-12 whitespace-nowrap"
            >
              {loading ? 'Subscribing...' : 'Give Me $5 Off'}
            </Button>
          </form>
        )}

        {error && (
          <p className="text-red-600 text-sm">{error}</p>
        )}

        <p className="text-sm text-gray-600">
          We respect your privacy. Unsubscribe anytime.
        </p>
      </div>
    </section>
  )
}
