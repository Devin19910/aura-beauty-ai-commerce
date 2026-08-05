'use client'

export default function Benefits() {
  const benefits = [
    {
      icon: '✨',
      title: 'Lash Growth Science',
      description: 'Our advanced serum contains biotin and peptides to nourish and strengthen each lash from root to tip.'
    },
    {
      icon: '💧',
      title: 'Waterproof Performance',
      description: 'Engineered for real life - gym, water, all-day wear. Smudge-proof, flake-proof, tear-proof.'
    },
    {
      icon: '🌿',
      title: 'Vegan & Safe',
      description: 'No harsh chemicals. Dermatologist-tested. Safe for sensitive eyes. Cruelty-free certified.'
    }
  ]

  return (
    <section id="benefits" className="py-20 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4">
        <h2 className="text-4xl font-bold text-gray-900 mb-4 text-center">
          Why Women Love It
        </h2>

        <p className="text-xl text-gray-600 text-center mb-12 max-w-3xl mx-auto">
          Our lash growth serum + mascara combo solves a problem women have faced for years: choosing between healthy lashes and beautiful makeup.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {benefits.map((benefit, index) => (
            <div key={index} className="bg-white rounded-lg p-8 text-center shadow-sm hover:shadow-md transition">
              <div className="text-5xl mb-4">{benefit.icon}</div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">{benefit.title}</h3>
              <p className="text-gray-600 leading-relaxed">{benefit.description}</p>
            </div>
          ))}
        </div>

        {/* Key Stats */}
        <div className="mt-16 bg-gradient-to-r from-purple-900 to-rose-900 rounded-lg p-12 text-white text-center">
          <h3 className="text-3xl font-bold mb-8">Join Thousands of Happy Customers</h3>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div>
              <div className="text-5xl font-bold mb-2">30 Days</div>
              <p className="text-purple-200">Clinically-proven lash growth timeline</p>
            </div>

            <div>
              <div className="text-5xl font-bold mb-2">24 Hours</div>
              <p className="text-purple-200">Waterproof wear without smudging</p>
            </div>

            <div>
              <div className="text-5xl font-bold mb-2">100%</div>
              <p className="text-purple-200">Money-back guarantee if not satisfied</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
