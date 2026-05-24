# Professional AI Product Architecture: 4 Pilot Briefs

Generated/normalized by scheduler supervisor at 2026-05-20T07:24:48. Source pilot files: content/pilots/pilot_01_cursor_architecture_teardown.md, content/pilots/pilot_02_test_time_compute_product.md

## pilot_01_cursor_architecture_teardown

Source: `content/pilots/pilot_01_cursor_architecture_teardown.md`

# Pilot Article Brief #1: Product Architecture Teardown

## Article Metadata

| Field | Value |
|-------|-------|
| **ID** | P001 |
| **Type** | Product Architecture Teardown |
| **Title** | How Cursor Probably Works: Codebase Indexing, Context Retrieval, and Agentic Editing |
| **Content Pillar** | AI Product Architecture Teardown |
| **Target Audience** | Senior backend engineers, AI startup CTOs, technical PMs |
| **Word Count Target** | 2,500-3,500 words |
| **Reading Time** | 12-15 minutes |
| **Production Estimate** | 10-12 hours |

---

## Core Thesis

Cursor is not just "GPT-4 in a code editor." It's a carefully architected system that solves three distinct engineering problems: (1) indexing large codebases in real-time, (2) retrieving relevant context at inference time, and (3) safely applying multi-file edits. Understanding this architecture reveals patterns applicable to any AI-powered developer tool.

---

## Article Structure

### 1. Hook (200 words)
**Opening Question**: Why can Cursor edit 5 files simultaneously while other AI coding tools struggle with single-file changes?

**Key Points**:
- Cursor's "wow moment" isn't the model—it's the system around it
- Architecture makes the difference between demo and production tool
- Three hard problems solved: indexing, retrieval, application

**Free Tier Cutoff**: After "three hard problems" introduction, transition to paid indicator

---

### 2. User Workflow Analysis (400 words)

**Document the actual user journey**:

1. **Codebase Ingestion**
   - Opening a project in Cursor
   - Initial indexing process (how long, what happens)
   - File watching for incremental updates

2. **Active Development Loop**
   - Editor-initiated requests (Cmd+K, Tab, Chat)
   - Model-initiated suggestions (predictive edits)
   - Agentic workflows (Composer mode)

3. **Output Application**
   - Single-file edits
   - Multi-file coordinated changes
   - Diff presentation and user control

**Diagram Required**: User flow diagram showing touchpoints with Cursor's systems

**Evidence Sources**:
- Cursor public docs: https://cursor.com/docs
- Cursor changelog analysis
- User behavior observation
- API behavior inference

---

### 3. Likely Architecture (800 words)

**Section Label**: [INFERRED FROM PRODUCT BEHAVIOR]

#### 3.1 Indexing System

**Hypothesis**: Incremental AST-based indexing with embedding storage

**Components**:
| Component | Likely Implementation | Evidence |
|-----------|----------------------|----------|
| Parser | Tree-sitter for multi-language support | Cursor supports 40+ languages |
| Embeddings | Local embedding model (likely small transformer) | Fast local search, offline capable |
| Storage | Local vector DB (likely LanceDB or similar) | No network requests for search |
| Incremental | File watcher + delta updates | Near-instant updates on save |

**Architecture Diagram**: Indexing pipeline showing file → AST → chunks → embeddings → vector store

**Trade-offs Discussed**:
- Local vs cloud indexing (latency, privacy, scale)
- AST vs token-based chunking (accuracy vs coverage)
- Incremental vs full re-index (consistency vs speed)

#### 3.2 Context Retrieval System

**Hypothesis**: Multi-stage retrieval with editor state awareness

**Retrieval Pipeline**:
1. **Explicit context**: User-selected code, open files
2. **Implicit context**: Cursor position, recent edits, error locations
3. **Semantic search**: Embedding-based retrieval from codebase index
4. **Reranking**: Cross-encoder

---

## pilot_02_test_time_compute_product

Source: `content/pilots/pilot_02_test_time_compute_product.md`

# Pilot Article Brief #2: Frontier Research to Product

## Article Metadata

| Field | Value |
|-------|-------|
| **ID** | P002 |
| **Type** | Research-to-Product Translation |
| **Title** | What Test-Time Compute Means for AI Products: From o1 to Your Application |
| **Content Pillar** | Frontier Research to Product |
| **Target Audience** | AI startup founders, technical PMs, AI application engineers |
| **Word Count Target** | 2,000-2,800 words |
| **Reading Time** | 10-12 minutes |
| **Production Estimate** | 8-10 hours |

---

## Core Thesis

OpenAI's o1 and the test-time compute paradigm isn't just a model improvement—it's a fundamental shift in AI product architecture. Products that treat inference as a single-pass operation will be outcompeted by those architected around multi-step reasoning, verification loops, and compute-time scaling. This article translates the research into implementation decisions.

---

## Article Structure

### 1. Hook (200 words)

**Opening Hook**: "o1 scored 83% on AIME math problems. GPT-4o scored 13%. The difference isn't training data—it's inference architecture."

**Key Points**:
- Test-time compute is an architectural pattern, not just a model
- Every AI product team needs to reconsider their inference design
- Three implementation patterns emerging from research

**Free Tier Cutoff**: After introducing the three patterns, transition to paid

---

### 2. Research Summary (What Actually Changed) (400 words)

**Section Label**: [CONFIRMED FROM PUBLISHED RESEARCH]

**Key Papers/Announcements**:

1. **OpenAI o1 System Card** (Sept 2024)
   - Chain-of-thought reasoning with scaling
   - Inference-time compute vs model size trade-off
   - Source: OpenAI o1 system card

2. **Scaling LLM Test-Time Compute Optimally** (DeepMind, 2024)
   - verifier-guided search approaches
   - compute allocation strategies
   - Source: DeepMind research publication

3. **Reasoning with Reinforced Search** (Multiple groups)
   - RL for search policy
   - Reward model training
   - Source: Anthropic, DeepMind papers

**Core Research Insights**:

| Finding | Implication |
|---------|-------------|
| More inference compute → better results | Latency/cost trade-off changes |
| Verifier quality matters as much as generator | Need evaluation infrastructure |
| Search strategies affect efficiency | Architecture decisions critical |
| CoT doesn't transfer directly | Product UX implications |

**Diagram Required**: Simple comparison of traditional vs test-time inference

---

### 3. Product Architecture Implications (700 words)

**Section Label**: [RESEARCH-TO-PRODUCT TRANSLATION]

#### 3.1 Pattern 1: Reasoning-as-a-Service

**Architecture**: Wrap reasoning in explicit API layer

**When to Use**:
- Complex analytical tasks
- Multi-step problem solving
- Decisions with verification steps

**Architecture Diagram**:
```
User Request → Router → [Fast Path / Reasoning Path]
                     ↓
              Reasoning Orchestrator
                     ↓
              [Generate → Verify → Iterate]
                     ↓
              Synthesized Response
```

**Implementation Notes**:
- Separate reasoning model from production model
- Streaming UI for long-running reasoning
- Cost controls (max reasoning steps)
- Cache common reasoning patterns

**Real Example**: Code review tools analyzing complex refactors

#### 3.2 Pattern 2: Hierarchical Planning

**Architecture**: Generate plan → execute steps → verify

**When to Use**:
- Multi-s

---


> NOTE: fewer than 4 dedicated pilot files currently exist; next task should add remaining briefs before publication.
