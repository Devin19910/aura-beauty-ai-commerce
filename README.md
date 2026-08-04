# Aura Beauty AI Commerce Platform

[![Node.js](https://img.shields.io/badge/Node.js-v20+-green)](https://nodejs.org)
[![Python](https://img.shields.io/badge/Python-3.11+-blue)](https://www.python.org)
[![Docker](https://img.shields.io/badge/Docker-enabled-blue)](https://www.docker.com)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

Enterprise-grade AI-powered beauty ecommerce platform built with Next.js 15, FastAPI, and intelligent AI agents.

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 20+
- Python 3.11+
- WSL 2 (for Windows users)

### Development Setup

```bash
# Clone or navigate to project
cd ~/Projects/aura-beauty-ai-commerce

# Copy environment variables
cp .env.example .env.local

# Start development environment
docker-compose up -d

# Frontend setup
cd frontend
npm install
npm run dev

# Backend setup (in new terminal)
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload

# Visit http://localhost:3000
```

## 📁 Project Structure

```
aura-beauty-ai-commerce/
├── frontend/                 # Next.js 15 React application
├── backend/                  # FastAPI Python backend
├── ai-agents/               # AI agent orchestration
├── database/                # Database schemas & migrations
├── docs/                    # Documentation
├── devops/                  # Docker, GitHub Actions, K8s
├── scripts/                 # Setup and deployment scripts
├── tests/                   # Integration & E2E tests
├── shared/                  # Shared types and utilities
├── configs/                 # Configuration files
├── memory/                  # AI-readable persistent memory
└── CLAUDE.md               # Master AI memory file
```

## 🏗️ Architecture

### Frontend Stack
- **Framework**: Next.js 15 (App Router)
- **UI**: ShadCN + TailwindCSS + Framer Motion
- **State**: Zustand + React Query
- **Auth**: Clerk
- **Deployment**: Vercel

### Backend Stack
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL + SQLAlchemy
- **Cache**: Redis
- **Tasks**: Celery + Redis
- **Search**: Meilisearch

### AI Stack
- **LLMs**: Claude, OpenAI GPT-4, Gemini
- **Agent Framework**: LangChain + CrewAI
- **Orchestration**: Celery for async jobs
- **Memory**: Redis + PostgreSQL

## 🤖 AI Agents

### Trend Hunter Agent
Autonomous discovery of trending beauty products and market opportunities
- Monitors: TikTok, Google Trends, Amazon, Reddit, Sephora
- Frequency: Daily
- Output: Product recommendations with profit potential

### Pricing Agent
Dynamic pricing optimization with 15%+ margins
- Updates: Real-time based on inventory and competition
- Safety: Automated margin validation and audit logs

### SEO Content Agent
High-ranking content generation for organic growth
- Generates: Product descriptions, blogs, FAQs, comparisons
- Publishing: Direct to Sanity CMS
- Frequency: Continuous based on demand

### Email Agent
Autonomous email marketing and customer engagement
- Campaigns: Abandoned carts, discounts, newsletters, winback
- Personalization: Product recs, browsing history, purchase patterns
- Frequency: Event-triggered + scheduled

### Support Agent
AI-powered customer service with human escalation
- Capabilities: FAQ, order tracking, returns, recommendations
- Languages: English (expandable)
- Quality: Fine-tuned on historical support tickets

### Analytics Agent
Autonomous business insights and anomaly detection
- Metrics: Revenue, conversion, CAC, LTV, AOV
- Alerts: Real-time performance anomalies
- Reports: Daily dashboards and executive summaries

## 🔧 Configuration

See [.env.example](.env.example) for all available environment variables.

Key configurations:
```env
# Database
DATABASE_URL=postgresql://user:password@db:5432/aura_beauty_db

# AI Providers
CLAUDE_API_KEY=your_key
OPENAI_API_KEY=your_key

# Payment
STRIPE_SECRET_KEY=sk_test_...

# Auth
CLERK_SECRET_KEY=your_key
```

## 📦 API Documentation

Complete API documentation available at `http://localhost:8000/docs` (Swagger)

Main endpoints:
- `/api/v1/auth/` - Authentication
- `/api/v1/products/` - Product catalog
- `/api/v1/cart/` - Shopping cart
- `/api/v1/orders/` - Order management
- `/api/v1/payments/` - Stripe integration
- `/api/v1/users/` - User profiles
- `/api/v1/agents/` - Agent control endpoints

## 🗄️ Database

### Migrations
```bash
cd backend
alembic upgrade head           # Apply migrations
alembic revision --autogenerate -m "Add new table"
alembic upgrade head
```

### Schema
- `users` - Authentication and profiles
- `products` - Inventory and product info
- `orders` - Order processing
- `carts` - Shopping carts
- `payments` - Payment records
- `agents_logs` - AI agent execution history
- `analytics_events` - User behavior tracking

## 🧪 Testing

```bash
# Run all tests
npm run test           # Frontend
python -m pytest       # Backend

# E2E tests
npm run test:e2e

# Coverage report
python -m pytest --cov=app
```

## 📊 Monitoring & Logging

### Logs
- Frontend: `/logs/frontend.log`
- Backend: `/logs/backend.log`
- Agents: `/logs/agents.log`

### Metrics
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3001`

## 🚢 Deployment

### Development
```bash
docker-compose up
```

### Staging/Production
See [DEPLOYMENT.md](docs/DEPLOYMENT.md)

### GitHub Actions CI/CD
Automatic testing and deployment on push to main branch.

## 📚 Documentation

- [Architecture Guide](docs/ARCHITECTURE.md)
- [API Reference](docs/API_REFERENCE.md)
- [Database Schema](docs/database/SCHEMA.md)
- [AI Agents Guide](docs/AGENTS.md)
- [SEO Strategy](docs/SEO_STRATEGY.md)
- [Security](docs/SECURITY.md)
- [SOP](docs/SOP.md)
- [Monetization](docs/MONETIZATION.md)

## 🔐 Security

- Secrets stored in environment variables
- HTTPS only in production
- CORS properly configured
- Rate limiting on all endpoints
- SQL injection protection via ORM
- XSS protection via React
- CSRF tokens for state-changing operations
- PCI compliance for payments

See [docs/SECURITY.md](docs/SECURITY.md) for details.

## 💰 Cost Optimization

Monthly infrastructure costs estimated at **$1,100-2,500**:
- Hosting: $400-800
- Database: $150-300
- APIs: $400-1,000
- Monitoring: $150-400

See [MONETIZATION.md](docs/MONETIZATION.md) for detailed breakdown.

## 🤝 Contributing

1. Create feature branch: `git checkout -b feat/feature-name`
2. Make changes following code standards in CLAUDE.md
3. Run tests: `npm test && python -m pytest`
4. Commit: `git commit -m "[feat]: description"`
5. Push: `git push origin feat/feature-name`
6. Create Pull Request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

- Documentation: See `/docs` folder
- Issues: GitHub Issues
- Contact: [engineering team info]

## 🗺️ Roadmap

- **Phase 1** (Current): MVP with core features
- **Phase 2**: AI content generation and email automation
- **Phase 3**: Mobile app and marketplace
- **Phase 4**: Real-time personalization and live shopping

See [CLAUDE.md](CLAUDE.md) for current progress tracking.

---

**Built with ❤️ for beauty entrepreneurs everywhere**

