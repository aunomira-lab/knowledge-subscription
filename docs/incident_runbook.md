# Incident Runbook: AI Architecture Weekly

**Project ID**: knowledge-subscription  
**Task ID**: 96cae9d2  
**Type**: monitoring (ops-support)  
**Last Updated**: 2026-05-21  
**Owner**: dev-optimizer (profitability-analyst)  
**Severity Levels**: P0 (Critical) / P1 (High) / P2 (Medium) / P3 (Low)

---

## 1. Incident Classification

### P0 — Critical (All Hands, < 1 hr response)
- Stripe checkout broken (zero revenue capture)
- Substack account suspended or banned
- Landing page hijacked / defaced
- Mass subscriber data breach
- Legal cease-and-desist received
- Founder / brand impersonation attack

### P1 — High (< 4 hr response)
- MRR drops > 20% week-over-week with no known cause
- Stripe payout frozen or KYC blocked
- Substack publish failure on scheduled day
- Hacker News front-page traffic spike (opportunity but needs capture)
- Major content error published (factual inaccuracy, broken code)
- Churn spike > 12% in a single week

### P2 — Medium (< 24 hr response)
- Email open rate < 30% for 2 consecutive sends
- Unsubscribe spike > 5% on single issue
- Support ticket > 24 hrs unanswered
- Code example repo issue reported
- Social media negative review / thread
- Minor pricing mismatch between Stripe and Substack

### P3 — Low (< 72 hr response)
- Typos in published issue
- Dead external link
- Minor CSS/layout issue on landing page
- Non-urgent feature request from subscriber

---

## 2. Runbook: P0 Incidents

### 2.1 Stripe Checkout Broken
**Symptoms**: Users report "payment failed", Stripe dashboard shows 0 successful charges, test card fails
1. **00:00-00:05** — Verify Stripe status at status.stripe.com
2. **00:05-00:15** — Run test payment via Stripe test mode
3. **00:15-00:30** — If Stripe is up but our integration broken:
   - Check Substack paid tier settings (pricing, currency, description)
   - Check if Stripe webhook endpoint is returning 200
   - Check Stripe dashboard for account holds / verification requests
4. **00:30-00:45** — If cannot fix: enable "pay what you want" fallback via Ko-fi or Buy Me a Coffee; tweet update
5. **00:45-01:00** — Notify dev-deploy and dev-architect; open `reports/incident_YYYY-MM-DD_stripe.md`
6. **Post-fix** — Send apology + discount code to affected users; log in tracker

### 2.2 Substack Account Suspended
**Symptoms**: Cannot log in, subscribers see "publication unavailable", email from Substack
1. **00:00-00:15** — Read Substack email carefully; screenshot everything
2. **00:15-00:30** — Export subscriber list CSV immediately (if still accessible)
3. **00:30-00:45** — Draft appeal email to Substack support; cc dev-security
4. **00:45-01:00** — Activate backup: create Beehiiv account, import CSV, tweet new URL
5. **01:00-02:00** — Update landing page with new subscription URL
6. **Post-recovery** — If restored, maintain dual-platform for 30 days; if not, full migrate to Beehiiv + self-hosted email

### 2.3 Landing Page Hijacked / Defaced
**Symptoms**: Visitors see unexpected content, SSL error, domain DNS mismatch
1. **00:00-00:10** — Check Vercel/Cloudflare dashboard for unauthorized deployments
2. **00:10-00:20** — Check DNS records for unauthorized changes
3. **00:20-00:30** — Roll back to last known good deployment via dashboard
4. **00:30-00:45** — Rotate API keys / tokens; check GitHub for unauthorized commits
5. **00:45-01:00** — Notify dev-security; run `docs/anti_ai_slop_checklist.md` equivalent for security

### 2.4 Mass Data Breach
**Symptoms**: Subscriber emails leaked, phishing emails sent to list, security notice received
1. **00:00-00:15** — Immediately change all platform passwords (Substack, Stripe, Twitter, GitHub)
2. **00:15-00:30** — Enable 2FA on all accounts where not already enabled
3. **00:30-01:00** — Draft breach notification to subscribers (transparent, factual)
4. **01:00-02:00** — Notify dev-security; investigate source (phishing, API key leak, platform breach)
5. **Post-incident** — Audit all integrations; remove unused API keys; document in `reports/security_incident_YYYY-MM-DD.md`

---

## 3. Runbook: P1 Incidents

### 3.1 MRR Drop > 20% WoW
1. Pull Stripe churn report: how many cancelled? Any bulk cancellations?
2. Check Substack: any email deliverability issues? Bounce spike?
3. Check last 2 published issues: any controversial content? Negative replies?
4. If churn concentrated on one day: investigate if related to specific email or publish
5. Response: Send targeted win-back email with discount; publish high-value free issue
6. Escalate to dev-architect if trend continues for 2nd week

### 3.2 Substack Publish Failure
1. Check Substack status page
2. Retry publish manually
3. If still failing: draft issue as Substack note / Twitter thread as temporary distribution
4. Email free list directly via CSV + SendGrid/Resend as emergency backup
5. Log in `metrics/experiment_tracker.csv`; update `docs/kpi_dashboard.md`

### 3.3 Hacker News Front-Page Spike
**This is a P1 opportunity, not a failure**
1. Monitor traffic in real time (Substack referrer analytics)
2. Pin tweet with subscription CTA
3. Update landing page hero to match HN post topic
4. Enable email capture popup if not already active
5. Prepare short follow-up comment on HN with subscription link
6. After spike: analyze conversion rate from HN → free sub → paid; document for repeatability

### 3.4 Sales Page Offline / Deployment Blocked (P1)
**Symptoms**: `curl` to landing page returns non-200, `wrangler whoami` shows "not authenticated", `CLOUDFLARE_API_TOKEN` not set, user reports "site down"
1. **00:00-00:05** — Verify: `curl -s -o /dev/null -w "%{http_code}" https://ai-opportunity-radar.pages.dev` (or configured domain)
2. **00:05-00:10** — Check `reports/deployment_verification.md` for current blocker status
3. **00:10-00:20** — Check `docs/deployment_blockers.md` for which user auth steps are incomplete
4. **00:20-00:30** — If user auth missing: STOP all content spend and paid ads immediately; do not burn CAC on a broken funnel
5. **00:30-01:00** — Generate updated `reports/deployment_verification.md` with exact unblock steps for user
6. **01:00-04:00** — If user provides auth (API Token / wrangler login success): run `./deploy/deploy.sh production`
7. **Post-deploy** — Verify HTTP 200, check payment links are not placeholders, update `metrics/experiment_tracker.csv` with "unblocked" note
8. **If unresolved > 48 hrs**: escalate to dev-architect with pivot recommendation (小报童-first or WeChat收款码 MVP)

---

## 4. Runbook: P2 Incidents

### 4.1 Email Open Rate < 30% (2x consecutive)
1. Check Substack spam score / deliverability dashboard
2. Review subject lines: are they generic? Too long? No clear value?
3. A/B test next 2 subject lines:
   - Variant A: Specific number + outcome ("3 mistakes that cost $10K in inference")
   - Variant B: Curiosity gap ("The long-context myth most teams believe")
4. Segment inactive subscribers (no open in 30 days) for re-engagement campaign
5. If no improvement after 2 A/B tests, escalate to dev-architect for content strategy review

### 4.2 Unsubscribe Spike > 5%
1. Identify which issue caused the spike (Substack shows unsubscribes per post)
2. Read all replies and comments on that issue
3. Common causes: too promotional, off-topic, controversial opinion, technical error
4. Response: Acknowledge in next issue's intro; adjust content calendar
5. If cause = technical error, publish correction note immediately

---

## 5. Recovery & Post-Incident Process

### Immediate (during incident)
- Create `reports/incident_YYYY-MM-DD_<short-name>.md`
- Log start time, symptoms, actions taken, timestamps
- Communicate in team channel every 30 min for P0, every 2 hr for P1

### Short-term (within 24 hrs of resolution)
- Update incident report with root cause
- Send subscriber communication if user-facing (transparent, not defensive)
- Update `docs/kpi_dashboard.md` with impact quantification (subs lost, revenue lost)

### Medium-term (within 1 week)
- Post-mortem meeting with dev-architect, dev-deploy, dev-security
- Update this runbook if new failure mode discovered
- Implement preventive measures (checklist updates, monitoring alerts, backup automation)

### Long-term (within 1 month)
- Review if incident type recurs; if yes, structural fix required
- Update `docs/support_sop.md` if procedures changed
- Train all team members on new runbook sections

---

## 6. Contact Escalation Tree

```
P0/P1 Detected
    |
    v
dev-optimizer (profitability-analyst) — first responder
    |
    +---> dev-deploy (infra/payment/platform) — P0 tech incidents
    |
    +---> dev-architect (strategy/content) — P1 business incidents
    |
    +---> dev-security (legal/compliance/breach) — P0 security incidents
    |
    +---> dev-tester (QA/code validation) — P2 content/code issues
```

**Emergency Contact Method**: Email team alias with subject `[P0] <incident type>` for critical issues.

---

**Next Drill**: 2026-06-21 (simulate Substack publish failure)  
**Owner**: dev-optimizer  
**Version**: 1.0
