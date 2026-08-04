# Standard Operating Procedures (SOP)

## Development Workflow

### 1. Local Setup

```bash
# Clone repo
cd ~/Projects/aura-beauty-ai-commerce

# Copy env file
cp .env.example .env.local

# Start Docker services
docker-compose up -d

# Frontend setup
cd frontend && npm install && npm run dev

# Backend setup (new terminal)
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload

# AI Agents (new terminal)
cd backend
celery -A app.tasks worker --loglevel=info
```

### 2. Making Changes

**Code Standards**:
- TypeScript strict mode (frontend)
- Type hints everywhere (backend)
- Async/await (not .then())
- Error handling at boundaries
- No console.logs in production code
- Max 80 lines per function

**Naming**:
- Components: PascalCase
- Files: kebab-case
- Database: snake_case
- API endpoints: /api/v1/resource/action
- Variables: camelCase (JS/TS), snake_case (Python)

**Testing**:
```bash
# Frontend
npm run test              # Jest
npm run test:watch       # Watch mode
npm run test:e2e         # Playwright

# Backend
python -m pytest         # All tests
python -m pytest tests/integration  # Integration only
pytest --cov=app         # Coverage report
```

### 3. Git Workflow

```bash
# Create feature branch
git checkout -b feat/feature-name

# Make commits following convention
git commit -m "[feat]: add user authentication"  # [type]: description
# Types: feat, fix, docs, style, refactor, test, chore

# Push and create PR
git push origin feat/feature-name

# On PR:
# - All tests must pass
# - 80%+ code coverage
# - At least 1 approval
# - CLAUDE.md updated if significant changes
```

**Commit Message Format**:
```
[type]: brief description (present tense, lowercase)

Optional longer explanation of why this change is needed.
Mention any related issues: fixes #123
```

### 4. Code Review Checklist

- [ ] Code follows project standards
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No console.logs or debug code
- [ ] No hardcoded secrets
- [ ] Performance impact assessed
- [ ] Backward compatible (if API change)
- [ ] CLAUDE.md updated

## Database Management

### 1. Creating Migrations

```bash
cd backend

# Generate migration from model changes
alembic revision --autogenerate -m "Add user preferences table"

# Review migration file
vim migrations/versions/xxx_add_user_preferences_table.py

# Apply migration
alembic upgrade head

# Verify
psql aura_beauty_db -c "\dt"  # List tables
```

### 2. Backups

```bash
# Daily backup (automatic via AWS RDS)

# Manual backup
pg_dump aura_beauty_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore from backup
psql aura_beauty_db < backup_20260515_120000.sql
```

### 3. Connection Management

```bash
# Connect to local database
psql -U aura_user -d aura_beauty_db

# Connect via Docker
docker-compose exec db psql -U aura_user -d aura_beauty_db

# Connection pooling
# PgBouncer (future): max_client_conn = 1000, default_pool_size = 25
```

## Deployment Process

### 1. Staging Deployment

```bash
# From main branch
git push origin feat/feature-name  # Push your feature branch

# GitHub Actions automatically:
# 1. Runs tests
# 2. Builds Docker images
# 3. Pushes to ECR
# 4. Deploys to staging ECS
# 5. Runs health checks

# Test at https://staging.aurabeauty.com
```

### 2. Production Deployment

```bash
# Only from main branch
git tag v0.2.0      # Semantic versioning
git push origin v0.2.0

# GitHub Actions:
# 1. Run full test suite
# 2. Build production images
# 3. Deploy frontend to Vercel
# 4. Deploy backend to ECS (auto-scaling)
# 5. Run smoke tests
# 6. Alert team on slack

# Monitor at https://aurabeauty.com
# Metrics: New Relic, Grafana
```

### 3. Rollback Procedure

```bash
# If production issue
git revert <commit-hash>
git push origin main

# Or deploy previous tag
git checkout v0.1.9
git push origin HEAD:main -f  # CAUTION: force push only in emergency

# Verify rollback
curl https://aurabeauty.com/api/v1/health
```

## Monitoring & Alerting

### 1. Health Checks

**Frontend**:
- Lighthouse score (> 90 for all metrics)
- Core Web Vitals
- Error rate (< 0.1%)

**Backend**:
- /health endpoint (< 100ms)
- Database connection pool
- Redis connection
- Error rate (< 0.05%)

**Database**:
- Connection pool utilization (< 80%)
- Query performance (p99 < 50ms)
- Replication lag (< 100ms)

### 2. Alerts

| Condition | Threshold | Action |
|-----------|-----------|--------|
| API Error Rate | > 1% | Slack + On-call |
| Database Down | Any | PagerDuty |
| Response Time | p99 > 2s | Slack |
| Memory Usage | > 85% | Auto-scale |
| Disk Usage | > 90% | Alert |

### 3. Incident Response

```
1. Alert fires → Slack notification
2. On-call acknowledges → PagerDuty
3. Diagnose issue
   - Check logs: New Relic
   - Check metrics: Grafana
   - Check database: CloudWatch
4. Apply fix or rollback
5. Verify recovery
6. Post-mortem within 24h
```

## Agent Management

### 1. Running Agents

**Manually Trigger**:
```bash
curl -X POST http://localhost:8000/api/v1/agents/trend-hunter/run
curl -X POST http://localhost:8000/api/v1/agents/pricing/run
curl -X POST http://localhost:8000/api/v1/agents/seo-content/run
curl -X POST http://localhost:8000/api/v1/agents/email/run
curl -X POST http://localhost:8000/api/v1/agents/analytics/run
```

**View Logs**:
```bash
# Recent executions
curl http://localhost:8000/api/v1/agents/logs

# Specific agent logs
curl http://localhost:8000/api/v1/agents/logs?agent=trend_hunter

# Failed executions
curl http://localhost:8000/api/v1/agents/logs?status=failed
```

### 2. Scheduled Execution

**Celery Beat Schedule** (configured in backend):
- Trend Hunter: Daily 2 AM UTC
- Pricing: Hourly
- SEO Content: Continuous (on-demand)
- Email: Event-triggered
- Support: Real-time
- Analytics: Hourly + Daily

### 3. Agent Costs

Monitor daily spend:
```bash
curl http://localhost:8000/api/v1/agents/costs/today
curl http://localhost:8000/api/v1/agents/costs/month
```

## Content Management

### 1. Publishing Blog Post

```bash
# Via Sanity Studio (https://sanity.aurabeauty.com)

# Or via API
curl -X POST http://localhost:8000/api/v1/blog \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "10 Skincare Tips for Oily Skin",
    "slug": "skincare-tips-oily-skin",
    "content": "...",
    "author": "...",
    "tags": ["skincare", "oily-skin"]
  }'
```

### 2. Creating Product Listing

```bash
# Via admin dashboard
# Or bulk import
curl -X POST http://localhost:8000/api/v1/admin/products/import \
  -F "file=@products.csv"
```

## Troubleshooting

### Frontend Issues

```bash
# Clear build cache
rm -rf .next
npm run build

# Check env variables
echo $NEXT_PUBLIC_API_URL

# Check browser console for errors
# F12 → Console tab
```

### Backend Issues

```bash
# Check logs
docker-compose logs -f backend

# Test API directly
curl http://localhost:8000/health

# Check database connection
docker-compose exec db psql -U aura_user -d aura_beauty_db -c "SELECT 1"

# Check Redis
docker-compose exec cache redis-cli ping
```

### Agent Issues

```bash
# Check Celery worker
docker-compose logs -f celery_worker

# List active tasks
celery -A app.tasks inspect active

# Clear failed tasks
celery -A app.tasks purge
```

## Performance Optimization

### Frontend

```bash
# Analyze bundle size
npm run analyze

# Check Core Web Vitals
npm run test  # Lighthouse testing

# Optimize images
# Use next/image for automatic optimization
```

### Backend

```bash
# Profile slow queries
# PostgreSQL slow query log

# Check database indexes
psql aura_beauty_db -c "\di+"

# Monitor Redis usage
redis-cli info stats
```

## Security Checklist

- [ ] Secrets in .env (not in code)
- [ ] HTTPS enforced everywhere
- [ ] CORS properly configured
- [ ] Rate limiting enabled
- [ ] SQL injection prevention (ORM usage)
- [ ] XSS protection (React escaping)
- [ ] CSRF tokens on state-changing operations
- [ ] Password hashing (bcrypt)
- [ ] API authentication (JWT/Clerk)
- [ ] Audit logging enabled
- [ ] Regular dependency updates
- [ ] Security scanning in CI/CD

## Release Checklist

- [ ] Version bump (MAJOR.MINOR.PATCH)
- [ ] CHANGELOG.md updated
- [ ] CLAUDE.md updated
- [ ] All tests passing
- [ ] Code review approved
- [ ] Deployment guide documented
- [ ] Rollback plan documented
- [ ] Stakeholders notified
- [ ] Release notes prepared
- [ ] Health checks verified post-deployment
