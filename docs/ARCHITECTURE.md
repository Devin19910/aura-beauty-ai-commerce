# Aura Beauty AI Commerce - Architecture Guide

## System Overview

Aura Beauty is an enterprise-scale, AI-powered beauty ecommerce platform designed for high scalability and reliability. The architecture follows a microservices-ready design with clear separation of concerns.

## Architecture Layers

### 1. Presentation Layer (Frontend)

**Technology**: Next.js 15 (App Router) + React 19

**Key Characteristics**:
- Server Components for optimal performance
- App Router with file-based routing
- ShadCN UI component library
- TailwindCSS for styling
- Zustand for global state
- React Query for server state management

**Deployment**: Vercel (automatic deployments)

**Key Pages**:
- Homepage with AI recommendations
- Product listing/search
- Product detail pages
- Shopping cart
- Checkout flow
- User dashboard
- Blog

### 2. API Layer (Backend)

**Technology**: FastAPI (Python) + Uvicorn

**Architecture**:
```
FastAPI Server
├── Routes (/api/v1/*)
├── Dependencies (Auth, DB, Rate Limiting)
├── Middleware (CORS, Security Headers)
└── Exception Handlers
```

**API Versioning**: `/api/v1/` (allows future `/api/v2/`)

**Key Endpoints**:
- Authentication (Clerk integration)
- Products CRUD
- Cart management
- Order processing
- Payment webhooks (Stripe)
- Search (Meilisearch proxy)
- AI agent controls
- Analytics

### 3. Data Layer

**Database**: PostgreSQL (async via AsyncPG)

**Schema**:
- Users & Authentication
- Products & Inventory
- Orders & Transactions
- Reviews & Ratings
- Cart & Wishlist
- Agent Execution Logs
- Analytics Events

**Migrations**: Alembic for schema versioning

**Cache**: Redis
- Session storage
- Cart data
- Search indexes
- Rate limit counters
- Agent job queues

### 4. AI Agent Layer

**Technology**: LangChain + CrewAI + Celery

**Agents**:
1. **Trend Hunter**: Autonomous product discovery
2. **Pricing**: Dynamic pricing engine
3. **SEO Content**: Content generation
4. **Email**: Marketing automation
5. **Support**: Customer service
6. **Analytics**: Business intelligence

**Architecture**:
```
Agent System
├── Agent Definition (prompts, tools)
├── Orchestration (scheduling, coordination)
├── Memory (execution history, context)
├── Tools (API integrations, data access)
└── Execution (Celery workers, beat)
```

**Scheduling**: Celery Beat for automated execution

### 5. Integration Layer

**External Services**:

| Service | Purpose | Integration |
|---------|---------|-------------|
| Clerk | Authentication | Frontend + Backend |
| Stripe | Payments | Webhook + API |
| Resend | Email | API |
| Meilisearch | Search | Standalone service |
| Sanity CMS | Content management | API |
| Claude/OpenAI/Gemini | AI | Agent API calls |

## Network Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Client (Browser)                         │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │  Vercel CDN + Frontend  │ (Next.js)
        └────────┬───────────────┘
                 │
                 ▼
        ┌────────────────────────┐
        │  API Gateway / Nginx    │
        └────┬──────────┬────┬────┘
             │          │    │
    ┌────────▼──┐    ┌──▼──┐ └────────────────┐
    │  FastAPI  │    │Redis│                  │
    │  Backend  │    └─────┘         ┌────────▼──────┐
    └────┬──────┘                     │Meilisearch    │
         │                            │(Search)       │
    ┌────▼──────────────┐            └───────────────┘
    │  PostgreSQL       │
    │  (Main Database)  │
    └────┬──────────────┘
         │
    ┌────▼──────────────┐
    │  Celery Workers   │
    │  (AI Agents)      │
    └───────────────────┘
```

## Data Flow

### 1. Product Browsing Flow

```
User Browser → Next.js Frontend → FastAPI /api/v1/products/ 
→ PostgreSQL/Redis → Response → Frontend → Browser
```

### 2. Search Flow

```
User Search Query → Frontend → FastAPI /api/v1/search/ 
→ Meilisearch → Results → Response → Frontend
```

### 3. Purchase Flow

```
Cart → Checkout → Create PaymentIntent (Stripe) 
→ Frontend: Collect Payment → Stripe → Webhook 
→ Backend: Verify Payment → Create Order → Update Inventory → Send Email
```

### 4. AI Agent Flow

```
Trigger (Scheduled/Manual) → Celery Beat/Endpoint 
→ Celery Worker → Agent (LangChain) → Tool Calls 
→ External APIs / Database → Process Results 
→ Store Results → Database/Logs
```

## Scalability Strategy

### Current (0-10k users)
- Single backend instance
- PostgreSQL single node
- Redis single instance
- Meilisearch single instance

### Phase 1 (10k-100k users)
- Backend autoscaling (2-10 instances)
- PostgreSQL read replicas
- Redis cluster
- Meilisearch replication

### Phase 2 (100k-1M users)
- Microservices split (products, orders, payments)
- PostgreSQL sharding by user_id
- Kafka for event streaming
- Elasticsearch for analytics
- Multi-region deployment

### Phase 3 (1M+ users)
- Full microservices architecture
- Kubernetes orchestration
- GraphQL API layer
- Real-time analytics stream processing
- Multi-cloud deployment

## Security Architecture

### Authentication & Authorization

```
Frontend: Clerk → JWT Token → API Request
Backend: JWT Validation → Role-Based Access Control → Resource Access
```

**RBAC Roles**:
- `user`: Regular customer
- `seller`: Vendor (future)
- `admin`: Platform administrator
- `support`: Customer support
- `agent`: System agents

### Data Protection

- Passwords: bcrypt hashing
- Secrets: Environment variables
- API Keys: Encrypted storage
- PCI Compliance: Stripe tokenization
- HTTPS: Enforced everywhere
- CORS: Restricted origins

### API Security

- Rate limiting (Redis)
- CSRF protection (same-site cookies)
- SQL injection prevention (SQLAlchemy ORM)
- XSS prevention (React escaping)
- HSTS headers

## Monitoring & Observability

### Logs

- **Frontend**: Browser console, error tracking (Sentry)
- **Backend**: Structured JSON logging to files/stdout
- **Agents**: Execution logs in database

### Metrics

- **Application**: Response time, error rate, request count
- **Database**: Query performance, connection pool
- **Cache**: Hit rate, evictions
- **Agents**: Execution time, success rate, cost

### Tools

- **APM**: New Relic
- **Error Tracking**: Sentry
- **Metrics**: Prometheus
- **Visualization**: Grafana
- **Logs**: ELK Stack (future)

## CI/CD Pipeline

```
Developer Push → GitHub
  ↓
GitHub Actions → Lint, Test, Build
  ↓
Tests Pass → Docker Build → Push to Registry
  ↓
Frontend → Vercel Deployment
Backend → AWS ECS Deployment
  ↓
Health Checks → Monitor Metrics
```

## Deployment Environments

### Development
- Docker Compose locally
- Hot reload
- Mock data
- Logging: verbose

### Staging
- AWS infrastructure (mirrored production)
- Real integrations (test accounts)
- Real database (production schema)
- Logging: info

### Production
- Multi-region AWS
- Auto-scaling enabled
- Monitoring & alerts
- Logging: warnings + errors
- Daily backups

## Key Architecture Decisions

### Why FastAPI?
- ✓ Async-first (handles concurrent requests)
- ✓ Pydantic validation (type-safe)
- ✓ Auto-generated docs (Swagger/ReDoc)
- ✓ Excellent for AI integrations
- ✓ Performance (~100k requests/sec single instance)

### Why Next.js 15?
- ✓ Server Components (SEO + performance)
- ✓ Incremental adoption
- ✓ Built-in optimizations (images, fonts, bundles)
- ✓ Full-stack capability (API routes)
- ✓ Vercel integration (automatic deployments)

### Why PostgreSQL?
- ✓ ACID compliance (financial transactions)
- ✓ Advanced features (JSONB, arrays, full-text search)
- ✓ Reliability & maturity
- ✓ Excellent async support (asyncpg)

### Why Redis?
- ✓ Sub-millisecond latency
- ✓ Multiple use cases (cache, queue, sessions)
- ✓ Cluster support
- ✓ Persistence options

### Why Meilisearch?
- ✓ Typo tolerance
- ✓ Fast (sub-100ms)
- ✓ Easy deployment
- ✓ REST API

## Performance Targets

| Metric | Target | Notes |
|--------|--------|-------|
| Homepage Load | < 1s | Core Web Vitals |
| API Response | < 200ms | p99 |
| Search | < 100ms | Meilisearch |
| Database Query | < 50ms | p95 |
| Cache Hit Rate | > 80% | Redis |

## Future Considerations

- GraphQL API for better frontend optimization
- Event sourcing for audit trail
- CQRS for read/write separation
- Streaming APIs (WebSockets for real-time features)
- Mobile app (React Native sharing code)
- Multi-tenant support
