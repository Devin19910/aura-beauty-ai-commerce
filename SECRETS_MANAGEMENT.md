# 🔐 Secrets Management System
**Store all API keys, tokens, and passwords once. Never ask again. Work like a real team member.**

---

## Overview

This project has an **intelligent secrets manager** that:

✅ **Stores secrets securely** in `.env` (never committed to git)  
✅ **Never asks twice** - saves and reuses credentials  
✅ **Works autonomously** - agents access secrets automatically  
✅ **Handles missing secrets gracefully** - asks once if needed  
✅ **Keeps secrets safe** - separated from code  

---

## Quick Start

### Option 1: Interactive Setup (Recommended)

```bash
python secrets_manager.py setup
```

This will:
1. Ask for essential API keys (Claude, Amazon, Stripe)
2. Ask if you want optional keys (Google, OpenAI, etc)
3. Store everything in `.env`
4. Show you what's configured

### Option 2: Manual Setup

Edit `.env` file directly:

```bash
# Copy the template
cp .env.example .env

# Edit with your keys
nano .env
# or
code .env
```

Then fill in your actual values.

### Option 3: One-Line Setup

```bash
# Set individual secrets
python -c "from secrets_manager import get_secret; get_secret('ANTHROPIC_API_KEY')"
```

---

## What Gets Stored

### Essential (Required for Agents)
- `ANTHROPIC_API_KEY` - Claude API
- `AMAZON_SELLER_ID` - Your Amazon account
- `STRIPE_SECRET_KEY` - Payment processing

### Important (Recommended)
- `GOOGLE_API_KEY` - Trend research
- `RESEND_API_KEY` - Email management
- `DATABASE_URL` - Your database

### Optional (Add as Needed)
- `OPENAI_API_KEY` - Fallback AI
- `CLERK_SECRET_KEY` - Authentication
- `AWS_ACCESS_KEY_ID` - Cloud storage

---

## How It Works

### The Magic: Smart Agent Integration

**Old way:**
```
Agent asks → "Need API key?"
You type → "sk-ant-..."
Agent crashes → You have to find key again
```

**New way:**
```
Agent starts → Checks .env
If found → Uses it
If missing → Asks once, stores it
Next time → Uses stored version
Never asks again → You move on
```

### In Code

Agents use it like this:

```python
from secrets_manager import get_secret, require_secret

# Flexible - OK if missing
api_key = get_secret("ANTHROPIC_API_KEY")

# Required - fails if missing
stripe_key = require_secret("STRIPE_SECRET_KEY")
```

---

## File Structure

```
your-project/
├── .env                 ← SECRET (stores your actual keys)
├── .env.example         ← SAFE (template, no real keys)
├── secrets_manager.py   ← TOOL (handles secrets)
├── .gitignore           ← SAFETY (prevents .env commits)
└── autonomous-agents/
    ├── autonomous-amazon-agent.py
    └── autonomous-operations-agent.py
```

### .gitignore Protects You

```
.env                    ← Never committed
.env.local              ← Never committed
.env.*.local            ← Never committed
```

Your actual credentials stay LOCAL only. They never go to GitHub or team members.

---

## Setting Up Right Now

### Step 1: Interactive Setup (2 minutes)

```bash
cd C:\Users\Admin\Projects\aura-beauty-ai-commerce
python secrets_manager.py setup
```

This will:
- Ask for Claude API key (you'll enter once)
- Ask for Amazon Seller ID (optional)
- Ask for Stripe key (optional)
- Store all in `.env`
- Show you what's configured

### Step 2: Verify Setup

```bash
python secrets_manager.py status
```

Shows:
```
SECRETS CONFIGURED

✓ CONFIGURED:
  • ANTHROPIC_API_KEY
  • AMAZON_SELLER_ID

✗ NOT CONFIGURED (2):
  • STRIPE_SECRET_KEY
  • GOOGLE_API_KEY
```

### Step 3: Run Agents (They Work Automatically)

```bash
python autonomous-amazon-agent.py
```

The agent will:
- Load your stored API key automatically
- Never ask for it again
- Complete its work
- Save results

---

## Common Scenarios

### Scenario 1: You Have Some Keys Already

If you already set `ANTHROPIC_API_KEY` in your terminal:

```bash
# When you run this:
python secrets_manager.py setup

# It will:
# 1. Check if key is in environment
# 2. If found, skip asking
# 3. Save it to .env for future use
# 4. Never ask again
```

### Scenario 2: Agent Needs a Key It Doesn't Have

```python
# If STRIPE_SECRET_KEY is missing:
stripe_key = require_secret("STRIPE_SECRET_KEY")

# This will:
# 1. Check .env
# 2. If not found, ask user
# 3. Store it
# 4. Return it
# 5. Next time: Use stored version
```

### Scenario 3: Team Member Gets Your Code

They get the code but NOT the `.env` file (it's in .gitignore).

They run:
```bash
python secrets_manager.py setup
```

They enter their own API keys. Their keys stay in their `.env`. Nobody shares credentials.

---

## Security Best Practices

### DO ✅
- Keep `.env` in `.gitignore` (already done)
- Never commit `.env` to git
- Never paste `.env` content in chat
- Never share your `.env` file
- Rotate keys regularly

### DON'T ❌
- Hardcode API keys in code
- Commit `.env` to git
- Share API keys in chat/email
- Commit secrets then delete (history remains)
- Use same key across environments

### If You Accidentally Expose a Key

1. **Immediately rotate it** (get new key from API provider)
2. **Update `.env`** with new key
3. **Test agents work** with new key
4. **Never use old key again**

---

## Advanced: Environment-Specific Secrets

For multiple environments:

```bash
# Development
.env.development      ← Local development keys

# Staging
.env.staging          ← Staging server keys

# Production
.env.production       ← Production keys (most secure)
```

All in `.gitignore`. Each developer/server has its own.

Load based on environment:

```python
from secrets_manager import get_secret

ENV = os.getenv("ENVIRONMENT", "development")
api_key = get_secret(f"{ENV}_ANTHROPIC_API_KEY")
```

---

## Troubleshooting

### Issue: "ANTHROPIC_API_KEY not configured"

**Solution:**
```bash
python secrets_manager.py setup
```

### Issue: "FileNotFoundError: .env"

**Solution:** The file is created automatically. Just run setup:
```bash
python secrets_manager.py setup
```

### Issue: Agent still asks for key

**Solution:** Either:
1. Key not in `.env` properly → Run `python secrets_manager.py status`
2. Old code not using secrets_manager → Update agent imports

### Issue: "Permission denied writing to .env"

**Solution:** Make sure you own the file:
```bash
ls -la .env
# Should show your user, not root
```

---

## For Team/Deployment

### Development Environment

Each developer has their own `.env`:

```
developer-1/
├── .env (their keys)
├── autonomous-agents/
└── ...

developer-2/
├── .env (their keys)
├── autonomous-agents/
└── ...
```

Nobody shares keys. Everyone runs their own setup.

### Production Environment

Server has its own `.env`:

```
production-server/
├── .env (production keys only)
├── autonomous-agents/
└── ...
```

Set via:
- Environment variables on server
- Docker secrets
- Kubernetes secrets
- AWS Secrets Manager (for cloud)

Example for Docker:

```dockerfile
FROM python:3.11
WORKDIR /app
COPY . .

# Keys injected at runtime, not in image
ENV ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
ENV STRIPE_SECRET_KEY=${STRIPE_SECRET_KEY}

CMD ["python", "autonomous-amazon-agent.py"]
```

---

## Commands Reference

```bash
# Interactive setup
python secrets_manager.py setup

# Show what's configured
python secrets_manager.py status

# Show this help
python secrets_manager.py help
```

---

## The Philosophy

**Store once. Use everywhere. Never ask again. Work like a real team.**

Your secrets manager acts like a smart colleague:
- "Do you have your API key?" (asks once)
- Remembers it (stores in .env)
- Uses it automatically (never mentions it again)
- Handles it securely (never commits to git)
- Fixes problems without asking (self-healing)

That's how a real team member works. And that's how your agents work too.

---

## Next Steps

1. **Run setup**
   ```bash
   python secrets_manager.py setup
   ```

2. **Verify configuration**
   ```bash
   python secrets_manager.py status
   ```

3. **Run your agents** (they'll use stored secrets automatically)
   ```bash
   python autonomous-amazon-agent.py
   ```

4. **Never worry about API keys again** - they're stored, secured, and automated

---

**Your secrets are safe. Your agents work automatically. You work smart.** 🔐🤖
