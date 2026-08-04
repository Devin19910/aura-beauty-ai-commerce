# Security Documentation

## Overview

Aura Beauty implements enterprise-grade security across all layers: authentication, data protection, infrastructure, and operational security.

## Authentication & Authorization

### Frontend Authentication (Clerk)

**Flow**:
```
1. User clicks "Sign In"
2. Clerk modal opens
3. User enters credentials
4. Clerk validates & creates session
5. JWT token returned to frontend
6. Token stored in secure cookie
7. Token sent with every API request
```

**Token Management**:
- Access token: 30 minutes TTL
- Refresh token: 7 days TTL
- Automatic refresh: Background process
- Logout: Token revocation

**Security**:
- Secure HttpOnly cookies
- SameSite=Strict
- Signed tokens (can't be tampered)

### Backend API Authentication

**JWT Validation**:
```python
# Every endpoint validates JWT
@router.get("/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello {current_user.name}"}
```

**Token Validation**:
1. Check token signature (using SECRET_KEY)
2. Check token expiration
3. Check user status (active/inactive)
4. Load user from database

### Authorization (Role-Based Access Control)

**Roles**:
- `user`: Standard customer (default)
- `admin`: Platform administrator
- `support`: Customer support staff
- `seller`: Vendor (future)
- `agent`: System agents

**Role Enforcement**:
```python
@router.delete("/admin/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user)
):
    # Check authorization
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    
    # Delete user
    ...
```

---

## Data Protection

### Passwords

- **Hash Algorithm**: bcrypt with cost factor 12
- **Never**: Log, display, or store plaintext
- **Reset**: 24-hour token via email (Resend)
- **Validation**: Minimum 8 chars, complexity rules

### API Keys & Secrets

**Storage**:
- Environment variables (Docker secrets in production)
- Never committed to git
- Rotated regularly (quarterly)
- Audit logging of access

**Example**: 
```env
# .env (NEVER commit)
STRIPE_SECRET_KEY=sk_live_...
CLAUDE_API_KEY=sk-...
CLERK_SECRET_KEY=...
```

### Sensitive Data

**PCI Compliance** (Payment Card Industry):
- Credit card numbers: NEVER stored (Stripe tokenization)
- Only store: Stripe Payment Method ID
- Audit logging: All payment transactions
- Encryption: TLS for all card data in transit

**GDPR Compliance**:
- User consent: Tracked for emails/analytics
- Data export: Available via /api/users/me/export
- Data deletion: Delete all user data (GDPR right to be forgotten)
- Privacy policy: Updated and linked

**Personal Data**:
- Encrypted at rest (RDS encryption)
- Encrypted in transit (HTTPS)
- Access logging: Who accessed what when
- Retention: 2-year policy

---

## Infrastructure Security

### Network

**HTTPS Only**:
- Redirect HTTP → HTTPS
- HSTS header (max-age=31536000)
- TLS 1.2+

**CORS**:
```python
# Only allow trusted origins
ALLOWED_ORIGINS = [
    "https://aurabeauty.com",
    "https://www.aurabeauty.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

**Firewall Rules**:
- Vercel: DDoS mitigation + WAF
- AWS: Security groups restricting inbound traffic
- Database: Private VPC, no public internet access

### Database Security

**PostgreSQL**:
- Encryption at rest: AWS RDS encryption
- Encryption in transit: SSL connections
- Access control: IAM database authentication
- Backups: Automated daily, encrypted
- Audit logging: CloudTrail for administrative access

**User Permissions**:
```sql
-- Limited database user (not root)
CREATE USER app_user WITH PASSWORD 'secure_password';
GRANT SELECT, INSERT, UPDATE, DELETE ON all tables IN SCHEMA public TO app_user;
REVOKE ALL ON DATABASE postgres FROM public;
```

### Application Security

**Secret Rotation**:
- Database credentials: Quarterly
- API keys: Quarterly
- JWT secret: On staff departure
- SSL certificates: 90-day auto-renewal

**Dependency Management**:
- Snyk scanning: Weekly vulnerability checks
- Dependabot: Automated dependency updates
- No direct npm publish: All packages from npm registry

---

## API Security

### Rate Limiting

**Implementation**: Redis-backed rate limiter

```python
@router.post("/login")
@rate_limit(requests=5, window=900)  # 5 requests per 15 minutes
async def login(credentials: LoginRequest):
    ...

@router.get("/search")
@rate_limit(requests=100, window=3600)  # 100 per hour
async def search(q: str):
    ...
```

**Endpoints Protected**:
- Login/Signup: 5/15min per IP
- Search: 100/hour per user
- API: 1000/hour per user token

### Input Validation

**Request Validation** (Pydantic):
```python
class ProductCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=200)
    price: float = Field(..., gt=0, le=100000)
    description: str = Field(..., min_length=10)
    
    @validator('price')
    def price_must_be_reasonable(cls, v):
        if v < 0.01:
            raise ValueError('Price too low')
        return v
```

**SQL Injection Prevention**:
- SQLAlchemy ORM (parameterized queries)
- No string concatenation
- Input validation before queries

**XSS Prevention**:
- React auto-escaping
- Content Security Policy headers
- DOMPurify for user-generated content

**CSRF Protection**:
- SameSite cookies (Strict)
- CSRF tokens for state-changing operations (future)
- Verify origin headers

### Error Handling

**Safe Error Messages**:
```python
# ❌ BAD - Exposes database details
@router.get("/users/{user_id}")
async def get_user(user_id: int):
    try:
        return db.query(User).filter(User.id == user_id).first()
    except Exception as e:
        return {"error": str(e)}  # Exposes SQL errors!

# ✓ GOOD - Generic error messages
@router.get("/users/{user_id}")
async def get_user(user_id: int):
    try:
        return db.query(User).filter(User.id == user_id).first()
    except Exception as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
```

---

## Operational Security

### Access Control

**Team Access**:
- GitHub: 2FA required
- AWS: MFA required
- SSH keys: Ed25519, no passwords
- Secrets: HashiCorp Vault (future)

**Least Privilege**:
- Developers: No production database access
- Database admin: Separate account, audit logging
- Credentials: Rotate every 90 days

### Monitoring & Logging

**Audit Logging**:
- All admin actions logged
- Payment transactions logged
- Authentication events logged
- Database modifications logged
- Retention: 2 years (compliance)

**Security Events**:
- Failed login attempts
- Permission denied errors
- Database access from unusual IPs
- Unusual payment patterns
- Large data exports

**Alert Triggers**:
- Suspicious authentication (Sentry)
- Permission denied spike (CloudWatch)
- Data exfiltration pattern (Datadog)
- Database down (PagerDuty)

### Incident Response

**Process**:
1. **Detect**: Monitoring system alerts
2. **Contain**: Isolate affected systems
3. **Investigate**: Review logs, determine scope
4. **Remediate**: Fix vulnerability, patch systems
5. **Recovery**: Restore from backups if needed
6. **Post-Mortem**: Document, improve processes

**Example**: Suspected data breach
1. Isolate database (remove internet access)
2. Pull audit logs (who accessed what)
3. Notify affected users within 24h
4. Issue password reset if credentials compromised
5. Review access controls (what failed?)
6. Update security measures

### Regular Security Activities

**Weekly**:
- Review failed login attempts
- Check Snyk for new vulnerabilities
- Review Cloudtrail logs for unusual activity

**Monthly**:
- Penetration testing checklist
- Dependency update review
- Access control review

**Quarterly**:
- Security audit
- Penetration testing (3rd party)
- Staff security training
- Disaster recovery drill

**Annually**:
- Security assessment
- Compliance audit (PCI-DSS, GDPR)
- Architecture review

---

## Compliance

### PCI-DSS (Payment Card Industry)

**Requirements**:
- [x] Secure network (firewall, no default passwords)
- [x] Protect stored data (encryption, tokenization)
- [x] Maintain vulnerability program (Snyk scanning)
- [x] Implement strong access control
- [x] Maintain audit trail (CloudTrail)
- [x] Regularly test security (penetration testing)

**Stripe Responsibility**:
- PCI-DSS Level 1 compliant
- Handles all card data
- We never store full card numbers

### GDPR (Data Protection)

**Requirements**:
- [x] Privacy policy (published)
- [x] Consent mechanism (email/analytics opt-in)
- [x] Data export functionality (API endpoint)
- [x] Right to deletion (30-day deletion queue)
- [x] Breach notification (24h to notify users)
- [x] Data processing agreement (signed with Stripe, Clerk, etc.)

**User Rights**:
- Access: `/api/users/me/export` (JSON export)
- Rectification: Edit profile
- Erasure: Delete account (permanent)
- Restriction: Pause email marketing
- Portability: Export account data

---

## Security Checklist

### Before Every Release

- [ ] All secrets in environment variables
- [ ] No hardcoded passwords/keys
- [ ] HTTPS enforced everywhere
- [ ] CORS properly configured
- [ ] Rate limiting enabled
- [ ] Input validation on all endpoints
- [ ] Error messages safe (no details exposed)
- [ ] Authentication required on protected endpoints
- [ ] Authorization checks in place
- [ ] Logging configured (no sensitive data)
- [ ] Dependencies updated
- [ ] Security headers set

### Before Production Deployment

- [ ] SSL/TLS certificate valid
- [ ] Database backed up
- [ ] Secrets rotated
- [ ] Firewall rules reviewed
- [ ] IAM roles reviewed
- [ ] Monitoring alerts configured
- [ ] Incident response plan tested
- [ ] Security team approval

---

## Resources

- **OWASP Top 10**: https://owasp.org/Top10/
- **NIST Cybersecurity Framework**: https://www.nist.gov/cyberframework
- **CIS Controls**: https://www.cisecurity.org/controls/
- **PCI-DSS**: https://www.pcisecuritystandards.org/
- **GDPR**: https://gdpr-info.eu/

