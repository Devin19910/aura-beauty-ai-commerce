# Security Tasks - Project Athena

## 🔐 TASK 1: API Key Rotation (URGENT - August 17, 2026)

**Status**: ⏳ Pending  
**Priority**: HIGH  
**Due Date**: August 17, 2026 (2 weeks from today)  
**Owner**: You (Manual action required)

### Why
API keys were shared in conversation. While safe to use now, they should be rotated for best practices.

### What to Do
1. **OpenAI (ChatGPT)**
   - Go to: https://platform.openai.com/account/api-keys
   - Delete old key (sk-proj-4_UOnnLyG...)
   - Create NEW key
   - Update `.env.local` with new key
   - Verify old key is gone from account

2. **Google Gemini**
   - Go to: https://ai.google.dev/
   - Delete old key (AIzaSyA0jpdaQug3E2Il...)
   - Create NEW key
   - Update `.env.local` with new key
   - Verify old key is gone from account

3. **Anthropic (Claude)**
   - Go to: https://console.anthropic.com/
   - Delete old key (sk-ant-api03-JRZvXNmjahBi...)
   - Create NEW key
   - Update `.env.local` with new key
   - Verify old key is gone from account

### Verification
- [ ] All 3 old keys deleted from provider accounts
- [ ] All 3 new keys in `.env.local`
- [ ] Agents still work with new keys (run test)
- [ ] No commits contain old keys (check git history)

### How to Run Test
```bash
cd /path/to/project
python -m ai_agents.test_api_keys
# Should output: ✅ All APIs working with new keys
```

---

## 🔐 TASK 2: .env Security Audit (After Deployment)

**Status**: ⏳ Pending  
**Priority**: MEDIUM  
**Due Date**: End of Week 8 (before production)

### What to Check
- [ ] `.env.local` in `.gitignore` ✅
- [ ] No API keys in code (grep check)
- [ ] No secrets in logs
- [ ] Environment variables validated on startup
- [ ] Error messages don't expose keys
- [ ] Production uses different secrets (AWS Secrets Manager)

---

## 🔐 TASK 3: Production Secrets Setup (Week 8)

**Status**: ⏳ Pending  
**Priority**: CRITICAL  
**Due Date**: Week 8 (before deploying to AWS)

### Setup AWS Secrets Manager
Instead of `.env.local`, production will use AWS Secrets Manager:

```python
# In production
import boto3

def get_api_keys():
    client = boto3.client('secretsmanager')
    secret = client.get_secret_value(SecretId='athena-api-keys')
    return json.loads(secret['SecretString'])
```

### Action Items
- [ ] Create AWS Secrets Manager secret
- [ ] Store API keys there (not in code)
- [ ] Update production code to read from Secrets Manager
- [ ] Test in staging environment
- [ ] Document secret rotation procedure

---

## Summary

| Task | Priority | Due | Owner |
|------|----------|-----|-------|
| Rotate API keys | HIGH | Aug 17 | You |
| Security audit | MEDIUM | Week 8 | Claude |
| Production secrets | CRITICAL | Week 8 | Claude |

**Next Action**: Add Aug 17 to your calendar. That's when you rotate the keys.

