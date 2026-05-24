# Substack 选题方向复核：英文 AI 产品架构 / 前沿研究深度教学

Updated: 2026-05-20 UTC

## Decision

**Pivot / Conditional Go**

这个方向比“普通中文 AI 教学”更符合 Substack 的高价值付费用户画像，但必须定位为专业英文内容，面向 AI builders，而不是泛 AI 爱好者。

推荐公开定位：

> Deep technical analysis of how frontier AI products are built — for engineers, founders, and technical PMs.

更精准版本：

> Architecture, evals, and strategy for teams shipping production AI products.

内部定位：

> ByteByteGo for AI-native products + research-to-production translation.

## Why it fits Substack paid users

Substack 付费用户愿意为以下东西付费：

- 专业判断，而不是新闻；
- 节省研究时间；
- 可用于工作/创业/投资决策的框架；
- 作者/团队的持续筛选能力；
- 能转发给团队的高质量材料；
- 可复用资产：架构图、checklist、templates、benchmarks、playbooks。

英文 AI 产品架构 / 前沿研究深度教学能服务以下高价值人群：

- AI application engineers；
- senior backend / infra engineers transitioning to AI；
- AI startup founders / CTOs；
- technical PMs；
- devtools / infra / MLOps builders；
- technical investors / analysts；
- engineering managers building internal AI systems。

这些人群比普通 AI 工具用户更可能在 Substack 付费，因为内容能影响他们的工程决策、产品方向、职业竞争力或投资判断。

## Comparable publications

### The Pragmatic Engineer

URL: https://newsletter.pragmaticengineer.com/

证明工程师愿意为高质量工程行业分析、职业判断和系统性拆解付费。可借鉴其案例密度、结构化分析和专业可信度。

### Latent Space

URL: https://www.latent.space/

证明 “AI Engineer” 是真实受众类别。差异空间：Latent Space 偏社区、访谈和趋势；Aunomira 可更偏架构图、系统设计、eval、production trade-offs。

### Interconnects

URL: https://www.interconnects.ai/

证明 frontier AI research interpretation 有受众和付费空间。差异空间：从 research interpretation 进一步转成 product architecture / implementation decision。

### Ahead of AI

URL: https://magazine.sebastianraschka.com/

证明高质量 AI/ML 教学、图解和代码化解释有持续受众。差异空间：不做模型算法课程，而做 LLM product architecture。

### ByteByteGo

URL: https://blog.bytebytego.com/

证明系统设计图解和工程教育需求强。差异空间：AI-native product systems design。

### Chip Huyen

URL: https://huyenchip.com/blog/

证明 ML systems / AI engineering 的高质量免费内容能形成强专业品牌和商业机会。差异空间：连续化、付费化、产品架构垂直化。

### Eugene Yan

URL: https://eugeneyan.com/writing/

证明 applied ML/system design writing 可被工程团队内部转发。差异空间：更聚焦 LLM apps、agents、RAG、eval-driven development。

### Hamel Husain

URL: https://hamel.dev/

证明 LLM evals、failure analysis、production debugging 是强痛点。差异空间：做成体系化架构包和可复用模板。

### SemiAnalysis

URL: https://semianalysis.com/

证明专业读者会为决策级 AI infra 分析付高价。差异空间：SemiAnalysis 偏硬件/infra/capital allocation；Aunomira 可做 application architecture 层。

### Lenny’s Newsletter

URL: https://www.lennysnewsletter.com/

证明 PM/founder 愿意为可执行框架和产品判断付费。差异空间：连接 AI product strategy 与 technical architecture。

## Market gaps

### Gap 1: News is abundant; architecture is scarce

市场上很多 AI news roundup、model release summary、tool list，但很少系统回答：

- 这个 AI 产品的架构可能是什么？
- RAG、memory、tools、evals、guardrails 如何组合？
- latency / cost / quality trade-off 是什么？
- 哪些组件该自建，哪些该购买？

### Gap 2: Research explanation is abundant; research-to-product translation is scarce

很多文章解释论文，但少有文章回答：

- 这篇 frontier research 能变成什么产品能力？
- 需要什么 production architecture？
- 什么场景能用，什么场景只是 hype？
- 产品化瓶颈是什么？

### Gap 3: Beginner tutorials are oversupplied; senior implementation content is undersupplied

过剩内容：

- “Build a RAG app in 10 minutes”；
- “LangChain basics”；
- “Top 10 AI tools”；
- “Prompt engineering tips”。

稀缺内容：

- eval-driven development；
- production RAG debugging；
- agent failure modes；
- inference cost modeling；
- context engineering；
- LLM observability；
- human-in-the-loop product design；
- multi-tenant AI SaaS architecture。

### Gap 4: Product teardowns are often business-focused, not technical

对 Cursor、Perplexity、Claude、NotebookLM、Devin、Glean 等产品，很多分析偏商业模式、融资、市场定位。技术读者更想知道：

- likely architecture；
- data flow；
- retrieval/indexing strategy；
- eval loop；
- latency/cost strategy；
- UX moat vs model moat；
- failure modes。

## Recommended content pillars

### 1. AI Product Architecture Teardown

Examples:

- How Cursor Probably Works: Codebase Indexing, Context Retrieval, and Agentic Editing
- Perplexity’s Product Architecture: Search, Retrieval, Citation, and Answer Generation
- NotebookLM Teardown: Source-Grounded Generation as a Product Primitive
- Devin vs Cursor vs Replit Agent: Architecture and UX Trade-offs

### 2. Frontier Research to Product

Examples:

- What Test-Time Compute Means for AI Products
- Why Long Context Does Not Kill RAG — It Changes the Architecture
- Reasoning Models: Product Moat or API Commodity?
- Multimodal Models and New Product Surfaces

### 3. Production AI Engineering

Examples:

- How to Design Evals for LLM Products
- RAG Failure Modes in Production
- The Real Cost Model of LLM Apps
- Agent Architecture: Planner, Executor, Memory, Tools, Evals

### 4. AI Product Strategy for Technical Builders

Examples:

- When Model Quality Is Not Your Moat
- Build vs Buy in AI Infra
- Workflow Integration Beats Chatbot Wrappers
- Pricing AI Features When Inference Cost Is Variable

## Paid product design

Do not sell articles only. Sell professional assets.

Free tier:

- 1 concise weekly issue;
- public architecture insight;
- one diagram or framework;
- strong CTA to subscribe.

Paid tier:

- full architecture diagrams;
- implementation checklist;
- eval plan;
- cost model;
- failure modes;
- vendor/build-vs-buy notes;
- companion code/templates when relevant;
- monthly architecture teardown database update.

Possible paid assets:

- AI product architecture map;
- RAG design review rubric;
- agent failure mode database;
- eval checklist library;
- model/vendor selection matrix;
- LLM cost calculator;
- teardown archive;
- monthly office hour after traction.

## Pricing hypothesis

Initial:

- $12/month;
- $120/year;
- first 100 founding members: $80–99/year;
- founding member: $200–300/year only if including office hour / private Q&A.

Reasoning:

Professional builders are not price-sensitive if content saves hours or improves decisions. Too-low pricing may weaken perceived expertise.

## Promotion channels

Primary:

- X/Twitter: architecture diagrams, high-density threads;
- LinkedIn: AI product/PM/founder framing;
- Hacker News: only for genuinely technical teardowns;
- Reddit: r/MachineLearning, r/LocalLLaMA, r/ExperiencedDevs, r/ProductManagement;
- GitHub: companion repo, templates, eval harness, diagrams;
- Substack Notes: cross-discovery.

Secondary:

- guest posts with AI engineering newsletters;
- podcast appearances;
- AI Engineer / MLOps communities;
- conference notes from NeurIPS/ICML/ICLR/AI Engineer Summit;
- collaborations with open-source AI tools.

## Validation plan

### Phase 1: 4-week free audience validation

Publish 4 high-signal articles:

1. Product teardown;
2. Research-to-product translation;
3. Production AI engineering tutorial;
4. Build-vs-buy / product strategy framework.

Each article must include:

- one clear thesis;
- architecture diagram;
- technical trade-offs;
- implementation notes;
- failure modes;
- no filler paragraphs.

Pass criteria:

- 500–1,000 email subscribers;
- open rate >= 45%;
- click rate >= 8%;
- at least one external distribution spike;
- 20–30 high-quality replies/comments/DMs from target readers.

### Phase 2: 2–4 week paid validation

Launch paid founding member.

Pass criteria:

- 50+ paid subscribers; or
- 3–5% free-to-paid conversion; or
- $5k–10k annualized run-rate;
- 5+ readers say they used content for work decisions;
- 2+ team/company subscription or advisory inquiries.

No-Go signals:

- audience mostly generic AI hobbyists;
- open rate < 35%;
- free-to-paid < 1%;
- comments are generic praise, not technical discussion;
- each article takes >20 hours with no reusable template/process;
- unable to produce original diagrams and sharp judgments.

## Editorial standard: no fluff

Every issue must pass this checklist:

- Does it answer a concrete professional question?
- Can a builder use it to make an architecture/product decision?
- Does it include diagram / decision table / checklist / cost model / eval plan?
- Does it distinguish confirmed facts from inferred architecture?
- Does it cite sources where possible?
- Does it state trade-offs instead of generic best practices?
- Does it avoid news summary, hype, and generic tutorials?
- Would a senior engineer/PM feel it saved time?

## Key risk controls

### Accuracy risk

Product teardowns often infer private architecture. Use labels:

- confirmed from public sources;
- inferred from product behavior/public docs;
- speculative hypothesis.

### Production cost risk

Deep issues can be expensive to produce. Use repeatable templates:

1. user workflow;
2. likely architecture;
3. data/model flow;
4. trade-offs;
5. failure modes;
6. eval strategy;
7. build-vs-buy notes;
8. product moat.

### Competition risk

Do not compete as another AI news/research newsletter. Own this narrower category:

> AI product architecture teardown + research-to-production translation.

## Next Dev Team actions

1. Create 4 pilot article briefs.
2. Create editorial template and no-fluff checklist.
3. Draft first issue in professional English.
4. Build one GitHub companion repo with diagrams/templates.
5. Launch free validation before paid wall.
6. Track subscriber source by channel.

## Final verdict

This direction is stronger than the earlier ordinary AI education plan for Substack.

**Go only if we commit to professional English, senior-builder depth, architecture diagrams, precise trade-offs, and paid validation.**

Otherwise it will collapse into generic AI content and fail.
