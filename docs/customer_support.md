# Customer Support Guide: AI Architecture Weekly

**Project ID**: knowledge-subscription  
**Task ID**: ab047a39  
**Type**: monitoring (ops-support)  
**Last Updated**: 2026-05-24  
**Owner**: dev-optimizer (profitability-analyst)

---

## 1. Support Philosophy

> **"Every support interaction is a retention and referral opportunity."**

We are a tiny team. We cannot offer 24/7 live chat. But we can be fast, personal, and genuinely helpful. Founder voice in all replies. No templates unless absolutely necessary.

---

## 2. Support Entry Points

### Public Channels (monitored daily)
| Entry Point | URL / Location | Typical Request Type | Response SLA |
|-------------|---------------|----------------------|--------------|
| Substack comments | On each post | Content questions, corrections, debate | 24 hrs |
| Substack email replies | Replies to newsletter | Private feedback, unsubscribe, upgrade | 24 hrs |
| Twitter/X replies & DMs | @ handle | Quick questions, sharing, bug reports | 48 hrs |
| LinkedIn comments & messages | Personal / page | B2B inquiries, Team tier interest | 48 hrs |
| Hacker News replies | On posted stories | Technical deep-dives, corrections | 24 hrs (if top-level) |
| GitHub Issues | Code example repo | Code bugs, setup help, feature requests | 72 hrs |

### Private / Internal Channels
| Entry Point | Access | Typical Request | SLA |
|-------------|--------|---------------|-----|
| Stripe customer portal | dashboard.stripe.com | Billing, refund, invoice, payment failure | 24 hrs |
| Direct email (team alias) | team@ domain | Sensitive issues, legal, partnership | 24 hrs |
| Discord (future) | Private server | Paid member Q&A, community, code help | 4 hrs |

---

## 3. FAQ — Pre-Written Answers (Use as Starting Point, Personalize)

### Q1: "How do I upgrade from free to paid?"
**Answer**: Thanks for considering it! You can upgrade directly on our Substack page — hit the "Subscribe" button and choose Pro ($15/mo) or Founding Member ($99/yr, limited to first 100). If you don't see the option, reply here and I'll send you a direct link.

### Q2: "I paid but I don't see the paid content / template."
**Answer**: Sorry for the confusion! Sometimes Substack takes a few minutes to sync with Stripe. Can you try refreshing the page? If still missing, tell me which issue you're looking for and I'll send it directly.

### Q3: "Can I get a refund?"
**Answer**: Yes — if you're not getting value, I don't want your money. Reply with the email you used to subscribe and I'll process a full refund within 48 hours. No questions asked (though I'd love to know what would have made it worth it).

### Q4: "Do you offer student / non-profit discounts?"
**Answer**: Yes! Email me from your .edu or org address and I'll send you a 50% off code for the annual plan.

### Q5: "Can I share this with my team?"
**Answer**: Free issues — absolutely, share widely. Paid issues and templates are for individual subscribers. If you need a team license, check out the Team tier ($499/yr per seat, includes sharing license). Or just forward me your team size and I'll quote custom.

### Q6: "The code example didn't work for me."
**Answer**: Sorry about that. A few quick things to check: (1) Are you on Python 3.10+? (2) Did you install the pinned versions in requirements.txt? (3) What's the exact error message? Paste it here and I'll debug with you.

### Q7: "I want to unsubscribe."
**Answer**: No problem — you can unsubscribe at the bottom of any email. If you're leaving because something wasn't working, I'd genuinely appreciate a one-line reply telling me why. It helps make the newsletter better.

### Q8: "Do you consult / can you advise on our architecture?"
**Answer**: Sometimes! I take on a very limited number of advisory engagements. If you're on the Team tier or above, you get a quarterly review call included. For deeper engagements, email me with your scope and timeline and I'll send availability and rates.

### Q9: "Can I republish / translate your content?"
**Answer**: Free issues: yes with attribution and a link back. Paid issues: no, that's how we fund the work. For syndication or translation deals, email me directly.

### Q10: "How do I access the Discord community?"
**Answer**: It's not live yet — we're launching it once we hit 50 paid subscribers. You'll get an invite automatically when we cross that threshold. Want in early? Reply and I'll add you to the pre-launch list.

### Q11: "Your website / sales page is not loading. Is this a scam?"
**Answer**: Thanks for flagging this! We're currently migrating our landing page to a new host and it may be briefly offline. If you're seeing a 404 or timeout, it should be resolved within a few hours. In the meantime, you can browse our content directly on Substack (link) or add me on WeChat for direct access. Apologies for the friction — here's a 20% off code for the inconvenience: `COMEBACK20`.

> **Internal note**: If sales page is offline due to deployment blocker, do NOT offer discounts until the page is live. Reply with expected fix time and direct user to Substack or WeChat as fallback.

### Q12: "我怎么付款？安全吗？"
**Answer**: 你直接微信/支付宝转我就行，¥29，确认后我秒发资料。不放心的话，我先发你一半试读，看完觉得值再付。

### Q13: "付了款没收到怎么办？"
**Answer**: 抱歉！有时候消息多会漏掉。你把付款截图发我，我立刻补发，再送你一份额外的模板作为补偿。

### Q14: "能不能便宜点？"
**Answer**: 这次早鸟价¥29已经是底价了，后面会涨到¥99。如果你觉得不值，我可以先发你一份免费资料，看完再决定。

### Q15: "我可以转发给朋友吗？"
**Answer**: 免费的内容随便转。付费资料仅限你自己用，朋友想要可以推我微信，我给他们同样的早鸟价。

---

## 4. Human Escalation Paths

### When to escalate immediately (don't try to handle alone)
| Scenario | Escalate To | Why |
|----------|-------------|-----|
| User threatens legal action | dev-security | Legal liability |
| User reports data breach / unauthorized charge | dev-security + dev-deploy | Security + payment integrity |
| User is a journalist / media inquiry | dev-architect | Brand/messaging control |
| User offers acquisition / partnership / investment | dev-architect | Strategic opportunity |
| User is clearly in distress / mental health crisis | dev-architect | Duty of care; no business response |
| User engages in harassment / abuse | dev-security | Safety and platform policy |

### Escalation process
1. Screenshot the full context
2. Do NOT reply further until escalation resolved
3. Forward to escalate-to with subject `[ESCALATION] <brief description>`
4. Document in `metrics/experiment_tracker.csv` notes (anonymized)

---

## 5. Tone & Voice Guidelines

### Do
- Use first person ("I", "me", "my") — this is a founder-led product
- Be specific: cite issue numbers, link directly to resources
- Admit mistakes openly: "You're right, that benchmark was outdated. Here's the corrected number."
- Over-deliver: if someone asks for one thing, give them the next related thing too
- Sign with your name / handle

### Don't
- Use corporate speak ("We value your feedback and will escalate to the relevant team")
- Copy-paste without reading the actual question
- Argue with subscribers in public threads — take debates to DMs/email
- Promise timelines you can't keep
- Ignore negative feedback — it's often the most valuable

---

## 6. Support Volume Targets & Capacity Planning

| Volume Level | Tickets/Day | Handling Time | Action |
|--------------|-------------|---------------|--------|
| < 5 | Normal ops | ~30 min/day | dev-optimizer handles directly |
| 5-15 | Growth phase | ~1.5 hrs/day | dev-optimizer + async dev-architect backup |
| 15-30 | Scaling threshold | ~3 hrs/day | Hire part-time community manager OR automate FAQ bot |
| > 30 | Full business | ~6 hrs/day | Dedicated support hire; document hiring SOP |

**Current capacity**: ~5 tickets/day before impacting content production time.

---

## 7. Feedback Loop to Product

Every support interaction feeds back into the product:

| Support Signal | Product Action | Owner |
|----------------|---------------|-------|
| 3+ people ask same question | Add to FAQ; consider self-service page | dev-optimizer |
| Code example broken | Fix in repo; add regression test | dev-coder |
| "Too expensive" > 20% of churn | A/B test pricing; consider new tier | dev-architect |
| "Not technical enough" | Adjust content difficulty upward | dev-architect |
| "Too dense / hard to read" | Add summary section; simplify diagrams | dev-optimizer |
| Feature request repeated 5+ times | Add to backlog; size for next sprint | dev-architect |
| Competitor mentioned favorably | Competitive research task | dev-optimizer |

---

**Next Review**: 2026-06-21  
**Version**: 1.0  
**Owner**: dev-optimizer  
**Measured by**: Support response time in `docs/kpi_dashboard.md`, subscriber NPS (future)
