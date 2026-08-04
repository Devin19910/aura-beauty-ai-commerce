# Deployment Guide

## Development Deployment

### Local Setup

```bash
# Clone repo
cd ~/Projects/aura-beauty-ai-commerce

# Copy environment
cp .env.example .env.local

# Start all services
docker-compose up -d

# Initialize database
docker-compose exec backend alembic upgrade head

# Check services
docker-compose ps

# Access services
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Meilisearch: http://localhost:7700
- PostgreSQL: localhost:5432
- Redis: localhost:6379
```

## Staging Deployment

### Automatic via GitHub Actions

**Trigger**: Push to any branch

**Process**:
1. Run linting & tests
2. Build Docker images
3. Push to ECR (Elastic Container Registry)
4. Deploy backend to ECS staging cluster
5. Deploy frontend to Vercel preview
6. Run smoke tests
7. Post results to pull request

**Access**:
- Frontend: https://staging.aurabeauty.com
- API: https://api-staging.aurabeauty.com

### Manual Staging Deploy

```bash
# From staging branch
git checkout staging
git pull origin staging

# Build images locally
docker build -t aura-beauty-frontend:latest ./frontend
docker build -t aura-beauty-backend:latest ./backend

# Push to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

docker tag aura-beauty-backend:latest \
  $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/aura-backend:staging

docker push $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/aura-backend:staging

# Update ECS service
aws ecs update-service \
  --cluster aura-staging \
  --service aura-backend \
  --force-new-deployment
```

## Production Deployment

### Automatic via GitHub Actions

**Trigger**: Push to `main` branch with version tag

**Example**:
```bash
git tag v0.2.0
git push origin v0.2.0
```

**GitHub Actions Workflow**:
1. Run full test suite
2. Build production Docker images
3. Run OWASP security scan
4. Push to ECR with `latest` and version tag
5. Deploy frontend to Vercel production
6. Deploy backend to ECS production (blue/green deployment)
7. Run health checks
8. Run smoke tests
9. Post deployment summary to Slack

### Frontend Deployment (Vercel)

**Configuration**: `.vercelrc.json`

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "out",
  "env": [
    "NEXT_PUBLIC_API_URL",
    "NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY",
    "STRIPE_PUBLISHABLE_KEY"
  ]
}
```

**Features**:
- Automatic deployments on git push
- Preview URLs for pull requests
- Environment variables per environment
- Automatic SSL certificates
- CDN & edge caching

**Deployment Time**: ~2 minutes

### Backend Deployment (ECS + CloudFormation)

**Infrastructure**:
```
Application Load Balancer (ALB)
  ↓
ECS Service (auto-scaling 2-10 instances)
  ↓
RDS PostgreSQL (Multi-AZ)
  ├── ElastiCache Redis (cluster)
  ├── Meilisearch (EC2 instances)
  └── Secrets Manager (credentials)
```

**Deployment Strategy**: Blue/Green

```
1. Create new "green" service with new image
2. Route traffic: 0% → green, 100% → blue
3. Health checks: Ensure green is healthy
4. Shift traffic: 50% → green, 50% → blue
5. Shift traffic: 100% → green, 0% → blue
6. Destroy blue service after 24h
```

**Rollback**:
If green is unhealthy, automatically revert to blue (instant).

**Deployment Time**: ~5 minutes

### Database Migration (Production)

**Before Deployment**:
1. Backup database
2. Test migrations on staging database
3. Plan rollback procedure
4. Schedule during low-traffic window

**During Deployment**:
```bash
# Connect to production database
docker-compose exec backend \
  alembic upgrade head
```

**After Deployment**:
1. Run health checks
2. Monitor error rates (alert if > 0.1%)
3. Check database performance (alert if p99 > 2s)

### Zero-Downtime Deployment

**Strategy**:
1. Deploy new code (handles both old & new database schema)
2. Run database migrations
3. Deploy final code (uses only new schema)

**Example**: Adding new column

```sql
-- Migration 1: Add column as nullable
ALTER TABLE users ADD COLUMN new_field VARCHAR(100) DEFAULT '';

-- Code update: Handle both with/without new field
if 'new_field' in user_dict:
    user.new_field = user_dict['new_field']

-- Migration 2: Make column not null (if needed)
ALTER TABLE users ALTER COLUMN new_field SET NOT NULL;
```

---

## Environment Configuration

### Development

```env
ENVIRONMENT=development
DEBUG=True
DATABASE_URL=postgresql://aura_user:aura_password@db:5432/aura_beauty_db
LOG_LEVEL=DEBUG
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
```

### Staging

```env
ENVIRONMENT=staging
DEBUG=False
DATABASE_URL=postgresql://aura_user:***@aura-db-staging.xyz.us-east-1.rds.amazonaws.com:5432/aura_beauty_db
LOG_LEVEL=INFO
ALLOWED_ORIGINS=https://staging.aurabeauty.com,https://api-staging.aurabeauty.com
```

### Production

```env
ENVIRONMENT=production
DEBUG=False
DATABASE_URL=postgresql://aura_user:***@aura-db.xyz.us-east-1.rds.amazonaws.com:5432/aura_beauty_db
LOG_LEVEL=WARNING
ALLOWED_ORIGINS=https://aurabeauty.com,https://www.aurabeauty.com,https://api.aurabeauty.com
```

---

## Monitoring Post-Deployment

### Health Checks

```bash
# Frontend
curl https://aurabeauty.com

# API
curl https://api.aurabeauty.com/health

# Database
SELECT 1;

# Redis
redis-cli ping

# Meilisearch
curl https://search.aurabeauty.com/health
```

### Key Metrics

| Metric | Alert Level | Check |
|--------|------------|-------|
| API Response Time (p99) | > 2 seconds | New Relic |
| Error Rate | > 0.1% | New Relic |
| Database Connections | > 80% | RDS CloudWatch |
| Disk Usage | > 80% | RDS CloudWatch |
| Memory Usage | > 85% | ECS CloudWatch |

### Logs

```bash
# Backend logs
aws logs tail /ecs/aura-backend --follow

# Database slow query log
SELECT * FROM pg_stat_statements ORDER BY mean_time DESC;

# Error tracking
curl https://sentry.io/api/0/organizations/aura/events/
```

---

## Rollback Procedure

### Frontend Rollback

```bash
# Using Vercel UI:
1. Go to Vercel Dashboard
2. Select aura-beauty-frontend project
3. Click "Deployments"
4. Find previous deployment
5. Click "..." menu
6. Click "Promote to Production"
```

### Backend Rollback

```bash
# ECS Blue/Green Automatic:
If new deployment (green) fails:
- Traffic automatically reverts to previous (blue)
- ECS replaces unhealthy instances
- Automatic rollback completed

# Manual Rollback:
aws ecs update-service \
  --cluster aura-production \
  --service aura-backend \
  --force-new-deployment \
  --task-definition aura-backend:v0.1.9
```

### Database Rollback

```bash
# If migration fails:
alembic downgrade -1  # Revert previous migration

# If data corruption:
# Restore from backup
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier aura-beauty-db \
  --db-snapshot-identifier aura-beauty-db-backup-20260515
```

---

## Performance Tuning

### Frontend

```javascript
// next.config.js
export const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
});

// Analyze bundle size
ANALYZE=true npm run build
```

### Backend

```python
# Enable query caching
from fastapi_cache2 import FastAPICache2
from fastapi_cache2.backends.redis import RedisBackend

@router.get("/products")
@cached(expire=300)  # Cache for 5 minutes
async def list_products():
    ...
```

### Database

```sql
-- Add indexes for common queries
CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_products_created_at ON products(created_at);

-- Enable query execution plans
EXPLAIN ANALYZE SELECT * FROM products WHERE category = 'skincare';
```

---

## Disaster Recovery

### Backup Strategy

- **Database**: Continuous with 35-day retention
- **Code**: Git repository (GitHub)
- **Assets**: S3 with versioning
- **Configuration**: Secrets Manager with versioning

### Recovery Scenarios

**Scenario 1: Database Down**
1. Failover to read replica (automatic, < 1 minute)
2. If multi-AZ replication fails, restore from latest snapshot
3. ETA: < 5 minutes downtime

**Scenario 2: Production Server Down**
1. Load balancer routes to healthy instances (automatic)
2. Auto-scaling replaces failed instances
3. ETA: < 2 minutes recovery

**Scenario 3: Datacenter Failure**
1. Traffic routes to secondary region (Route 53 failover)
2. Database restored from cross-region backup
3. ETA: < 15 minutes recovery
4. Need manual verification

### Testing Backups

**Monthly**:
```bash
# Restore backup to staging
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier aura-beauty-test \
  --db-snapshot-identifier aura-beauty-db-20260515

# Run tests
npm run test:e2e

# Verify data integrity
SELECT COUNT(*) FROM users;  # Should match production count
```

---

## Deployment Checklist

### Before Deployment

- [ ] Tests passing (local & CI)
- [ ] Code reviewed & approved
- [ ] CLAUDE.md updated
- [ ] CHANGELOG.md updated
- [ ] Database migrations tested
- [ ] Environment variables configured
- [ ] Monitoring alerts configured
- [ ] Rollback plan documented
- [ ] Stakeholders notified

### During Deployment

- [ ] Monitor deployment progress
- [ ] Check health check status
- [ ] Monitor error rates
- [ ] Monitor performance metrics
- [ ] Test critical functionality

### After Deployment

- [ ] Verify all health checks passing
- [ ] Check error rates (< 0.1%)
- [ ] Check response times (< 2s p99)
- [ ] Test user-facing features
- [ ] Monitor logs for errors
- [ ] Post notification to team

---

## Emergency Procedures

### If Production is Down

1. **Alert**: PagerDuty notifies on-call engineer (automatic)
2. **Triage**: Check metrics, logs, system status
3. **Investigate**: Root cause analysis
4. **Action**: Fix code, revert deployment, or restore backup
5. **Recovery**: Verify system restored
6. **Communication**: Update status page every 5 minutes
7. **Post-mortem**: Schedule within 24 hours

### If Data is Corrupted

1. **Contain**: Stop writes (set database to read-only)
2. **Assess**: Determine scope of corruption
3. **Notify**: Legal/compliance team
4. **Restore**: Restore from latest clean backup
5. **Notify Users**: Communicate impact transparently
6. **Audit**: Review what happened
7. **Fix**: Implement preventative measures

### Escalation Path

Level 1 (Sev 2): On-call engineer
Level 2 (Sev 1): Engineering lead + ops lead
Level 3 (Sev 0): VP Engineering + CTO + Legal

