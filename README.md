# Knowledge Subscription

**AI Architecture Weekly** — Production-grade AI engineering decisions, delivered weekly.

## Project Overview

This repository contains the content, code, and infrastructure for a premium English-language newsletter focused on AI architecture and production engineering decisions.

## Repository Structure

```
knowledge-subscription/
├── docs/                    # Strategy and planning documents
│   ├── strategy.md          # Business strategy and positioning
│   └── mvp_spec.md          # MVP specification
├── content/                 # Newsletter issues
│   └── pilot-issue-01-long-context-vs-rag.md
├── diagrams/                # Architecture diagrams (SVG)
│   └── long-context-decision-tree.svg
├── code-examples/           # Runnable code samples
│   └── long_context_client.py
├── reports/                 # Analytics and deployment reports
└── README.md               # This file
```

## Quick Start

### Reading the Content

1. **Pilot Issue #1**: [Long Context vs RAG](./content/pilot-issue-01-long-context-vs-rag.md)
   - Complete architecture decision record format
   - Trade-off analysis, code examples, failure modes

### Running the Code

```bash
# Install dependencies
pip install anthropic tiktoken python-dotenv

# Set your API key
export ANTHROPIC_API_KEY="your-key-here"

# Run the example
cd code-examples
python long_context_client.py
```

## Content Format

Each newsletter issue follows the **Architecture Decision Record (ADR)** format:

1. **Thesis**: Clear, actionable insight
2. **Architecture Diagram**: Visual mental model
3. **Trade-off Analysis**: When to use vs. when to avoid
4. **Implementation Notes**: Production-ready code
5. **Failure Modes**: Real-world pitfalls
6. **Sources**: Primary research and evidence

## Current Status

- [x] Strategy document
- [x] MVP specification
- [x] Pilot issue #1 (Long Context vs RAG)
- [x] Architecture diagram
- [x] Code examples
- [ ] Substack account setup
- [ ] Landing page
- [ ] Issues #2-4 (buffer building)

## Market Research

**Verdict**: GO (79/100)

This project has passed the market research gate:
- Total Score: 79/100 (≥ 70 required)
- Paid Willingness: 19/25 (≥ 15 required)
- Risk Controllability: 11/15 (≥ 8 required)

See: `/ai-opportunity-radar/market-research/knowledge-subscription/verdict.md`

## Revenue Model

| Tier | Price | Features |
|------|-------|----------|
| Free | $0 | 1 issue/month, delayed access |
| Pro | $15/mo | Weekly issues, immediate access, code repos |
| Team | $499/yr | Everything + sharing license + quarterly reviews |

**Year 1 Target**: $36K ARR (200 paid subscribers)

## Contributing

This is a Dev Team project. See team charter for contribution guidelines.

## License

Content © 2026 AI Architecture Weekly. Code examples under MIT License.

---

*Built by the Dev Team • Making money with AI, one architecture decision at a time*