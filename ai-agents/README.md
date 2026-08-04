# Aura Beauty AI Agents

Autonomous AI agent system for ecommerce intelligence, content generation, and automation.

## Agents Overview

### 1. Trend Hunter Agent
Discovers trending beauty products and market opportunities.

- **Schedule**: Daily (2 AM UTC)
- **Data Sources**: TikTok, Google Trends, Amazon BSR, Reddit, Instagram, Sephora
- **Output**: JSON with trending products, trend scores, market gaps
- **Cost**: ~$0.50/day (Claude API)

### 2. Pricing Agent
Dynamic pricing optimization with margin management.

- **Schedule**: Hourly
- **Inputs**: Product cost, competition data, inventory levels, demand signals
- **Algorithm**: Cost-based + Competition-based + Demand-based
- **Constraints**: Minimum 15% margin, maximum 50% markup

### 3. SEO Content Agent
High-ranking content generation for organic growth.

- **Schedule**: Continuous (on-demand + scheduled)
- **Content Types**: Product descriptions, Blog posts, FAQs, Comparisons, Category pages
- **Publishing**: Direct to Sanity CMS
- **SEO**: Keyword targeting, schema.org markup, readability optimization

### 4. Email Agent
Autonomous email marketing and customer engagement.

- **Schedule**: Event-triggered + scheduled
- **Campaigns**: Abandoned cart, discount promotions, newsletters, winback
- **Personalization**: Product recommendations, browsing history, purchase patterns
- **Provider**: Resend

### 5. Support Agent
AI customer service with human escalation.

- **Schedule**: 24/7 real-time
- **Capabilities**: FAQ, order tracking, returns, product recommendations
- **Training**: Fine-tuned on historical support tickets
- **Escalation**: Automatic handoff with full context

### 6. Analytics Agent
Business insights and anomaly detection.

- **Schedule**: Hourly reports + Daily summaries
- **Metrics**: Revenue, conversion rate, CAC, LTV, AOV, bounce rate
- **Alerts**: Real-time anomaly detection
- **Reports**: Executive dashboards, trend analysis

## Architecture

```
ai-agents/
├── agents/                    # Individual agent implementations
│   ├── trend_hunter/
│   ├── pricing/
│   ├── seo_content/
│   ├── email_agent/
│   ├── support/
│   └── analytics/
├── orchestration/            # Agent coordination and scheduling
├── prompts/                  # LLM prompt templates
├── memory/                   # Persistent agent memory
├── utils/                    # Shared utilities
└── celery_tasks.py          # Background job definitions
```

## Running Agents Locally

```bash
# Start Celery worker
celery -A app.tasks worker --loglevel=info

# Start Celery beat (scheduler)
celery -A app.tasks beat --loglevel=info

# Trigger agent manually (from backend)
curl -X POST http://localhost:8000/api/v1/agents/trend-hunter/run
```

## Environment Variables

See backend `.env.example` for all required AI provider keys:
- `CLAUDE_API_KEY`
- `OPENAI_API_KEY`
- `GEMINI_API_KEY`
- `RESEND_API_KEY`

## Cost Optimization

**Multi-Provider Strategy**:
1. Try Claude (most capable)
2. Fallback to OpenAI (faster)
3. Fallback to Gemini (cheapest)

**Estimated Monthly Costs**:
- Trend Hunter: $15/month
- Pricing Agent: $50/month
- SEO Content: $100/month (variable)
- Email Agent: $30/month
- Support Agent: $40/month
- Analytics Agent: $20/month
- **Total**: ~$250/month

## Monitoring

Each agent logs execution details:
- Execution time
- Input/output
- Cost
- Errors
- Results

View logs: `curl http://localhost:8000/api/v1/agents/logs`

## Future Enhancements

- [ ] Multi-language support
- [ ] Real-time learning from feedback
- [ ] Collaborative multi-agent workflows
- [ ] Fine-tuned models for domain specificity
- [ ] Agentic memory systems
- [ ] Dynamic prompt optimization
