# AI Agents Guide

## Overview

Six autonomous AI agents power Aura Beauty's intelligence layer, handling everything from trend discovery to customer support.

## Agent Specifications

### 1. Trend Hunter Agent

**Purpose**: Autonomous discovery of trending products and market opportunities

**Schedule**: Daily at 2 AM UTC

**Data Sources**:
- TikTok API (beauty hashtags)
- Google Trends (beauty/skincare keywords)
- Amazon Best Sellers (beauty category)
- Reddit (r/skincare, r/beauty, r/makeup)
- Instagram (hashtag trends)
- Sephora website (top sellers)

**Process**:
1. Scrape data from all sources
2. Analyze trends (growth rate, mention frequency, engagement)
3. Identify profitable gaps (high demand, low competition)
4. Score products (1-100 based on profitability)
5. Store results in database
6. Alert team to top opportunities

**Output**:
```json
{
  "trends": [
    {
      "product": "Hyaluronic Acid Serum",
      "trend_score": 92,
      "growth_rate": "245% MoM",
      "mentions": 4532,
      "engagement": "8.4%",
      "profit_potential": "High",
      "recommendation": "Stock immediately"
    }
  ],
  "timestamp": "2026-05-15T02:00:00Z"
}
```

**Cost**: ~$15/month (Claude API)

---

### 2. Pricing Agent

**Purpose**: Dynamic pricing optimization with 15%+ margin guarantee

**Schedule**: Hourly

**Inputs**:
- Product cost (COGS)
- Competition pricing (scraped from Amazon, Sephora)
- Current inventory levels
- Demand signals (page views, add-to-cart)
- Historical conversion rates

**Algorithm**:
```
base_price = cost / (1 - target_margin)  // Cost-based
comp_price = average_competitor_price    // Competition-based
demand_multiplier = (demand / avg_demand) * 0.1 + 1  // Demand signal

final_price = max(
  base_price,  // Ensure minimum margin
  (comp_price - 5) * demand_multiplier  // Price competitively
)
```

**Constraints**:
- Minimum margin: 15%
- Maximum markup: 50%
- Price change limit: Max 10% per update
- Manual override: Admin can lock prices

**Output**:
```json
{
  "product_id": 123,
  "current_price": 79.99,
  "recommended_price": 89.99,
  "margin": "18.5%",
  "confidence": 0.94,
  "reason": "High demand, competitor pricing $99"
}
```

**Cost**: ~$50/month

---

### 3. SEO Content Agent

**Purpose**: High-ranking content generation for organic growth

**Schedule**: Continuous (on-demand + daily batch)

**Content Types**:

| Type | Frequency | Keyword Research | Publishing |
|------|-----------|------------------|-----------|
| Product Descriptions | Per new product | Yes | Auto to Sanity |
| Blog Posts | 3x weekly | Yes | Auto to Sanity |
| Category Pages | Monthly | Yes | Auto-generate |
| FAQ Pages | Quarterly | Yes | Auto-generate |
| Comparison Pages | On-demand | Yes | Manual review |

**SEO Optimization**:
- Keyword targeting (long-tail focus)
- Meta descriptions (<160 chars)
- Schema.org markup (Product, FAQPage, BreadcrumbList)
- Internal linking suggestions
- Readability score (Flesch-Kincaid > 60)
- Image alt text generation

**Output**:
```json
{
  "title": "Best Hyaluronic Acid Serums for Dry Skin - 2026",
  "slug": "best-hyaluronic-acid-serums-dry-skin",
  "content": "...(2000+ words optimized for SEO)...",
  "meta_description": "Discover the best hyaluronic acid serums for dry skin. Expert reviews, comparisons, and skincare tips from dermatologists.",
  "keywords": ["hyaluronic acid serum", "dry skin serum", "best face serum"],
  "schema": {...},
  "internal_links": [{"text": "skincare routine", "url": "/blog/skincare-routine-dry-skin"}]
}
```

**Cost**: ~$100/month (variable based on content volume)

---

### 4. Email Agent

**Purpose**: Autonomous email marketing and customer engagement

**Schedule**: Event-triggered + scheduled

**Campaigns**:

1. **Abandoned Cart** (1h after abandon)
   - Dynamic product recommendations
   - Discount incentive (5% off)
   - Urgency messaging

2. **Weekly Newsletter** (Every Thursday)
   - Trending products
   - Blog recommendations
   - Exclusive discounts

3. **Discount Campaigns** (Monthly)
   - Personalized offers
   - Product recommendations
   - Seasonal themes

4. **Winback Campaign** (30+ days inactive)
   - Special reactivation offer
   - "We miss you" messaging
   - New product highlights

**Personalization**:
- Product recommendations based on browsing/purchase history
- Segmentation by customer value (VIP, regular, at-risk)
- Optimal send time prediction
- Dynamic product inventory

**Provider**: Resend (transactional + marketing)

**Cost**: ~$30/month

---

### 5. Support Agent

**Purpose**: AI-powered customer service with human escalation

**Schedule**: 24/7 real-time

**Capabilities**:

| Query Type | Resolution | Escalation |
|-----------|-----------|-----------|
| Order tracking | Auto (from database) | If order missing |
| Returns/Refunds | FAQ-based | Always to human |
| Product questions | Product info + reviews | Complex questions |
| Account issues | Account lookup | Sensitive issues |
| General questions | Knowledge base | Complex issues |

**Workflow**:
1. User asks question via chat
2. Agent analyzes intent
3. Search knowledge base (fine-tuned on past tickets)
4. Provide answer with confidence score
5. If confident < 70% or flagged, escalate to human
6. Human agent takes over with full context
7. Resolution logged for future training

**Training Data**: Last 2 years of support tickets (fine-tuned model)

**Cost**: ~$40/month

---

### 6. Analytics Agent

**Purpose**: Autonomous business insights and anomaly detection

**Schedule**: Hourly metrics + Daily reports + Weekly summaries

**Metrics Tracked**:

**Revenue**:
- Daily/Weekly/Monthly revenue
- Revenue by product category
- Revenue by source (organic, paid, direct)
- Customer lifetime value (CLV)

**Conversion**:
- Conversion rate (visitor → customer)
- Cart abandonment rate
- Product page bounce rate
- Checkout dropout rate

**Cost**:
- Customer acquisition cost (CAC)
- Marketing spend by channel
- Return on ad spend (ROAS)

**Inventory**:
- Stock levels by product
- Slow-moving products
- High-demand items
- Inventory turnover

**Performance**:
- Page load time
- API response time
- Search quality metrics
- Error rates

**Anomaly Detection**:
- Revenue drop > 20% (Alert)
- Conversion rate drop > 15% (Alert)
- Error rate spike (Auto-investigate)
- Unusual traffic patterns (Flag for review)

**Output**:
```json
{
  "timestamp": "2026-05-15",
  "metrics": {
    "revenue_today": "$12,450",
    "revenue_vs_avg": "+34%",
    "conversion_rate": "3.2%",
    "cac": "$28",
    "clv": "$450",
    "anomalies": [
      {
        "metric": "search_response_time",
        "value": "850ms",
        "normal_range": "50-100ms",
        "severity": "high",
        "recommendation": "Investigate Meilisearch performance"
      }
    ],
    "recommendations": [
      "Restock high-demand items ASAP",
      "Consider increasing paid ad spend for high-ROAS campaigns"
    ]
  }
}
```

**Cost**: ~$20/month

---

## Agent Orchestration

### Execution Flow

```
┌─────────────────────────────────┐
│  Manual Trigger or Schedule      │
└────────────┬────────────────────┘
             │
    ┌────────▼────────┐
    │ Celery Beat     │
    │ (Scheduler)     │
    └────────┬────────┘
             │
    ┌────────▼──────────────────┐
    │ Celery Worker Queue       │
    └────────┬──────────────────┘
             │
    ┌────────▼──────────────────────────┐
    │ Agent (LangChain/CrewAI)          │
    │ - Load prompt template            │
    │ - Initialize tools                │
    │ - Execute with context/memory     │
    └────────┬──────────────────────────┘
             │
    ┌────────▼────────────────────┐
    │ Tools (API calls)           │
    │ - External APIs             │
    │ - Database queries          │
    │ - Scraping/Data processing  │
    └────────┬────────────────────┘
             │
    ┌────────▼────────────────┐
    │ Store Results           │
    │ - Database              │
    │ - Logs                  │
    │ - Notifications         │
    └────────────────────────┘
```

### Monitoring Agents

```bash
# View active agents
celery -A app.tasks inspect active

# Recent agent logs
curl http://localhost:8000/api/v1/agents/logs?limit=50

# Agent cost today
curl http://localhost:8000/api/v1/agents/costs/today

# Agent performance
curl http://localhost:8000/api/v1/agents/stats
```

---

## Cost Optimization

### Multi-Provider Strategy

```python
# Try providers in order
try:
    result = claude_api_call(prompt)
except APIError:
    try:
        result = openai_api_call(prompt)
    except APIError:
        result = gemini_api_call(prompt)
```

**Estimated Monthly Costs**:
| Agent | Claude | OpenAI | Gemini | Used |
|-------|--------|--------|--------|------|
| Trend | $15 | - | - | Claude |
| Pricing | $50 | - | - | Claude |
| SEO | $80 | $20 | - | Claude (fallback OpenAI) |
| Email | $25 | $5 | - | Gemini |
| Support | $35 | $5 | - | Claude (fallback) |
| Analytics | $20 | - | - | Gemini |
| **Total** | **$225** | **$30** | **$0** | **~$250** |

---

## Prompt Engineering

### Template Structure

```markdown
SYSTEM_ROLE: You are an expert [domain] agent...

TASK_DEFINITION:
Your goal is to [specific task]...

CONTEXT:
- Input data: [fields]
- External data: [sources]
- Constraints: [limits]

TOOLS:
You have access to:
- [tool_name]: [description]
- [tool_name]: [description]

OUTPUT_FORMAT:
Return JSON with fields:
- [field]: [description]
- [field]: [description]

EXAMPLES:
Example 1: [input] → [output]
Example 2: [input] → [output]

QUALITY_CRITERIA:
- [criterion]
- [criterion]
```

---

## Troubleshooting

### Agent Failed

```bash
# Check logs
curl http://localhost:8000/api/v1/agents/logs?agent=trend_hunter&status=failed

# Retry manually
curl -X POST http://localhost:8000/api/v1/agents/trend-hunter/run

# Check error message
docker-compose logs celery_worker | grep "trend"
```

### Agent Slow

Check execution time:
```bash
curl http://localhost:8000/api/v1/agents/stats
```

Optimize:
- Reduce data fetching
- Use caching for external APIs
- Parallelize tasks with Celery group/chain

### High Cost

Monitor spend:
```bash
# Daily spend
curl http://localhost:8000/api/v1/agents/costs/today

# By agent
curl http://localhost:8000/api/v1/agents/costs/by-agent
```

Reduce:
- Use cheaper models (OpenAI/Gemini)
- Cache results (avoid re-processing)
- Batch operations
- Reduce prompt verbosity

---

## Future Enhancements

- [ ] Multi-language support for agents
- [ ] Fine-tuned models for domain specificity
- [ ] Collaborative multi-agent workflows
- [ ] Real-time learning from feedback
- [ ] Cost prediction and optimization
- [ ] Agent A/B testing
- [ ] Distributed agent execution
