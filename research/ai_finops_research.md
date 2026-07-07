# AI FinOps Deep Research: A Framework for Enterprise AI Cost, Value, and Risk Management

*Prepared for a Principal AI Solutions Consultant designing a company-wide AI FinOps framework for a large, banking-adjacent, domain-generic enterprise portfolio.*

---

## 1. The FinOps Foundation's "FinOps for AI" Framework

The FinOps Foundation — the vendor-neutral standards body behind the FinOps Framework — formally extended its discipline from pure cloud cost management to a **"Cloud+"** model in 2025, adding **Scopes** as a first-class element to capture non-cloud technology spend, including AI, SaaS, licensing, and data centers ([FinOps Foundation, "FinOps Framework 2025"](https://www.finops.org/insights/2025-finops-framework/)). A **FinOps Scope** is defined as "a segment of technology-related spending to which FinOps Practitioners apply FinOps concepts," and Scopes are explicitly *not* mutually exclusive — meaning AI spend can span cloud, SaaS, and enterprise-agreement scopes simultaneously ([FinOps Foundation, 2025 Framework updates](https://www.finops.org/insights/2025-finops-framework/)). Notably, the 2025 State of FinOps survey found that "Optimization was the top priority for Cloud" but was *not* in the top five priorities for SaaS, AI, Licensing, or Data Centers — signaling that AI FinOps maturity still centers on visibility and allocation rather than optimization ([FinOps Foundation](https://www.finops.org/insights/2025-finops-framework/)).

The Foundation's dedicated **"FinOps for AI Overview"** whitepaper, produced by its AI Working Group, is the primary normative reference ([FinOps Foundation, "FinOps for AI Overview"](https://www.finops.org/wg/finops-for-ai-overview/)). Adoption has moved fast: **98% of FinOps teams now manage AI spend, up from just 31% two years earlier** ([FinOps Foundation, "AI Value" topic page](https://www.finops.org/topic/ai-value/)).

### 1.1 Phases: Crawl-Walk-Run mapped to Inform-Optimize-Operate

While the canonical FinOps lifecycle (Inform → Optimize → Operate) still applies, the AI-specific guidance frames AI maturity through a **Crawl / Walk / Run** adoption curve that nests inside it ([FinOps Foundation, "FinOps for AI Overview"](https://www.finops.org/wg/finops-for-ai-overview/)):

- **Crawl** — learning, prototyping, MVPs, pilots; "fail fast" with pre-agreed cost/time ceilings; manual cost calculations; non-financial success indicators dominate.
- **Walk** — integration into simple business processes; deployment/integration costs minimized to what's needed for daily use; basic automated cost tracking and anomaly detection appear; budgets split into run vs. release costs.
- **Run** — AI powers core business processes; costs must not fall below a baseline relative to business benefit; advanced anomaly tracking; **total ROI from the AI model** becomes a governing metric; budgets are granular and relatively stable.

This nests inside the classic **Inform** (cost/usage visibility), **Optimize** (rate and workload optimization), **Operate** (continuous governance) phases that structure the broader FinOps Framework, with token-level metering added to the "Understand Usage and Cost" domain and AI-specific unit metrics added to "Quantify Business Value" ([FinOps Foundation, "Token Economics: The Atomic Unit of AI Value"](https://www.finops.org/insights/token-economics-the-atomic-unit-of-ai-value/)).

### 1.2 AI-specific personas

The FinOps for AI Overview names eight AI-specific personas beyond the traditional Engineering/Finance/Leadership/Procurement FinOps audience ([FinOps Foundation](https://www.finops.org/wg/finops-for-ai-overview/)):

1. **Data Scientists** — develop/fine-tune models, consume training and evaluation compute.
2. **Data Engineers** — build and maintain data pipelines feeding AI systems.
3. **Software/Prompt/Automation Engineers** — integrate AI into applications via APIs.
4. **Business Analysts** — consume AI-derived insights for decisions and reporting.
5. **DevOps Engineers** — manage infrastructure and resource allocation.
6. **Product Managers** — define AI feature requirements and monitor value delivered.
7. **Leadership** — set adoption goals, approve budgets, define success criteria.
8. **End Users** — consume AI-enriched outputs via SaaS, dashboards, or copilots.

### 1.3 How AI FinOps differs from cloud FinOps

The Foundation is explicit that the basic **Price × Quantity = Cost** equation still holds, billing still flows through cloud bills, and tagging/rate-optimization remain core tools ([FinOps Foundation](https://www.finops.org/wg/finops-for-ai-overview/)). But several structural differences change practice:

- **Volatile, inconsistent pricing** — AI vendors ship new SKUs constantly, some untaggable natively, requiring engineering tooling for cost attribution.
- **Tokens as the atomic unit** — the "meter" is now tokens (input/output/cached), not compute-hours; measuring tokens at user input differs from the compressed/rewritten tokens actually billed by the API.
- **GPU scarcity** — capacity management techniques (reservations, provisioned throughput) are needed because of infrastructure scarcity uncommon in general cloud services.
- **New stakeholders** — product, marketing, sales, and executive leadership now directly shape consumption, not just engineering.
- **Quality as a cost lever** — teams must trade off smaller/cheaper models against frontier reasoning models to hit a minimum quality bar, a dimension absent from most traditional cloud workloads.
- **Continuous training** as an ongoing cost center rather than a one-time capital cost.

The FinOps Foundation's practitioner survey found that **managing the cost and use of tokens in SaaS-model AI is the single top challenge facing practitioners today**, rooted in developer-led purchasing, opaque billing, absent native allocation mechanisms, and highly variable per-tier pricing ([FinOps Foundation, "Token Economics: Managing AI Value in SaaS Model Token Costs"](https://www.finops.org/wg/token-economics-saas/)).

---

## 2. Unit Economics for AI Workloads

The FinOps Foundation's **Unit Economics capability** states that for organizations adopting generative AI, "early unit economics often starts with cost per token and expands toward outcome-oriented measures, for example cost per assist, cost per agent action, or cost per case deflected" ([FinOps Foundation, "Capability: Unit Economics"](https://www.finops.org/framework/capabilities/unit-economics/)). The core formulas, with worked examples from the Foundation's own guidance:

| Metric | Formula | Worked example |
|---|---|---|
| Cost per inference/API call | Total Inference/API Cost ÷ Number of Requests | $5,000 ÷ 100,000 requests = **$0.05/request** ([FinOps Foundation](https://www.finops.org/wg/finops-for-ai-overview/)) |
| Cost per token | Total Cost ÷ Tokens Used | $2,500 ÷ 1,000,000 tokens = **$0.0025/token** ([FinOps Foundation](https://www.finops.org/wg/finops-for-ai-overview/)) |
| Cost per API call (managed services) | Total API Cost ÷ Number of Calls | $1,200 ÷ 240,000 = **$0.005/call** ([FinOps Foundation, Unit Economics capability](https://www.finops.org/framework/capabilities/unit-economics/)) |
| ROI on AI initiative | (Financial Benefits − Costs) ÷ Costs × 100 | ($50,000 − $20,000) ÷ $20,000 × 100 = **150%** ([FinOps Foundation](https://www.finops.org/framework/capabilities/unit-economics/)) |
| Time to Business Value | Total value from AI service ÷ daily cost of alternative | Forecast $100k/mo in 1 month; actual $50k/mo achieved in 5 months → **5-month time-to-value** ([FinOps Foundation](https://www.finops.org/wg/finops-for-ai-overview/)) |

Beyond these foundational metrics, practitioner guidance converges on a small set of **outcome-tied unit economics** that FinOps teams should graduate to as maturity increases ([FinOps Foundation, "Token Economics: Managing AI Value in SaaS Model Token Costs"](https://www.finops.org/wg/token-economics-saas/)):

- **Cost per query/API call** — capacity planning.
- **Cost per user per month** — comparison against seat-based SaaS alternatives.
- **Cost per workflow completion** — total cost of a multi-step agentic process, the basis for agent ROI.
- **Cost per business transaction** — AI cost embedded in a broader unit (e.g., cost of AI-assisted ticket resolution).

A general-purpose "cost per outcome" formula recommended in industry practice is:

\[
\text{Cost per Outcome} = \frac{\text{Tokens} \times \text{Cost per Token}}{\text{Outcomes Delivered}}
\]

This reframes the conversation from "how much are we spending" to "what are we getting per token" ([AIM Consulting, "Finding Business Value with AI"](https://aimconsulting.com/insights/finops-for-ai-business-value/)). Practically, "success" must be operationalized per use case before cost-per-outcome is meaningful:

- **Customer support / conversational AI** — cost per *resolved* conversation (not cost per conversation started), typically defined as containment without human escalation or a satisfaction-score threshold, tied to the business KPI of case deflection rate and CSAT.
- **Coding/developer copilots** — cost per *accepted* suggestion (accept rate × suggestions served), tied to developer velocity and defect-rate KPIs, not raw completion volume.
- **Sales/marketing content generation** — cost per *approved/published* asset, tied to campaign conversion or pipeline-influenced revenue.
- **Document processing/agents** — cost per *correctly completed* workflow (straight-through-processing rate), tied to cycle-time and error-rate KPIs.

The FinOps Foundation stresses this same principle: metadata attribution should "measure AI impact through chatbot response times, interaction frequency, resolution rates, and cost per engagement" and correlate spend with business KPIs such as "chatbot-driven conversions and peak usage periods" ([FinOps Foundation, "Choosing an AI Approach and Infrastructure Strategy"](https://www.finops.org/wg/choosing-an-ai-approach-and-infrastructure-strategy/)). Microsoft's FinOps toolkit guidance operationalizes the arithmetic against FOCUS-conformed billing data: **Unit Cost = EffectiveCost ÷ ConsumedQuantity**, applied per model, team, and feature ([Microsoft Tech Community, "Managing Azure OpenAI costs with the FinOps toolkit and FOCUS"](https://techcommunity.microsoft.com/blog/finopsblog/managing-azure-openai-costs-with-the-finops-toolkit-and-focus-turning-tokens-int/4413886)).

---

## 3. Cost Drivers in Modern AI Stacks

### 3.1 Token pricing structure

Nearly every frontier LLM now prices on three axes — **input, output, and cached input** — with output tokens typically costing **3–5x more than input tokens** because generation is more compute-intensive than context processing ([HostingX, "Kubernetes FinOps: SaaS Unit Economics"](https://hostingx.co.il/articles/kubernetes-finops-unit-economics)). Cached input (prompt/context caching) is typically priced at roughly **10% of standard input cost** for cache reads, with a modest premium (~25%) for the initial cache write ([Anthropic, "Prompt caching with Claude"](https://www.anthropic.com/news/prompt-caching)).

### 3.2 Model routing and cascading

Routing sends each request to the cheapest model capable of meeting a quality bar, rather than defaulting every request to a frontier model. The FinOps for AI guidance formalizes this as an explicit KPI — **"LM Model Choice Quality Score Alignment"** — comparing the MMLU (or other benchmark) score actually required by a task against the score of the model in use, flagging waste when a high-cost model answers a low-complexity prompt ([FinOps Foundation, "FinOps for AI Overview"](https://www.finops.org/wg/finops-for-ai-overview/)).

### 3.3 Fine-tuning vs. prompting vs. RAG cost tradeoffs

- **Prompting/few-shot** has near-zero upfront cost but pays a per-call "tax" on every request (larger context = more input tokens each time).
- **RAG** adds infrastructure cost (embeddings + vector database + retrieval latency) but keeps the base model frozen and avoids retraining costs; it dominates when knowledge changes frequently.
- **Fine-tuning** carries high upfront training cost (compute + data curation + evaluation) but can reduce per-call token counts (shorter prompts, no need to inject instructions/examples) and improve task-specific accuracy, making it attractive at very high call volumes on stable tasks.

### 3.4 Retrieval costs

RAG cost has two components: **embeddings generation** (a one-time or incremental cost per document chunk) and **vector database operations** (storage + read/write units per query). Pinecone's own pricing shows embedding inference at **$0.08–$0.16 per million tokens** depending on model, and reranking at **$2.00 per 1,000 requests** ([CheckThat.ai, "Pinecone Pricing 2026"](https://checkthat.ai/brands/pinecone/pricing)); vector query costs on Pinecone's serverless tier run roughly **$0.33 per million read units** with an effective cost near **$0.0000026 per single top-k=10 query** on 1536-dimension vectors ([LeanOps, "Pinecone Costs 4-8x Self-Hosted Past 10M Vectors"](https://leanopstech.com/blog/pinecone-pricing-2026/)).

### 3.5 Agent/tool-call overhead, evaluation, guardrails, HITL, and observability

- **Agent/tool-call overhead** — every tool invocation in a multi-step agent consumes tokens for reasoning traces, tool schemas, and intermediate outputs; the FinOps Foundation recommends tracking "cost per workflow completion" precisely because agentic costs compound across steps in ways a single cost-per-call metric hides ([FinOps Foundation, "Token Economics: Managing AI Value"](https://www.finops.org/wg/token-economics-saas/)).
- **Evaluation costs** — running eval suites (LLM-as-judge, human eval, regression tests) consumes additional model calls on every release; this is a recurring operating cost often excluded from naive TCO models.
- **Guardrail/safety costs** — content moderation and safety classifiers (input and output screening) run as an additional inference pass per request, per OWASP's guidance on treating LLM output as untrusted ([OWASP, "LLM05:2025 Improper Output Handling"](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)).
- **Human-in-the-loop (HITL) costs** — labor cost of human review/approval steps for high-stakes or low-confidence outputs; OWASP explicitly recommends "human oversight" and approval gates for consequential agent actions ([OWASP LLM Top 10 2025 — LLM06 Excessive Agency](https://www.trydeepteam.com/docs/red-teaming-owasp-top-10-for-llms)).
- **Platform/observability costs** — LLM observability tooling (e.g., Langfuse, Helicone, LangWatch) auto-captures token usage and traces but adds a per-seat or per-event platform cost layered atop model spend ([Amnic, "How to Track AI Cost: A FinOps Method"](https://amnic.com/blogs/how-to-track-ai-cost)).

---

## 4. Current (2025–2026) Pricing Benchmarks

All figures below are per 1 million tokens (MTok) unless noted, drawn directly from vendor pricing pages, with effective dates where published.

### 4.1 Frontier proprietary model API pricing (direct provider APIs)

| Model | Input | Cached input (read) | Output | Source / effective date |
|---|---:|---:|---:|---|
| GPT-4o | $2.50 | $1.25 | $10.00 | [OpenAI Platform Docs](https://platform.openai.com/docs/models/gpt-4o-mini) |
| GPT-4o-mini | $0.15 | $0.075 | $0.60 | [OpenAI Platform Docs](https://platform.openai.com/docs/models/gpt-4o-mini) |
| Claude Sonnet 4.5 | $3.00 | $0.30 (5-min cache read) | $15.00 | [Anthropic/Claude Platform Docs pricing](https://platform.claude.com/docs/en/about-claude/pricing) |
| Claude Haiku 4.5 | $1.00 | $0.10 | $5.00 | [Claude Platform Docs pricing](https://platform.claude.com/docs/en/about-claude/pricing) |
| Claude Opus (current flagship tier) | $5.00 | $0.50 | $25.00 | [Claude Platform Docs pricing](https://platform.claude.com/docs/en/about-claude/pricing) |
| Gemini 2.5 Pro (≤200K tokens) | $1.25 | $0.13 | $10.00 | [Google Cloud Vertex AI pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Gemini 2.5 Pro (>200K tokens) | $2.50 | $0.25 | $15.00 | [Google Cloud Vertex AI pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| Gemini 2.5 Flash | $0.30 (text/image/video) | $0.03 | $2.50 | [Google Cloud Vertex AI pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing) |

Notes: Claude Sonnet 4.5 also offers a **1-hour cache write** tier at $6/MTok versus $3.75/MTok for the standard 5-minute cache write, and **batch API pricing at 50% off** standard rates ($1.50 input / $7.50 output) ([Claude Platform Docs pricing](https://platform.claude.com/docs/en/about-claude/pricing)). GPT-4o's own batch pricing likewise runs at roughly 50% off standard rates. Anthropic confirmed at launch that "pricing remains the same as Claude Sonnet 4, at $3/$15 per million tokens" for Sonnet 4.5 ([Anthropic, "Introducing Claude Sonnet 4.5"](https://www.anthropic.com/news/claude-sonnet-4-5)).

### 4.2 Open-weights models on hyperscaler platforms

**Google Vertex AI** ([Google Cloud Vertex AI pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing)):

| Model | Input ($/MTok) | Output ($/MTok) |
|---|---:|---:|
| Llama 3.3 70B | $0.72 | $0.72 |
| Llama 4 Scout | $0.25 | $0.70 |
| Llama 4 Maverick | $0.35 | $1.15 |
| Mistral Medium 3 | $0.40 | $2.00 |
| Mistral Small 3.1 | $0.10 | $0.30 |

**AWS Bedrock** ([AWS Bedrock Pricing](https://aws.amazon.com/bedrock/pricing/)):

| Model | Input ($/MTok) | Output ($/MTok) |
|---|---:|---:|
| Llama 2 Chat 70B | $1.95 | $2.56 |
| Llama 2 Chat 13B | $0.75 | $1.00 |
| Mistral Large 3 | $0.50 | $1.50 |
| Ministral 8B 3.0 | $0.15 | $0.15 |
| Claude 3.5 Sonnet (on-demand, current public extended access rate effective Dec 1, 2025) | $6.00 | $30.00 |

The Bedrock Claude 3.5 Sonnet rate above reflects a **"Public Extended Access"** tier published effective December 1, 2025, notably higher than Anthropic's own direct-API Sonnet pricing — illustrating that **platform choice materially changes effective unit economics for the same model family**, and FinOps teams must compare direct-API, Bedrock, Vertex, and Azure pricing per model rather than assuming parity ([AWS Bedrock Pricing](https://aws.amazon.com/bedrock/pricing/)).

**Azure OpenAI** offers the same GPT-4o/4o-mini token rates as OpenAI's direct API on pay-as-you-go, plus a **Provisioned Throughput Unit (PTU)** model for guaranteed capacity; Azure introduced **monthly PTU commitments** in addition to yearly-only commitments as of late 2024/2025, giving enterprises a mid-length reservation option to balance against pay-as-you-go economics ([FinOps Foundation, "FinOps for AI Overview"](https://www.finops.org/wg/finops-for-ai-overview/); [Microsoft Tech Community, PTU pricing](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/unveiling-azure-openai-service-provisioned-reservations-and-hourly-pricing/4214560)).

### 4.3 Vector database pricing

| Provider | Pricing model | Rate | Source |
|---|---|---|---|
| Pinecone (Standard, serverless) | Storage + read/write units | ~$0.33/GB-month storage; ~$8.25–$16 per 1M read units; ~$2–$4 per 1M write units; $50/month minimum | [Pinecone Pricing](https://www.pinecone.io/pricing/); [PE Collective Pinecone pricing analysis](https://pecollective.com/tools/pinecone-pricing/) |
| Pinecone Enterprise | Storage + read/write units | Higher per-unit rates; $500/month minimum | [UsagePricing, Pinecone](https://www.usagepricing.com/blueprint/pinecone) |
| Weaviate Cloud | Free tier | 100,000 objects, 1GB memory, 10GB disk, 2,000 embedding req/day free | [Weaviate Pricing](https://weaviate.io/pricing) |
| pgvector (self-hosted on Postgres) | Compute/storage only (no per-query fee) | Cost = underlying Postgres instance cost; no vendor markup | Widely documented as the low-cost, self-managed alternative when query volume is high and vendor lock-in is a concern |
| OpenSearch (AWS-managed, with k-NN plugin) | Cluster compute + storage | Standard OpenSearch Service instance/storage pricing; no separate vector fee | Vector search is a plugin feature on existing OpenSearch infrastructure pricing |

**Effective dates:** Pinecone pricing reflects **2026 published rates**; Vertex AI Gemini and open-weights pricing reflects the **current Google Cloud pricing page**; Anthropic/Claude pricing reflects the **current Claude Platform Docs pricing page**; AWS Bedrock rates reflect the page's **stated effective date of December 1, 2025** for the Claude Public Extended Access tier ([AWS Bedrock Pricing](https://aws.amazon.com/bedrock/pricing/)).

---

## 5. FinOps Optimization Levers and Realistic Impact Ranges

| Lever | Mechanism | Typical impact | Source |
|---|---|---|---|
| **Prompt caching** | Reuse previously processed context (system prompts, long documents) at ~10% of input cost | **Up to 90% cost reduction and up to 85% latency reduction** on long, repeated-context prompts; observed 53–90% cost reduction and 31–79% latency reduction across Anthropic's own benchmark scenarios | [Anthropic, "Prompt caching with Claude"](https://www.anthropic.com/news/prompt-caching) |
| **Semantic caching** | Serve semantically similar queries from cache instead of re-invoking the model | **45.1% reduction in LLM queries** in a published EdTech case study (vs. 30.4% for traditional exact-match caching), with **3.9×–12× latency improvement** on cache hits | [SBC/SBRC academic case study, "Evaluating Semantic Caching in Practice"](https://sol.sbc.org.br/index.php/sbrc_estendido/article/download/35896/35683/) |
| **Model cascading/routing** | Route simple queries to cheap/small models, escalate only when needed | Reported real-world savings commonly cited in the 30–50% range for mixed-complexity workloads (vendor and practitioner reporting; treat as directional, not audited) | [FinOps Foundation, "FinOps for AI Overview" — MMLU alignment KPI](https://www.finops.org/wg/finops-for-ai-overview/) |
| **Batch inference** | Accept a completion-time SLA (e.g., 24 hours) for a flat discount | **Flat 50% discount** on both input and output tokens across OpenAI's Batch API; Anthropic's Batch API offers the same 50% off structure | [OpenAI Pricing docs](https://developers.openai.com/api/docs/pricing); [Claude Platform Docs pricing](https://platform.claude.com/docs/en/about-claude/pricing) |
| **Output length caps / prompt compression** | Constrain max tokens, strip redundant system-prompt verbosity, summarize long context | Cost is linear in tokens, so trimming verbose system prompts or capping max_output_tokens produces proportional savings; FinOps Foundation recommends auditing system prompts for "verbosity, redundancy" as a standard optimization pass | [FinOps Foundation, "Token Economics: Managing AI Value in SaaS Model Token Costs"](https://www.finops.org/wg/token-economics-saas/) |
| **Conversation summarization / sliding window** | Replace full chat history with a compact summary or recent-N-turns window | Converts an O(n²) token-growth pattern (full history resent every turn) into near-constant per-turn cost | [FinOps Foundation](https://www.finops.org/wg/token-economics-saas/) |
| **RAG top-k tuning / reranker gating** | Retrieve fewer, higher-precision chunks; only invoke a reranker when initial retrieval confidence is low | Reduces both embedding/vector-query cost and downstream input-token volume fed to the LLM; rerankers add ~$2.00 per 1,000 requests, so gating them behind a confidence threshold avoids paying for reranking on already-confident retrievals | [CheckThat.ai, Pinecone add-on pricing](https://checkthat.ai/brands/pinecone/pricing) |
| **Distillation / fine-tuning smaller models** | Train a smaller model to replicate a larger model's behavior on a narrow task | Enables replacing an expensive frontier-model call with a cheap fine-tuned small model at inference time; upfront training cost is amortized over call volume | General industry practice; see FinOps Foundation Compute Cost Optimization guidance on model right-sizing ([FinOps Foundation](https://www.finops.org/wg/choosing-an-ai-approach-and-infrastructure-strategy/)) |
| **Provisioned throughput / commitment discounts** | Pre-purchase capacity (PTUs, throughput units) instead of pay-as-you-go | Azure's own published example shows a **1-month PTU reservation at ~$0.3562/hour vs. ~$1/hour on-demand — roughly 64% savings** for sustained utilization, effective January 1, 2025 pricing | [Microsoft Tech Community, "Provisioned Reservations and Hourly Pricing"](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/unveiling-azure-openai-service-provisioned-reservations-and-hourly-pricing/4214560) |

**Governance guardrail on savings claims:** the FinOps Foundation's own guidance stresses that a sophisticated approach requires shifting focus "from the token to the use case," measuring unit economics of the entire business outcome rather than the individual API call, because narrow token-level optimization can degrade the very outcome the AI system exists to produce ([FinOps Foundation, "GenAI FinOps: How Token Pricing Really Works"](https://www.finops.org/wg/genai-finops-how-token-pricing-really-works/)).

---

## 6. AI Governance and Risk Overlays That Touch Cost

### 6.1 Model risk management (SR 11-7 / OCC guidance) — now in transition

The Federal Reserve's **SR 11-7** ("Supervisory Guidance on Model Risk Management," 2011) has long been the definitive US banking-sector framework requiring independent model validation, ongoing monitoring, and governance for any quantitative model used in decision-making ([Federal Reserve, SR 11-7](https://www.federalreserve.gov/boarddocs/srletters/2011/sr1107.pdf)). **This changed materially in April 2026**: the OCC, Federal Reserve Board, and FDIC jointly issued **updated model risk management guidance (OCC Bulletin 2026-13)** that **rescinds the prior OCC Bulletin 2011-12** (the OCC's SR 11-7-aligned issuance) and several related bulletins, replacing prescriptive requirements with a risk-based, size-and-complexity-tailored approach most relevant to institutions with **over $30 billion in total assets** ([OCC News Release 2026-29](https://www.occ.gov/news-issuances/news-releases/2026/nr-occ-2026-29.html)). Critically, the new guidance **explicitly excludes generative AI and agentic AI models from its scope**, calling them "novel and rapidly evolving," while flagging that regulators plan a forthcoming request for information specifically addressing banks' use of AI, generative AI, and agentic AI models ([OCC News Release 2026-29](https://www.occ.gov/news-issuances/news-releases/2026/nr-occ-2026-29.html)). For a Principal AI Solutions Consultant, this means: (1) legacy MRM validation cost models built around SR 11-7 cannot simply be extended to GenAI systems without new methodology, and (2) banking clients should expect near-term regulatory guidance specifically on GenAI/agentic model risk, which will likely add new validation and monitoring cost lines.

### 6.2 NIST AI RMF 1.0

NIST released the **AI Risk Management Framework 1.0** on **January 26, 2023**, a voluntary, sector-agnostic framework built around four functions — **Govern, Map, Measure, Manage** — with Govern applying across the full AI lifecycle ([NIST, AI RMF 1.0 PDF](https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf); [NIST AI RMF program page](https://www.nist.gov/itl/ai-risk-management-framework)). On **July 26, 2024**, NIST released a companion **Generative AI Profile (NIST-AI-600-1)** identifying GenAI-specific risks ([NIST AI RMF program page](https://www.nist.gov/itl/ai-risk-management-framework)). As of **April 7, 2026**, NIST released a concept note for an **AI RMF Profile on Trustworthy AI in Critical Infrastructure**, signaling continued framework expansion relevant to energy, telecom, and public-sector overlays ([NIST AI RMF program page](https://www.nist.gov/itl/ai-risk-management-framework)). Cost implication: each of the four functions (especially Measure) implies recurring evaluation, red-teaming, and monitoring costs that should be budgeted as a percentage of AI program spend, not treated as one-time.

### 6.3 EU AI Act

The EU AI Act defines four risk tiers (unacceptable, high, limited, minimal) with tiered penalties: **up to €35M or 7% of global turnover** for prohibited practices, **up to €15M or 3%** for high-risk non-compliance, **up to €20M or 4%** for limited-risk transparency/data violations, and **up to €7.5M or 1.5%** for other infringements ([SQ Magazine, "EU AI Act Compliance Cost Statistics 2026"](https://sqmagazine.co.uk/eu-ai-act-compliance-cost-statistics/); [CheckCompliance.eu](https://www.checkcompliance.eu/cost/)). AI literacy (Article 4) and prohibited-practice bans (Article 5) have been enforceable **since February 2025**; **high-risk system obligations are set to take effect August 2, 2026**, though a Digital Omnibus proposal from May 2026 seeks to defer this to December 2, 2027 (not yet formally adopted) ([CheckCompliance.eu](https://www.checkcompliance.eu/cost/)). High-risk obligations include a continuous **risk management system (Article 9)**, **data governance (Article 10)**, **technical documentation (Article 11)**, **automatic logging retained a minimum of 6 months (Articles 12–14)**, and **Fundamental Rights Impact Assessments** for credit, insurance, and public-sector use cases ([Cloud Security Alliance, "EU AI Act High-Risk Deadline"](https://labs.cloudsecurityalliance.org/research/csa-research-note-eu-ai-act-high-risk-compliance-deadline-20/)). Published compliance-cost estimates: **€15,000–€40,000/year** in ongoing maintenance for a mid-size organization, **€80,000–€250,000** first-year cost for a single high-risk system, and **over €1 million** for enterprises with multiple Annex III deployments ([DEV Community, "What EU AI Act Compliance Actually Costs"](https://dev.to/appz_b0659e1ca24e36738948/what-eu-ai-act-compliance-actually-costs-and-where-the-money-goes-4d71)).

### 6.4 ISO/IEC 42001

**ISO/IEC 42001:2023** is the first international certifiable standard for an **AI Management System (AIMS)**, specifying requirements to establish, implement, maintain, and continually improve organizational AI governance, covering fairness, transparency, accountability, and privacy ([Microsoft Learn, ISO 42001 compliance offering](https://learn.microsoft.com/en-us/compliance/regulatory/offering-iso-42001); [PECB, ISO/IEC 42001](https://pecb.com/en/education-and-certification-for-individuals/iso-iec-42001)). As a certifiable standard (unlike NIST AI RMF, which is voluntary/non-certifiable), ISO 42001 creates a recurring **audit cost line** — internal audits, surveillance audits, and re-certification — that enterprises should budget as part of the AI governance operating cost, distinct from one-time compliance projects.

### 6.5 OWASP Top 10 for LLM Applications (2025)

OWASP's 2025 refresh reorders and reworks the list based on production incident data ([OWASP Gen AI Security Project, "LLM01:2025 Prompt Injection"](https://genai.owasp.org/llmrisk/llm01-prompt-injection/); [Invicti, "OWASP Top 10 for LLMs 2025"](https://www.invicti.com/blog/web-security/owasp-top-10-risks-llm-security-2025)):

1. **LLM01: Prompt Injection** (direct + indirect)
2. **LLM02: Sensitive Information Disclosure** (jumped from #6 to #2)
3. **LLM03: Supply Chain** (renamed/broadened, #5→#3)
4. **LLM04: Data and Model Poisoning**
5. **LLM05: Improper Output Handling** (#2→#5)
6. **LLM06: Excessive Agency** (significantly expanded: excessive functionality, permissions, autonomy)
7. **LLM07: System Prompt Leakage** (new)
8. **LLM08: Vector and Embedding Weaknesses** (new — directly relevant to RAG architectures)
9. **LLM09: Misinformation** (replaces Overreliance)
10. **LLM10: Unbounded Consumption** (replaces Model Denial of Service — directly a cost-control risk)

Two of these map straight to FinOps cost control: **LLM10 (Unbounded Consumption)** is explicitly a resource/cost-management risk requiring per-key budgets, token-length caps, and rate limits ([Future AGI, "OWASP LLM Top 10 (2025)"](https://futureagi.com/blog/owasp-llm-top-10-2025-risks-mitigations-2026/)), and **LLM06 (Excessive Agency)** requires human-approval gates on consequential agent actions — a direct HITL cost driver ([OWASP Top 10 walkthrough](https://www.trydeepteam.com/docs/red-teaming-owasp-top-10-for-llms)).

### 6.6 How governance translates into cost

| Governance requirement | Cost category created |
|---|---|
| NIST AI RMF "Measure" function; EU AI Act Article 9 risk management | Recurring evaluation/red-teaming spend |
| EU AI Act Article 12 logging (6-month minimum retention) | Observability/logging storage and platform cost |
| ISO 42001 certification | Annual audit fees, internal audit labor |
| OWASP LLM06 (Excessive Agency), LLM10 (Unbounded Consumption) | Guardrail inference passes, human-in-the-loop review labor, rate-limiting infrastructure |
| Bank MRM (post-SR 11-7 transition) for GenAI | Independent validation labor pending forthcoming regulator guidance |
| EU AI Act Fundamental Rights Impact Assessments (credit, insurance) | Pre-deployment legal/compliance review cost per use case |

---

## 7. Chargeback/Showback for AI

FinOps orthodoxy distinguishes **showback** (visibility without billing) from **chargeback** (actual internal billing to cost centers), and the AI-specific guidance recommends progressing from tagging → showback → chargeback as maturity increases, rather than jumping straight to chargeback ([FinOps Foundation, "Token Economics: Managing AI Value in SaaS Model Token Costs"](https://www.finops.org/wg/token-economics-saas/)).

**Allocation bases** commonly used for AI, in increasing order of sophistication:

1. **Tokens consumed** — simplest, closest to the underlying bill, but doesn't reflect value delivered.
2. **Requests/API calls** — easier for business stakeholders to reason about, but obscures cost variance driven by prompt/response length.
3. **Cost per workflow completion / cost per outcome** — most accurate for chargeback fairness, but requires instrumentation to tie multi-step agent traces to a single business outcome.
4. **Proportionate/rule-based allocation for shared resources** — the FinOps Foundation recommends explicit rule-based splits (e.g., 70% analytics / 30% AI inferencing) when infrastructure is shared across AI and non-AI workloads ([FinOps Foundation, "Choosing an AI Approach and Infrastructure Strategy"](https://www.finops.org/wg/choosing-an-ai-approach-and-infrastructure-strategy/)).

**Implementation steps** recommended by the Foundation: (1) inventory every model-provider account, API key, and payment method; (2) deploy API key governance and a proxy layer to capture attribution data; (3) tag every call with calling application, team, and environment; (4) aggregate in a proxy analytics layer and export to the data warehouse for FOCUS-conformed reporting ([FinOps Foundation, "Token Economics: Managing AI Value"](https://www.finops.org/wg/token-economics-saas/)). For budgeting, the Foundation recommends instrumenting for **30–60 days to establish a baseline**, then setting budgets at **110–120% of baseline** with alerts at **80% and 100%** of budget ([FinOps Foundation, "Token Economics: Managing AI Value"](https://www.finops.org/wg/token-economics-saas/)).

**Incentive design and common pitfalls:**

- **Perverse incentive of pure token-based chargeback**: teams that innovate with more expressive (token-heavy) prompts get penalized relative to teams doing less valuable but token-light work — undermining the goal of maximizing business value per dollar. The Foundation's fix is to pair token-based showback with outcome-based chargeback once instrumentation matures.
- **Developer-led shadow purchasing**: because AI APIs can be adopted with a personal or team credit card and no procurement gate, chargeback frequently under-counts true spend unless API-key governance is centralized first — the Foundation names this as a root cause of the token-management challenge broadly ([FinOps Foundation, "Token Economics: Managing AI Value"](https://www.finops.org/wg/token-economics-saas/)).
- **SKU churn breaking allocation**: constantly changing model SKUs (new versions, deprecations) break static tagging schemes; the Foundation recommends dynamic, rule-based tagging rather than static tag dictionaries ([FinOps Foundation, "Choosing an AI Approach and Infrastructure Strategy"](https://www.finops.org/wg/choosing-an-ai-approach-and-infrastructure-strategy/)).
- **Chargeback without context discourages experimentation**: charging full price for Crawl-phase pilots can kill innovation before value is proven; the Crawl/Walk/Run model implies lighter-touch showback (not chargeback) during early-stage pilots ([FinOps Foundation, "FinOps for AI Overview"](https://www.finops.org/wg/finops-for-ai-overview/)).
- **Ignoring shared/platform costs**: observability tooling, guardrail infrastructure, and vector database platform costs are often shared services that get left out of per-team chargeback, understating true unit economics.

---

## 8. ROI Methodology for AI Programs

### 8.1 Incremental vs. gross benefits and the enterprise EBIT gap

McKinsey's **State of AI in 2025** survey (fielded June 25–July 29, 2025; 1,993 respondents, 105 countries) found that while **88% of organizations report regular AI use in at least one business function** (up from 78% a year earlier), only **39% attribute any enterprise-level EBIT impact to AI**, and most of those attribute **less than 5% of EBIT** to it ([McKinsey, "The state of AI in 2025"](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai)). McKinsey identifies **"AI high performers"** — about **6% of respondents** — as those attributing ≥5% EBIT impact to AI *and* reporting "significant" value; these firms disproportionately redesign workflows, track well-defined KPIs, and give the CEO direct oversight of AI governance, which McKinsey found to be the single organizational factor most correlated with higher self-reported bottom-line AI impact ([McKinsey, "The State of AI: How organizations are rewiring to capture value"](https://www.mckinsey.com/~/media/mckinsey/business%20functions/quantumblack/our%20insights/the%20state%20of%20ai/2025/the-state-of-ai-how-organizations-are-rewiring-to-capture-value_final.pdf)). This gap between local (use-case) ROI and enterprise (EBIT) ROI is the central methodological challenge: **cost-per-outcome metrics prove local value; only workflow redesign and adoption at scale convert that into enterprise financial impact.**

### 8.2 BCG's "future-built" benchmark and productivity gains

BCG's September 2025 study of 1,250+ global firms found only **5% of companies generate measurable AI value at scale** (defined as revenue/cash-flow increases plus process/workflow improvements), while **60% see little to no material value** despite substantial investment ([BCG, "Are You Generating Value from AI? The Widening Gap"](https://www.bcg.com/publications/2025/are-you-generating-value-from-ai-the-widening-gap)). The "future-built" 5% achieve **1.7x the revenue growth, 3.6x the three-year total shareholder return, 2.7x the return on invested capital, and 1.6x the EBIT margin** of peers, while planning to spend **26% more on IT** and dedicate **up to 64% more of IT budget to AI** ([BCG, "The Widening AI Value Gap" PDF](https://media-publications.bcg.com/The-Widening-AI-Value-Gap-Sept-2025.pdf)). BCG's January 2026 tech-function-specific research found **software development productivity gains of 25% today, rising to an expected 44% at full scale**; **IT service-desk automation delivering 20–30% shorter handling times and 25–40% higher first-contact resolution**; and **AI agents delivering 30–50% efficiency gains and 3–10 points of profit-margin improvement** in cited examples, with agentic AI's share of total company AI value expected to almost double from **17% in 2025 to 29% by 2028** ([BCG, "How AI Is Paying Off in the Tech Function"](https://www.bcg.com/publications/2026/how-ai-is-paying-off-in-the-tech-function)).

### 8.3 Adoption curves and attribution windows

BCG's adoption-stage model identifies five stages from "AI as search engine" to "fully autonomous orchestration," and finds the **inflection point for real value creation occurs at stage four (semiautonomous collaboration)** — yet **more than 85% of employees remain stuck at stages two and three**, with **fewer than 10%** reaching stage four or beyond ([BCG, "AI Adoption Puzzle: Why Usage Is Up But Impact Is Not"](https://www.bcg.com/publications/2025/ai-adoption-puzzle-why-usage-up-impact-not)). BCG's 2026 frontline-worker survey (~12,000 respondents) found **74% of frontline employees are now regular AI users** (up from ~50% in prior years), with **42% of regular users saving a full workday per week** — but **66% receive limited or no guidance on how to reinvest that saved time**, meaning realized productivity savings frequently do not convert to measured output gains without deliberate workflow redesign ([BCG, "AI at Work: Why Strategy Matters More Than Tools"](https://www.bcg.com/publications/2026/ai-at-work-why-strategy-matters-more-than-tools)). This is the practical basis for setting **attribution windows and counterfactuals**: ROI models should separate (a) time saved, (b) time reinvested into measurable output, and (c) the lag between adoption and reinvestment, rather than assuming 1:1 conversion of time saved into financial benefit.

### 8.4 Gartner's caution on project failure

Widely cited Gartner research projects that **30% of generative AI projects will be abandoned after proof-of-concept by end of 2025** due to poor data quality, inadequate risk controls, escalating costs, or unclear business value, and industry secondary sources report that **74% of companies struggle to scale AI value** and only **roughly 24% of GenAI projects achieve their expected ROI** ([reporting on Gartner findings, LinkedIn/secondary aggregation](https://www.linkedin.com/posts/bold-generic-solutions_genai-activity-7472350702888140800-M5K5); note: verify against a primary Gartner press release before citing the 74%/24% figures in a board-level document, as these appear in secondary aggregation rather than a located primary Gartner URL in this research pass).

### 8.5 Practical ROI methodology recommendations

Drawing on the above, a defensible AI ROI methodology should:

1. **Separate gross benefit from incremental (counterfactual) benefit** — measure against a "no-AI" baseline or control group, not against pre-AI absolute performance, since other factors (headcount, process changes) confound naive before/after comparisons.
2. **Use McKinsey's dual-lens approach** — track both **use-case-level cost/revenue benefit** (where evidence is strongest — software engineering, manufacturing, IT report 10–20%+ cost reductions) and **enterprise-level EBIT attribution** (where evidence remains thin — only ~39% report any effect) ([McKinsey, State of AI in 2025](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai)).
3. **Set a realistic time-to-value window** — McKinsey and BCG data both suggest 12+ months from pilot to workflow redesign to measurable EBIT impact; premature ROI claims at the pilot stage should be treated as directional, not final.
4. **Track adoption stage, not just usage** — usage (logins, queries) is a leading indicator; workflow redesign and reinvestment of saved time are the actual value-creation events, per BCG's adoption-stage findings.
5. **Tie cost-per-outcome (Section 2) directly into the ROI numerator** — the "financial benefit" side of the ROI formula should be built bottom-up from cost-per-outcome improvements multiplied by outcome volume, cross-checked against top-down EBIT attribution.

---

## 9. Enterprise AI Portfolio Management

Large regulated enterprises (banks, telcos, retailers) converge on a small number of **AI Center of Excellence (CoE)** operating models, typically progressing through a maturity curve ([Stratenity, "Organizational Design for AI Readiness — Banking"](https://www.stratenity.com/pages/engagements/Organizational-Design-for-AI-Readiness-Banking.html)):

- **Centralized CoE** — a single hub (under CDO/CTO) owning standards, platforms, and guardrails; best for early maturity and high regulatory pressure (typical starting point for banks).
- **Federated model** — the CoE sets policy and shared services (model registry, MLOps platform, evaluation harness) while embedded AI squads sit inside business units; balances central control with delivery speed. This is the most common target-state model cited for mid-maturity, multi-line-of-business organizations.
- **Fully distributed** — AI competency embedded in every function with lightweight central oversight; reserved for high-maturity organizations with strong internal standards culture.

A representative **governance and stage-gate roadmap** ([Stratenity, "Organizational Design for AI Readiness"](https://www.stratenity.com/pages/engagements/Organizational-Design-for-AI-Readiness-Banking.html)):

| Horizon | Governance state | Key artifacts | Decision gates |
|---|---|---|---|
| Months 0–3 (Reactive → Proactive) | AI CoE + Governance Board stood up; initial policy set; model inventory; risk taxonomy | AI Ethics Charter, RACI, Model Registry v1, Data Access Policy | Use-case intake gate; privacy & model-risk checks before any pilot begins |
| Months 4–9 (Integrated) | Federated squads; standardized MLOps; monitoring & audit logs; explainability norms | Playbooks, Monitoring SLAs, Prompt/Model Logging, Vendor Risk Standard | Go/No-Go at pilot gates; board-visible risk dashboards |
| Months 10–12+ (Embedded) | Enterprise operating model; clear roles; explainability and audit trails; benefits register | Benefits Register, Next-year Investment Plan, Capability Roadmap | Scale/stop decisions driven by value and risk dashboards |

**Use-case intake and stage gating** typically include: (1) an intake form capturing business sponsor, target KPI, data sensitivity, and estimated volume; (2) a **privacy/model-risk pre-check** before any pilot spend is approved; (3) a **pilot (Crawl) gate** bounding cost and timeline per the FinOps Crawl-Walk-Run model (Section 1.1); (4) a **scale (Walk→Run) gate** requiring demonstrated unit economics (cost per outcome) and a completed risk/compliance review before production rollout; and (5) a **portfolio-level review cadence** (typically quarterly) that reallocates budget across use cases based on realized ROI versus the benefits register. This mirrors the FinOps Foundation's own Crawl-Walk-Run cost-governance stages mapped onto formal go/no-go decision points ([FinOps Foundation, "FinOps for AI Overview"](https://www.finops.org/wg/finops-for-ai-overview/)).

---

## 10. Domain Overlays

| Domain | Primary frameworks/regulators | Cost/FinOps implication |
|---|---|---|
| **Banking** | SR 11-7 (in transition — see Section 6.1); updated OCC/Fed/FDIC MRM guidance (OCC Bulletin 2026-13, effective April 2026, excludes GenAI/agentic AI from scope pending future guidance); OCC third-party risk management guidance for vendor/model validation ([OCC News Release 2026-29](https://www.occ.gov/news-issuances/news-releases/2026/nr-occ-2026-29.html)) | Independent validation and third-party vendor risk review add recurring cost per model; expect new GenAI-specific MRM cost lines once the forthcoming interagency RFI produces guidance. |
| **Retail** | PCI DSS (payment card data protection) for any AI system touching transaction data; marketing-attribution compliance (consumer privacy laws governing AI-driven personalization and attribution modeling) | AI systems processing cardholder data inherit PCI DSS scope, adding segmentation, encryption, and audit costs; attribution-model AI must budget for consent-management and data-minimization tooling. |
| **Oil & gas** | OT/IT safety boundaries — AI systems interfacing with operational technology (SCADA, industrial control systems) require safety-case documentation and segregation from IT networks | AI-driven predictive maintenance or optimization must budget for OT/IT security gateway infrastructure and safety validation, distinct from pure-IT AI cost models. |
| **Aerospace** | DO-178C (software assurance for airborne systems) provides relevant context for safety-critical software assurance rigor, though it is not an AI-specific standard | Any AI component touching flight-critical or safety-critical systems inherits DO-178C-level verification and documentation cost expectations, historically far higher per-line-of-code than typical enterprise software. |
| **Public sector** | FedRAMP (cloud authorization for federal systems); NIST SP 800-53 (security controls baseline); CMMC 2.0 / NIST SP 800-171 for defense-adjacent contractors handling CUI/FCI | Cloud-hosted AI tools used in federal systems — including AI embedded in productivity software — require FedRAMP authorization before deployment; AI agents accessing CUI/FCI are subject to full CMMC 2.0 and NIST 800-171 controls with no AI-specific exemption, and non-compliant certification carries False Claims Act exposure ([Kiteworks, "AI Compliance for Federal Contractors"](https://www.kiteworks.com/regulatory-compliance/ai-compliance-federal-contractors/)). |
| **Telecom** | CPNI (Customer Proprietary Network Information) rules governing use of call/usage data, relevant to AI systems built on subscriber data | AI systems trained on or accessing CPNI must maintain the same consent, access-control, and audit-logging rigor as any other CPNI-touching system, adding compliance review cost to telecom AI use cases (e.g., churn prediction, network optimization on subscriber data). |
| **Entertainment** | Content rights and IP licensing — AI systems that generate, summarize, or recommend content must respect underlying rights-holder licensing terms | Generative AI use cases touching licensed content require legal review of training-data provenance and output-rights clearance, a distinct cost line from technical AI development. |
| **Energy** | NERC CIP (Critical Infrastructure Protection) standards for the bulk electric system; FERC Order 3052 (2024) creates cybersecurity investment incentives tied to NERC CIP compliance, with AI security-monitoring systems eligible for incentive rate treatment | AI systems touching grid operations must meet NERC CIP cybersecurity and access-control requirements; FERC's incentive-rate treatment can partially offset AI security-monitoring investment costs for eligible utilities ([VeriProof Documentation, Energy & Utilities policy](https://docs.veriproof.app/policy/industry-enums/08-vertical-energy-utilities/)). |

---

## Summary Framework for the FinOps Practitioner

A large enterprise building a company-wide AI FinOps practice should:

1. **Adopt the FinOps Scope model** — treat AI as a distinct Scope with its own personas, capabilities, and thresholds nested inside the existing FinOps Framework, not a bolt-on ([FinOps Foundation, 2025 Framework](https://www.finops.org/insights/2025-finops-framework/)).
2. **Instrument at the token level first, then graduate to outcome-based unit economics** (cost per resolved conversation, cost per accepted suggestion, cost per workflow completion) as instrumentation matures ([FinOps Foundation, Unit Economics capability](https://www.finops.org/framework/capabilities/unit-economics/)).
3. **Benchmark pricing continuously** — model pricing and platform-specific rates (direct API vs. Bedrock vs. Vertex vs. Azure) diverge materially and change frequently; build pricing refresh into the FinOps Inform cycle.
4. **Sequence optimization levers by effort/impact** — prompt caching and batch inference deliver the largest, most provable savings (50–90%) with the least architectural risk; model cascading and distillation deliver comparable savings but require more engineering investment and quality validation.
5. **Fold governance cost explicitly into the AI TCO model** — evaluation, logging, audit, and human-in-the-loop review are recurring operating costs mandated by NIST AI RMF, EU AI Act, ISO 42001, and OWASP guidance, not one-time compliance projects.
6. **Gate portfolio investment on demonstrated unit economics, not usage** — use the Crawl-Walk-Run stage-gate model to ensure spend scales only once cost-per-outcome and risk clearance are both proven.

