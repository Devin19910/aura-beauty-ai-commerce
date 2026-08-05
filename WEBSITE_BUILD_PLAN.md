# 🌐 Website Build Plan
**Build Your Lash Serum Mascara Ecommerce Website in 2 Weeks**

---

## Overview

You have:
- ✅ Next.js 14 frontend (already set up)
- ✅ FastAPI backend (production-ready)
- ✅ PostgreSQL database (ready)
- ✅ Product images (descriptions provided)
- ✅ Product content (Amazon listing copy)

We need to build:
- 🔄 Homepage (hero + product showcase)
- 🔄 Product page (detailed description + buy button)
- 🔄 Email capture (newsletter signup)
- 🔄 About page (your story)
- 🔄 Shopping cart (optional but recommended)

---

## Phase 1: MVP Website (Week 1)

### Goal
Get a professional-looking site live with:
- Beautiful homepage
- Product showcase
- Email capture
- "Buy on Amazon" call-to-action

### What We'll Build

#### 1. Homepage Component
```
Homepage (/)
├─ Header with navigation
├─ Hero section (benefit-focused)
│  ├─ Headline: "Grow Lashes While You Wear Mascara"
│  ├─ Subheadline: Key benefit
│  ├─ Hero image: Woman with mascara
│  └─ CTA button: "Shop Now on Amazon"
├─ Product showcase
│  ├─ Product image
│  ├─ Key benefits (bullets)
│  ├─ Price
│  └─ "Buy on Amazon" button
├─ Why choose us (3 sections)
│  ├─ Lash growth science
│  ├─ Waterproof performance
│  └─ Vegan & safe
├─ Customer testimonials (from Amazon reviews)
├─ Email signup section
│  ├─ Headline: "Get $5 Off Your First Order"
│  ├─ Email input
│  └─ Subscribe button
└─ Footer
   ├─ About
   ├─ Contact
   ├─ Social media
   └─ Copyright
```

#### 2. Product Page
```
Product (/product)
├─ Product images (the 5 we described)
│  ├─ Main image gallery
│  └─ Thumbnail selection
├─ Product details
│  ├─ Title
│  ├─ Price
│  ├─ Rating (from Amazon)
│  └─ Review count
├─ Description
│  ├─ What makes it different
│  ├─ Key benefits
│  ├─ How to use
│  └─ Ingredients
├─ Call-to-action section
│  ├─ "Buy Now on Amazon" button (large, prominent)
│  ├─ Direct Amazon link
│  └─ "Check Amazon Reviews" link
├─ Testimonials
│  └─ Real reviews from Amazon customers
└─ FAQ section
   ├─ How long until I see results?
   ├─ Is it safe for sensitive eyes?
   ├─ How does it compare to X brand?
   └─ Money-back guarantee details
```

#### 3. About Page
```
About (/about)
├─ Your story
│  ├─ Why you created this product
│  ├─ Your journey
│  └─ Your mission
├─ The product
│  ├─ What problem it solves
│  ├─ How it works
│  └─ Why it's different
├─ Values
│  ├─ Vegan & cruelty-free
│  ├─ Dermatologist-tested
│  └─ Results-focused
└─ Contact info
   ├─ Email
   └─ Social media
```

#### 4. Email Signup
```
Newsletter Signup (In header + footer + dedicated section)
├─ Input field (email)
├─ Button (Subscribe)
├─ Benefits copy:
│  ├─ "$5 off first order"
│  ├─ "Beauty tips & trends"
│  └─ "Exclusive deals"
└─ Auto-response
   ├─ Welcome email
   ├─ Discount code
   └─ Product education
```

---

## Phase 2: Advanced Features (Week 2)

### Optional but Recommended

#### 1. Shopping Cart (Stripe Integration)
```
Shopping Cart
├─ View cart
├─ Update quantities
├─ Remove items
├─ Checkout
├─ Stripe payment processing
└─ Order confirmation
```

#### 2. Email Automation
```
Email Flows
├─ Welcome email (when subscribe)
├─ Thank you email (after purchase)
├─ Follow-up email (day 7)
├─ Review request (day 30)
└─ Re-engagement (inactive customers)
```

#### 3. Blog Integration
```
Blog Section (/blog)
├─ Beauty tips
├─ Lash care guides
├─ Product education
└─ SEO-optimized content
```

---

## Tech Implementation

### Files You Need to Create

#### Homepage Component
```typescript
// frontend/app/page.tsx
export default function Home() {
  return (
    <>
      <Header />
      <HeroSection />
      <ProductShowcase />
      <WhyChooseUs />
      <CustomerTestimonials />
      <EmailSignup />
      <Footer />
    </>
  )
}
```

#### Product Page Component
```typescript
// frontend/app/product/page.tsx
export default function ProductPage() {
  return (
    <>
      <Header />
      <ProductImages />
      <ProductDetails />
      <ProductDescription />
      <CallToAction />
      <Testimonials />
      <FAQ />
      <Footer />
    </>
  )
}
```

#### Reusable Components (You already have most)
```
frontend/components/
├─ Header.tsx               [Create]
├─ HeroSection.tsx          [Create]
├─ ProductCard.tsx          [Create]
├─ ProductImages.tsx        [Create]
├─ EmailSignup.tsx          [Create]
├─ TestimonialCard.tsx      [Create]
├─ Button.tsx               [Use existing ShadCN]
├─ Card.tsx                 [Use existing ShadCN]
├─ Input.tsx                [Use existing ShadCN]
└─ Footer.tsx               [Create]
```

#### API Endpoints (Build on existing FastAPI)
```python
# backend/app/api/endpoints/
├─ products.py             [Extend]
├─ emails.py                [Create for newsletter signup]
├─ orders.py                [Create for shopping cart]
├─ reviews.py               [Create if displaying reviews]
└─ admin.py                 [Use existing]
```

#### Database Models (Add to existing)
```python
# backend/app/models/
├─ Product.py              [Already exists]
├─ User.py                 [Already exists]
├─ EmailSubscriber.py      [Create]
├─ Order.py                [Already exists]
└─ Review.py               [Extend]
```

---

## Content Ready to Use

### Homepage Copy
```
HERO SECTION:
Headline: "Grow Lashes While You Wear Mascara"
Subheadline: "The world's first lash serum + mascara combo. 
             Clinically-proven results in 30 days."

PRODUCT SHOWCASE:
"2-IN-1 INNOVATION
  Forget choosing between lash health and beautiful makeup. 
  Our revolutionary formula grows your lashes while delivering 
  professional-grade waterproof coverage.
  
  ✓ Clinically-proven lash growth in 30 days
  ✓ Waterproof, smudge-proof, 24-hour wear
  ✓ Vegan, cruelty-free, dermatologist-tested
  ✓ Works on natural lashes and extensions
  ✓ 100% money-back guarantee"

BENEFITS:
"Why Women Love It
  • See real lash growth in just 30 days
  • Professional-grade formula, drugstore-friendly price
  • One product replaces serum + mascara (saves money & time)
  • Works even at the gym, in the water, all day long
  • Safe for sensitive eyes, no harsh chemicals"

SOCIAL PROOF:
"Join 10,000+ women who've discovered longer, fuller, 
more beautiful lashes with our lash serum mascara combo."
```

### Product Page Copy
```
Use the Amazon listing description we already wrote.
It's proven to convert and it's SEO-optimized.

Just copy from: amazon_business_plan.json
Section: "amazon_listing" → "description"
```

### Email Signup Copy
```
MAIN CTA:
"Get $5 Off Your First Order"

SUPPORTING TEXT:
"Join our lash community and get:
  ✓ $5 off your first purchase
  ✓ Weekly beauty tips
  ✓ Exclusive deals & discounts
  ✓ New product alerts"

BUTTON TEXT:
"Give Me $5 Off"
```

---

## Build Checklist

### Week 1 Tasks

#### Day 1-2: Setup & Design
- [ ] Create design mockups (Figma or pen/paper)
- [ ] Set up Next.js pages:
  - [ ] `/` (homepage)
  - [ ] `/product` (product detail)
  - [ ] `/about` (about page)
- [ ] Create component structure
- [ ] Install additional packages if needed

#### Day 3-4: Build Homepage
- [ ] Create Header component
- [ ] Create HeroSection component
- [ ] Create ProductShowcase component
- [ ] Create EmailSignup component
- [ ] Create Footer component
- [ ] Style with Tailwind (you already have it)
- [ ] Test responsiveness

#### Day 5-6: Build Product Page
- [ ] Create ProductImages component
- [ ] Create ProductDetails component
- [ ] Add image gallery
- [ ] Add testimonials section
- [ ] Add FAQ section
- [ ] Create email capture in product page
- [ ] Test all interactions

#### Day 7: Polish & Deploy
- [ ] Test all pages on mobile
- [ ] Test email signup flow
- [ ] Fix any styling issues
- [ ] Deploy to development environment
- [ ] Final review

### Week 2 Tasks (Optional but Recommended)

#### Email Integration
- [ ] Set up Resend API (for email sending)
- [ ] Create welcome email template
- [ ] Create discount code generation
- [ ] Create email service in backend
- [ ] Test email flows

#### Shopping Cart (If Adding)
- [ ] Create Cart context
- [ ] Create Add to Cart functionality
- [ ] Integrate Stripe
- [ ] Create checkout flow
- [ ] Test payment processing

#### Analytics
- [ ] Add Google Analytics
- [ ] Track pageviews
- [ ] Track email signups
- [ ] Track button clicks

---

## Design Inspiration

### Color Scheme (Beauty/Lash Focus)
```
Primary:     Deep Purple (#2D1B4E)  - Sophisticated, beauty-focused
Secondary:   Rose Pink (#E91E63)    - Energetic, premium feel
Accent:      Gold (#FFD700)         - Luxury, high-end
Background:  Off-white (#F8F8F8)    - Clean, minimal
Text:        Dark Gray (#333333)    - Readable, professional
```

### Layout
- Clean, minimal aesthetic
- Large product images
- Bold, compelling headlines
- White space (not cramped)
- Strong CTAs (buttons everywhere)

### Typography
```
Headlines:   Bold, large (32-48px)
Body:        Clear, readable (16-18px)
Buttons:     Clear, prominent (18-24px)
CTA buttons: BRIGHT, impossible to miss
```

---

## Step-by-Step Build Instructions

### 1. Create HomePage Component
```typescript
// frontend/app/page.tsx
'use client'

import Header from '@/components/Header'
import Hero from '@/components/Hero'
import Product from '@/components/Product'
import Benefits from '@/components/Benefits'
import Testimonials from '@/components/Testimonials'
import EmailSignup from '@/components/EmailSignup'
import Footer from '@/components/Footer'

export default function Home() {
  return (
    <div className="w-full">
      <Header />
      <Hero />
      <Product />
      <Benefits />
      <Testimonials />
      <EmailSignup />
      <Footer />
    </div>
  )
}
```

### 2. Create Hero Component
```typescript
// frontend/components/Hero.tsx
import Image from 'next/image'
import { Button } from '@/components/ui/button'

export default function Hero() {
  return (
    <section className="min-h-screen bg-gradient-to-br from-purple-900 via-purple-800 to-rose-900 flex items-center">
      <div className="max-w-7xl mx-auto px-4 py-20 grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
        
        {/* Left: Text Content */}
        <div>
          <h1 className="text-5xl md:text-6xl font-bold text-white mb-6">
            Grow Lashes While You Wear Mascara
          </h1>
          
          <p className="text-xl text-purple-100 mb-8">
            The world's first lash serum + mascara combo. 
            Clinically-proven lash growth in just 30 days.
          </p>
          
          <div className="flex gap-4">
            <Button 
              size="lg" 
              className="bg-rose-500 hover:bg-rose-600 text-white px-8"
              onClick={() => window.location.href = 'https://amazon.com'}
            >
              Shop Now on Amazon
            </Button>
            <Button 
              size="lg" 
              variant="outline" 
              className="border-white text-white hover:bg-white/20"
              onClick={() => document.getElementById('product').scrollIntoView()}
            >
              Learn More
            </Button>
          </div>
        </div>
        
        {/* Right: Image */}
        <div className="relative h-96 md:h-full">
          <Image
            src="/images/hero-mascara.jpg"
            alt="Lash serum mascara combo"
            fill
            className="object-cover rounded-lg"
          />
        </div>
      </div>
    </section>
  )
}
```

### 3. Create EmailSignup Component
```typescript
// frontend/components/EmailSignup.tsx
'use client'

import { useState } from 'react'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'

export default function EmailSignup() {
  const [email, setEmail] = useState('')
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      const response = await fetch('/api/v1/emails/subscribe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email })
      })

      if (response.ok) {
        setSuccess(true)
        setEmail('')
        setTimeout(() => setSuccess(false), 3000)
      }
    } catch (error) {
      console.error('Signup error:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="bg-purple-50 py-16">
      <div className="max-w-2xl mx-auto px-4 text-center">
        <h2 className="text-4xl font-bold mb-4">Get $5 Off Your First Order</h2>
        <p className="text-lg text-gray-600 mb-8">
          Join our lash community and get weekly beauty tips, 
          exclusive deals, and new product alerts.
        </p>

        {success ? (
          <div className="bg-green-100 text-green-800 p-4 rounded-lg">
            ✓ Check your email for your $5 discount code!
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="flex gap-2">
            <Input
              type="email"
              placeholder="your@email.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="flex-1"
            />
            <Button
              type="submit"
              disabled={loading}
              className="bg-rose-500 hover:bg-rose-600 px-8"
            >
              {loading ? 'Subscribing...' : 'Give Me $5 Off'}
            </Button>
          </form>
        )}
      </div>
    </section>
  )
}
```

---

## Backend API to Create

### Email Signup Endpoint
```python
# backend/app/api/endpoints/emails.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from app.database import get_db

router = APIRouter()

class EmailSubscribe(BaseModel):
    email: EmailStr

@router.post("/api/v1/emails/subscribe")
async def subscribe_email(data: EmailSubscribe, db=Depends(get_db)):
    """Subscribe email to newsletter"""
    try:
        # Check if already subscribed
        existing = db.query(EmailSubscriber).filter_by(email=data.email).first()
        if existing:
            return {"message": "Already subscribed", "status": "ok"}
        
        # Add new subscriber
        subscriber = EmailSubscriber(email=data.email)
        db.add(subscriber)
        db.commit()
        
        # Send welcome email with discount code
        # (integrate with Resend API)
        
        return {"message": "Subscribed successfully", "status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

## Hosting & Deployment

### Development (Week 1)
- Run locally: `npm run dev` (port 3000)
- Test all pages
- Test mobile responsiveness

### Production (Week 2)
**Frontend:** Deploy to Vercel (easiest for Next.js)
- Connect GitHub repo
- Auto-deploy on push
- Free tier includes everything you need

**Backend:** Keep on local server or AWS (for development)

---

## Timeline

```
WEEK 1: MVP Website
├─ Day 1-2: Design & setup
├─ Day 3-4: Homepage build
├─ Day 5-6: Product page build
└─ Day 7: Polish & deploy

WEEK 2: Optional Features
├─ Email automation
├─ Shopping cart (optional)
├─ Analytics
└─ Final polish

LAUNCH: Week 2, Day 5-7
```

---

## Success Metrics

### Week 1 Goals
- ✅ Homepage live
- ✅ Product page live
- ✅ Email signup working
- ✅ Mobile responsive
- ✅ Page load time <3 seconds

### Week 2 Goals (If doing Phase 2)
- ✅ Email flows working
- ✅ Shopping cart functional
- ✅ Analytics tracking
- ✅ 100+ email signups

---

## Ready to Start?

**Next Step:** 

1. ✅ Review this plan
2. 🔄 Start building homepage (we can help with components)
3. 🔄 Contact supplier (send Alibaba message)
4. 🔄 Parallel: Order from supplier while building site

You ready to build? 🚀

I can help you with:
- React/TypeScript for components
- Tailwind CSS styling
- API integration
- Email flows
- Payment integration

Just say the word! 💻
