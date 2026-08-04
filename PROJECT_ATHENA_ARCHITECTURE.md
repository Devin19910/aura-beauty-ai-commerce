# PROJECT ATHENA: Multi-Agent Architecture (Option B)
## Complete Technical Design

**Status**: Ready for Implementation  
**Timeline**: 6-8 weeks  
**Complexity**: Advanced Multi-Agent Orchestration  
**Scope**: 4-5 autonomous agents working 24/7

---

## ARCHITECTURE OVERVIEW

```
┌──────────────────────────────────────────────────────────────┐
│                    ORCHESTRATION LAYER                        │
│  (CrewAI / AutoGen - Manages agent workflows)                │
└──────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┼─────────────┐
                │             │             │
          ┌─────▼─────┐ ┌────▼─────┐ ┌───▼──────┐
          │ Scheduler │ │ Message  │ │ Executor │
          │(Celery)   │ │ Queue    │ │(Runner)  │
          │           │ │(Redis)   │ │          │
          └───────────┘ └──────────┘ └──────────┘
                │
    ┌───────────┼───────────┬──────────────┐
    │           │           │              │
┌───▼──┐  ┌────▼────┐ ┌───▼────┐  ┌────▼────┐
│Agent1│  │ Agent 2 │ │Agent 3 │  │ Agent 4 │
│Res.  │  │Supplier │ │Validat.│  │Scoring  │
│      │  │         │ │        │  │         │
└──┬───┘  └────┬────┘ └───┬────┘  └────┬────┘
   │           │          │            │
   └───────────┼──────────┼────────────┘
               │
        ┌──────▼──────┐
        │   Memory    │
        │ (PostgreSQL)│
        │ + Cache     │
        │ (Redis)     │
        └──────┬──────┘
               │
        ┌──────▼──────────┐
        │   Dashboard     │
        │ (Next.js + WS)  │
        └─────────────────┘
```

---

## AGENT ARCHITECTURE (Detailed)

### AGENT 1: Research Intelligence Agent
**Primary API**: OpenAI (ChatGPT) - Fast web analysis  
**Secondary API**: Claude - If complex reasoning needed  
**Fallback**: Gemini

```
ResearchAgent:
├── Responsibilities
│   ├── Scrape Amazon best-sellers (Beauty category)
│   ├── Extract product data (name, price, rating, reviews)
│   ├── Analyze Google Trends
│   ├── Identify market gaps
│   ├── Create product dataset
│   └── Communicate findings to Supplier Agent
│
├── Inputs
│   └── None (self-initiated, scheduled daily)
│
├── Outputs
│   ├── products[] = {
│   │   id, name, asin, amazon_price, rating,
│   │   reviews, category, keywords, trend_score
│   │ }
│   └── message_to_supplier_agent = "Found 500 products"
│
├── Self-Testing
│   ├── Validate: len(products) > 100
│   ├── Validate: All products have required fields
│   ├── Validate: Prices are reasonable (5-500)
│   └── Auto-retry if validation fails
│
└── Error Handling
    ├── Amazon scrape fails? → Try AliExpress
    ├── Missing data? → Log & continue
    ├── API error? → Retry with backoff
    └── Alert human if: 3 retries fail
```

**Code Structure**:
```
ai-agents/agents/research/
├── __init__.py
├── agent.py (main Research Agent)
├── scrapers/
│   ├── amazon_scraper.py
│   ├── aliexpress_scraper.py
│   ├── google_trends.py
│   └── reddit_monitor.py
├── processors/
│   ├── data_cleaner.py
│   └── trend_analyzer.py
├── validators/
│   └── data_validator.py
├── prompts/
│   └── research_prompt.txt
└── tests/
    ├── test_scrapers.py
    ├── test_processors.py
    └── test_validators.py
```

---

### AGENT 2: Supplier Intelligence Agent
**Primary API**: Claude - Complex reasoning, data synthesis  
**Secondary API**: ChatGPT - If fast analysis needed  
**Fallback**: Gemini

```
SupplierAgent:
├── Responsibilities
│   ├── Parse product data from Research Agent
│   ├── Find Alibaba suppliers (3-5 per product)
│   ├── Extract supplier metrics (MOQ, price, rating, shipping)
│   ├── Compare suppliers using weighted scoring
│   ├── Rank suppliers by: price, reliability, speed
│   ├── Communicate with Research Agent if data needed
│   └── Send findings to Validation Agent
│
├── Inputs
│   └── Message from Research Agent: products[]
│
├── Outputs
│   ├── suppliers[] = {
│   │   product_id, supplier_name, alibaba_id,
│   │   moq, unit_price, shipping_days,
│   │   rating, defect_rate, supplier_score
│   │ }
│   └── message_to_validation_agent = "Scored 150 suppliers"
│
├── Self-Testing
│   ├── Validate: Each product has 3+ suppliers
│   ├── Validate: No duplicate suppliers
│   ├── Cross-check: Prices reasonable for category
│   └── Flag: Suppliers with 0 reviews
│
└── Inter-Agent Communication
    ├── IF missing_data → message Research Agent
    ├── Research Agent responds → Continue analysis
    ├── IF data_quality_issue → Ask for re-analysis
    └── ELSE → Send to Validation Agent
```

**Code Structure**:
```
ai-agents/agents/supplier/
├── __init__.py
├── agent.py
├── scrapers/
│   ├── alibaba_scraper.py
│   └── alibaba_parser.py
├── scorers/
│   ├── supplier_scorer.py
│   └── moq_analyzer.py
├── comparators/
│   └── supplier_comparison.py
├── prompts/
│   └── supplier_analysis_prompt.txt
└── tests/
    ├── test_scrapers.py
    ├── test_scorers.py
    └── test_comparators.py
```

---

### AGENT 3: Validation & Risk Agent
**Primary API**: Gemini - Fact-checking, verification  
**Secondary API**: Claude - Risk analysis  
**Fallback**: ChatGPT

```
ValidationAgent:
├── Responsibilities
│   ├── Cross-check Research data vs live Amazon
│   ├── Verify supplier ratings (check for fake reviews)
│   ├── Confirm market demand (Google Trends validation)
│   ├── Identify red flags (complaints, low ratings, etc.)
│   ├── Risk-score each product (1-100)
│   ├── Flag suspicious products
│   └── Send validated data to Scoring Agent
│
├── Inputs
│   ├── products[] from Research Agent
│   └── suppliers[] from Supplier Agent
│
├── Outputs
│   ├── validated_products[] = {
│   │   ...all product fields...,
│   │   is_valid (bool),
│   │   risk_score (0-100),
│   │   red_flags[]
│   │ }
│   └── message_to_scoring_agent = "Validated 47/50 products"
│
├── Self-Testing
│   ├── Validate: No products with risk_score > 80
│   ├── Flag: All red flags documented
│   ├── Cross-check: Supplier ratings match Alibaba live
│   └── Alert: If >20% products flagged as risky
│
└── Quality Assurance
    ├── IF supplier_has_0_reviews → Flag as risky
    ├── IF product_price_dropped_30% → Investigate
    ├── IF competitor_count_doubled → Alert
    └── ELSE → Mark as validated
```

**Code Structure**:
```
ai-agents/agents/validation/
├── __init__.py
├── agent.py
├── validators/
│   ├── amazon_validator.py
│   ├── supplier_validator.py
│   └── trend_validator.py
├── risk_scorers/
│   ├── risk_calculator.py
│   └── red_flag_detector.py
├── prompts/
│   └── validation_prompt.txt
└── tests/
    ├── test_validators.py
    └── test_risk_scorers.py
```

---

### AGENT 4: Product Scoring & Recommendation Agent
**Primary API**: Claude - Complex multi-dimensional math  
**Secondary API**: ChatGPT - If fast calculation needed  
**Fallback**: Gemini

```
ScoringAgent:
├── Responsibilities
│   ├── Calculate profit margins (Alibaba → Amazon → Profit)
│   ├── Calculate ROI per product
│   ├── Score on 7 dimensions (weights: 25%, 20%, 20%, 15%, 10%, 5%, 5%)
│   │   ├─ 1. Profit Potential (25%)
│   │   ├─ 2. Competition Level (20%)
│   │   ├─ 3. Market Trend (20%)
│   │   ├─ 4. Customer Sentiment (15%)
│   │   ├─ 5. Repeat Purchase (10%)
│   │   ├─ 6. Brandability (5%)
│   │   └─ 7. Supply Chain (5%)
│   ├── Rank products 1-100
│   ├── Create executive summary
│   ├── Store final recommendations
│   └── Trigger dashboard update
│
├── Inputs
│   └── validated_products[] + suppliers[] from Validation Agent
│
├── Outputs
│   ├── scored_products[] = {
│   │   ...all fields...,
│   │   profit_margin (%),
│   │   roi (%),
│   │   scores {profit, competition, trend, sentiment, repeat, brand, supply},
│   │   final_score (0-100),
│   │   rank (1, 2, 3, ...),
│   │   recommendation_reason (text),
│   │   confidence (0-100%)
│   │ }
│   └── Dashboard update: Triggers real-time refresh
│
├── Self-Testing
│   ├── Validate: All products have all scores
│   ├── Validate: final_score is weighted sum
│   ├── Validate: Ranks are sequential (no duplicates)
│   ├── Cross-check: Top 5 products make intuitive sense
│   └── Alert: If top product risk_score was high
│
└── Output Format
    ├── TOP 5 Recommendations
    ├── Detailed analysis per product
    ├── Risk flags highlighted
    └── Next action steps (contact supplier, order sample, etc.)
```

**Code Structure**:
```
ai-agents/agents/scoring/
├── __init__.py
├── agent.py
├── calculators/
│   ├── profit_calculator.py
│   ├── roi_calculator.py
│   └── fee_calculator.py
├── scorers/
│   ├── dimension_scorer.py
│   ├── competition_scorer.py
│   ├── trend_scorer.py
│   ├── sentiment_scorer.py
│   ├── repeat_scorer.py
│   ├── brand_scorer.py
│   └── supply_scorer.py
├── rankers/
│   └── product_ranker.py
├── prompts/
│   └── scoring_prompt.txt
└── tests/
    ├── test_calculators.py
    ├── test_scorers.py
    └── test_rankers.py
```

---

## MESSAGE PASSING SYSTEM (Inter-Agent Communication)

### Message Format (JSON)
```json
{
  "message_id": "uuid",
  "from_agent": "research_agent",
  "to_agent": "supplier_agent",
  "timestamp": "2026-08-03T22:30:00Z",
  "type": "task_completion",
  "priority": "high",
  "payload": {
    "products": [...],
    "metadata": {
      "count": 500,
      "sources": ["amazon", "aliexpress"],
      "quality_score": 0.95
    }
  },
  "requires_response": true
}
```

### Message Queue (Redis)
```
Queue: agent_tasks
├── research_agent:output → Supplier Agent reads
├── supplier_agent:output → Validation Agent reads
├── validation_agent:output → Scoring Agent reads
└── scoring_agent:output → Dashboard reads
```

### Communication Patterns

**Sequential Workflow**:
```
Research Agent completes
    ↓ (pushes message to queue)
Supplier Agent reads & processes
    ↓ (pushes message to queue)
Validation Agent reads & processes
    ↓ (pushes message to queue)
Scoring Agent reads & processes
    ↓ (pushes message to queue)
Dashboard updates in real-time
```

**Agent-to-Agent Requests**:
```
Supplier Agent: "Research Agent, need more detail on Product #5"
    ↓
Research Agent: "Fetching more data..."
    ↓
Research Agent: "Here's the detailed data for Product #5"
    ↓
Supplier Agent: "Thanks, continuing analysis"
```

---

## MEMORY SYSTEM (What Agents Know)

### Database Tables
```sql
-- Agent Knowledge Base
CREATE TABLE agent_memories (
    id INT PRIMARY KEY,
    agent_name VARCHAR(100),
    memory_type VARCHAR(50), -- "product", "supplier", "market", "rule"
    key VARCHAR(255),
    value JSONB,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    confidence FLOAT
);

-- Agent Execution Logs
CREATE TABLE agent_executions (
    id INT PRIMARY KEY,
    agent_name VARCHAR(100),
    execution_timestamp TIMESTAMP,
    status VARCHAR(20), -- "running", "completed", "failed"
    input_data JSONB,
    output_data JSONB,
    error_message TEXT,
    duration_seconds INT,
    api_cost FLOAT
);

-- Agent Communication
CREATE TABLE agent_messages (
    id INT PRIMARY KEY,
    from_agent VARCHAR(100),
    to_agent VARCHAR(100),
    message_type VARCHAR(50),
    payload JSONB,
    created_at TIMESTAMP,
    processed_at TIMESTAMP,
    status VARCHAR(20) -- "pending", "processed"
);

-- Products (Results)
CREATE TABLE athena_products (
    id INT PRIMARY KEY,
    amazon_asin VARCHAR(50),
    name VARCHAR(255),
    price FLOAT,
    rating FLOAT,
    reviews INT,
    ... (all product data),
    is_validated BOOLEAN,
    final_score FLOAT,
    recommendation_rank INT,
    created_at TIMESTAMP
);

-- Suppliers (Results)
CREATE TABLE athena_suppliers (
    id INT PRIMARY KEY,
    product_id INT,
    alibaba_id VARCHAR(100),
    company_name VARCHAR(255),
    ... (all supplier data),
    supplier_score FLOAT,
    best_for_product_id INT
);
```

### Redis Cache (Fast Access)
```
Key: "agent:research:last_run_timestamp" → Value: "2026-08-03T22:30:00Z"
Key: "agent:supplier:products_count" → Value: "500"
Key: "agent:validation:risk_flags_found" → Value: "3"
Key: "product:trending:top_20" → Value: JSON array of products
Key: "supplier:best_prices:mascara" → Value: JSON array of suppliers
```

---

## ORCHESTRATION WORKFLOW

### Daily Execution (Automated)

```
TIME: 00:00 UTC (Midnight)
┌─────────────────────────────────────────┐
│ Scheduler (Celery Beat) Triggers         │
└─────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────┐
│ Step 1: Research Agent Starts (00:00)    │
│ - Scrape Amazon (30 min)                │
│ - Scrape AliExpress (15 min)            │
│ - Analyze trends (15 min)               │
│ - Self-validate (5 min)                 │
│ - Push to queue                         │
│ Duration: ~1h 5m                        │
└─────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────┐
│ Step 2: Supplier Agent Starts (01:15)    │
│ - Read Research output                  │
│ - Find 3-5 suppliers per product (45m)  │
│ - Score suppliers (15 min)              │
│ - Self-validate (10 min)                │
│ - Push to queue                         │
│ Duration: ~1h 10m                       │
└─────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────┐
│ Step 3: Validation Agent Starts (02:30)  │
│ - Read Supplier output                  │
│ - Verify Amazon data (20 min)           │
│ - Check supplier ratings (20 min)       │
│ - Cross-validate (15 min)               │
│ - Risk scoring (10 min)                 │
│ - Self-validate (5 min)                 │
│ - Push to queue                         │
│ Duration: ~1h 10m                       │
└─────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────┐
│ Step 4: Scoring Agent Starts (03:50)     │
│ - Read Validation output                │
│ - Calculate profits (20 min)            │
│ - Calculate ROI (10 min)                │
│ - 7-dimension scoring (20 min)          │
│ - Ranking (5 min)                       │
│ - Self-validate (5 min)                 │
│ - Push to Dashboard                     │
│ Duration: ~1h                           │
└─────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────┐
│ DONE at ~05:00 UTC                      │
│ Total time: ~5 hours                    │
│ All results in database & dashboard     │
└─────────────────────────────────────────┘

USER WAKES UP: Dashboard shows "Daily analysis complete"
```

---

## API USAGE OPTIMIZATION

### When to Use Each API

| Task | Primary API | Why | Secondary |
|------|-------------|-----|-----------|
| Web scraping analysis | ChatGPT | Fast, good at parsing | Claude |
| Complex reasoning | Claude | Best reasoning ability | ChatGPT |
| Fact-checking | Gemini | Good at verification | Claude |
| Weighted scoring math | Claude | Complex calculations | ChatGPT |
| Risk analysis | Claude | Nuanced reasoning | Gemini |
| Data validation | Gemini | Fast verification | ChatGPT |
| Content generation | Claude | Best writing | ChatGPT |

### Cost Breakdown (Per Daily Run)
```
Research Agent (ChatGPT):    $0.02 (web analysis)
Supplier Agent (Claude):    $0.05 (complex reasoning)
Validation Agent (Gemini):  $0.01 (fact-checking)
Scoring Agent (Claude):     $0.03 (math + ranking)
─────────────────────────────────────────
TOTAL PER DAY:              $0.11
TOTAL PER MONTH:            $3.30
TOTAL PER YEAR:             $40
```

---

## DASHBOARD (What User Sees)

### Real-Time Status Page
```
http://localhost:3000/athena/dashboard

Shows:
├── Agent Status (✅ Complete / ⏳ Running / ❌ Error)
├── Progress Bars (Research 100%, Supplier 75%, ...)
├── Timeline (started 22:00, est. completion 04:00)
├── TOP 5 RECOMMENDATIONS (live updated)
├── Risk Flags (any issues found)
├── Cost This Run ($0.11)
└── [View Full Report] [Approve Top 5] [Rerun Now]
```

### Report View
```
Each agent generates a detailed report:
├── Research Agent Report
│   ├── Products found: 500
│   ├── Sources used: Amazon, AliExpress
│   ├── Data quality: 95%
│   └── Execution time: 1h 5m
│
├── Supplier Agent Report
│   ├── Suppliers found: 150
│   ├── Suppliers per product: 3-5
│   ├── Quality: 92%
│   └── Execution time: 1h 10m
│
├── Validation Report
│   ├── Products validated: 47/50
│   ├── Risk flags: 3
│   ├── Data quality: 94%
│   └── Execution time: 1h 10m
│
└── Scoring Report
    ├── Products scored: 47
    ├── Top product: #1 (94/100)
    ├── ROI range: 38-58%
    └── Execution time: 1h
```

---

## ERROR HANDLING & SELF-HEALING

### Agent Failure Recovery

**Level 1: Agent self-heals**
```
IF api_call_fails:
    retry_with_backoff(max_retries=3)
    if all_retries_fail:
        use_secondary_api()
    if secondary_api_fails:
        use_fallback_api()
    if all_fail:
        log_error() and continue_with_cached_data()
```

**Level 2: Inter-agent communication fails**
```
IF message_not_delivered:
    retry_message_delivery(max_retries=5)
    if delivery_fails:
        store_in_deadletter_queue()
        alert_human() via email
    else:
        continue
```

**Level 3: Data quality issue**
```
IF validation_fails:
    IF recoverable:
        retry_with_different_approach()
    ELSE:
        flag_as_risky()
        log_red_flag()
        continue_with_caution()
```

---

## DEPLOYMENT & EXECUTION

### Local Development
```bash
# Start all services
docker-compose up

# Run agents locally (one-time)
python -m ai_agents.orchestrator --run-once

# Run agents on schedule (continuous)
celery -A ai_agents.tasks worker --loglevel=info
celery -A ai_agents.tasks beat --loglevel=info

# View dashboard
http://localhost:3000/athena/dashboard
```

### Production (AWS)
```
- Agents run on AWS Lambda (serverless)
- Scheduled via EventBridge (cron trigger)
- PostgreSQL on RDS (managed database)
- Redis on ElastiCache (managed cache)
- Dashboard on Vercel (frontend)
```

---

## TESTING STRATEGY

### Unit Tests (Per Agent)
```python
# test_research_agent.py
def test_research_agent_finds_products():
    agent = ResearchAgent()
    products = agent.execute()
    assert len(products) > 100
    assert all(p.has_required_fields())
    
def test_research_agent_self_validates():
    agent = ResearchAgent()
    invalid_data = generate_invalid_products()
    agent.validate(invalid_data)
    assert agent.validation_failed()

# Similar tests for all other agents
```

### Integration Tests (Agent Communication)
```python
# test_agent_communication.py
def test_research_to_supplier_pipeline():
    research = ResearchAgent()
    supplier = SupplierAgent()
    
    research_output = research.execute()
    supplier_input = research_output
    
    supplier_output = supplier.execute(supplier_input)
    assert supplier_output.has_all_suppliers()

# Test full pipeline
def test_full_athena_pipeline():
    result = run_full_pipeline()
    assert result.has_top_5_recommendations()
    assert result.all_agents_succeeded()
```

### Performance Tests
```python
# test_performance.py
def test_research_agent_performance():
    # Should complete in <1.5 hours
    start = time.time()
    agent.execute()
    duration = time.time() - start
    assert duration < 5400  # 90 minutes

# Test cost efficiency
def test_api_cost_optimization():
    # Total cost per run should be < $0.20
    assert get_total_api_cost() < 0.20
```

---

## MONITORING & OBSERVABILITY

### Metrics to Track
```
Per Agent:
├── Execution time (seconds)
├── API calls made (count)
├── API cost (dollars)
├── Success rate (%)
├── Data quality score (%)
├── Errors encountered (count)
└── Self-healing actions taken (count)

Overall:
├── Total execution time per day
├── Total API cost per day
├── Number of products scored
├── Number of red flags found
└── Dashboard uptime (%)
```

### Logging
```
All logs go to:
├── PostgreSQL (agent_executions table) - permanent record
├── Redis (last 1000 logs) - quick access
├── CloudWatch (AWS) - production logs
└── Local console (development)

Log format:
{
  "timestamp": "2026-08-03T22:30:00Z",
  "agent": "research_agent",
  "level": "INFO",
  "message": "Scraped 500 Amazon products",
  "data": {...}
}
```

---

## FUTURE ENHANCEMENTS (Phase 2+)

1. **Agent Learning**
   - Track which recommendations you approve/reject
   - Agents adjust weights based on feedback

2. **Continuous Monitoring**
   - Instead of daily runs, monitor 24/7
   - Alert when market conditions change

3. **Additional Agents**
   - Content Agent (writes blog posts about selected products)
   - Email Agent (nurtures customers)
   - Branding Agent (suggests packaging/photography)
   - Autopilot Agent (executes decisions automatically)

4. **Multi-Product Support**
   - Run agents on multiple products simultaneously
   - Prioritize best opportunities

5. **Feedback Loop**
   - Users provide feedback via dashboard
   - Agents learn and improve scoring weights

---

## TIMELINE

**Week 1-2**: Infrastructure Setup
- Message queue (Redis)
- Database schema
- Agent framework (CrewAI/AutoGen)

**Week 3-4**: Research Agent
- Web scraping
- Data validation
- Self-testing

**Week 5**: Supplier Agent
- Alibaba integration
- Scoring logic
- Inter-agent communication

**Week 6**: Validation Agent
- Cross-checking logic
- Risk analysis
- Red flag detection

**Week 7**: Scoring Agent
- Complex calculations
- Final ranking
- Report generation

**Week 8**: Dashboard + Testing
- Real-time dashboard
- Full testing
- Production deployment

---

## SUCCESS CRITERIA

✅ All agents run independently without human intervention  
✅ Agents communicate with each other without user involvement  
✅ Self-testing catches 95%+ of errors  
✅ Daily run completes in <6 hours  
✅ API cost per run < $0.15  
✅ Dashboard shows live progress  
✅ Top 5 recommendations are accurate  
✅ Can run 24/7 without intervention

---

**This is Option B: The Full Multi-Agent System.**

Ready to build it.

