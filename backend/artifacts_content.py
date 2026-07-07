"""
Single source of truth for all 21 FinOps AI artifacts.

Each artifact contains:
- id, number, title
- role_context: what a Principal AI Solutions Consultant does with this artifact
- purpose, when_to_use, inputs_needed (from the original templates)
- learning: reference-manual-depth teaching content for beginners
    - concepts: [{term, definition, why_it_matters}]
    - how_to_use: ordered step-by-step guidance
    - worked_example: narrative walk-through with realistic numbers
    - pitfalls: common failure modes and how to avoid them
    - decision_tree: when-to-branch guidance
    - domain_overlays: {generic, banking, retail, energy, aerospace, public_sector, telecom, entertainment}
- fields: form fields for the app to render, each with {key, label, type, help, sample}
- tables: structured table definitions {key, label, columns:[{key,label,type,help}], rows_sample}
- deliverable_sections: how the DOCX is laid out
"""

from __future__ import annotations
from typing import Any


# =====================================================================
# Shared references used across artifacts
# =====================================================================

GLOSSARY = {
    "FinOps": "A discipline combining Finance, Engineering, and Business teams to manage variable cloud/AI spend with shared accountability. The FinOps Foundation defines three lifecycle phases: Inform (visibility), Optimize (efficiency), and Operate (governance/culture).",
    "Unit economics": "Cost expressed per unit of business value — e.g., cost per request, cost per successful outcome, cost per resolved conversation. This is the primary lens for AI FinOps because raw monthly spend hides efficiency changes as volume scales.",
    "Cost per successful outcome": "Total cost of producing an outcome the business accepts, divided by the count of accepted outcomes. If cost/request is $0.02 and 80% pass the quality gate, cost/successful outcome is $0.025.",
    "Cost boundary": "The explicit list of what is IN and OUT of the model. Prevents late surprises like 'we forgot vector DB storage' or 'this includes dev traffic.'",
    "Cost driver": "A measurable quantity whose change drives cost — input tokens, output tokens, retrieval calls, tool calls, eval runs, GB-months of vector storage.",
    "Prompt caching": "Vendor feature where repeated portions of a prompt (system prompt, few-shot examples) are cached at reduced cost. Typical discount: 50–90% off cached input tokens (OpenAI, Anthropic, Google as of 2025).",
    "Semantic caching": "Application-layer cache that returns previously generated responses when a new query is semantically similar. Different from prompt caching. Can reduce inference cost dramatically for repetitive traffic (support FAQs, common intents).",
    "Model cascading / routing": "Sending easier requests to smaller/cheaper models and reserving large models for hard requests. Common ratio: 70–90% of traffic to small models with quality gates catching escalations.",
    "RAG": "Retrieval-Augmented Generation. LLM answers grounded in retrieved documents. Cost drivers: embeddings, vector storage, retrieval queries, reranker calls, and the extra input tokens fed to the LLM.",
    "Top-k": "Number of retrieved chunks passed to the LLM. Higher top-k = better recall but more input tokens. A common tuning target.",
    "Reranker": "A second-stage model that reorders retrieved chunks by relevance. Adds cost per query but often lets you reduce top-k downstream.",
    "Guardrails": "Safety/policy filters (input/output moderation, PII redaction, hallucination checks). Each guardrail is a mini-model call — they add cost.",
    "Human-in-the-loop (HITL)": "Human review of AI output. Costs = reviewer minutes × loaded labor rate. Often larger than compute cost for regulated workflows.",
    "Evaluation harness": "Automated pipeline that runs a suite of prompts against a model and scores outputs. Cost = eval_runs × prompts_per_run × tokens × unit_price. Can silently balloon.",
    "Chargeback / Showback": "Chargeback moves cost from platform to LOB budgets. Showback reports allocated cost without moving it. Choose showback first; move to chargeback when allocation is stable.",
    "Model risk management (SR 11-7 / MRM)": "Federal Reserve guidance on managing risk of any model used for material business decisions. In practice: independent validation, ongoing monitoring, documentation, and inventory. Applies to LLMs when they influence customer, credit, or compliance decisions.",
    "NIST AI RMF": "NIST AI Risk Management Framework 1.0 (2023). Four functions: Govern, Map, Measure, Manage. Widely used as the enterprise AI risk backbone.",
    "EU AI Act": "First horizontal AI regulation. Risk tiers (prohibited, high-risk, limited, minimal) and separate GPAI (general-purpose AI) obligations. Phased application through 2025–2027.",
    "ISO/IEC 42001": "Management-system standard for AI (2023). Provides a certifiable structure similar to ISO 27001 for infosec.",
    "OWASP LLM Top 10": "Community list of top LLM application risks (prompt injection, sensitive information disclosure, supply chain, etc.). Useful for red-team and control design.",
    "Counterfactual": "The estimate of what would have happened without AI. Required for incremental benefit calculation. Common approaches: matched controls, pre/post with baseline correction, holdout groups.",
    "NPV": "Net Present Value: sum of discounted future net cashflows minus initial investment. Positive = economically worthwhile at the chosen discount rate.",
    "Payback period": "Months until cumulative net cashflow turns positive. Complements NPV — leadership often anchors on payback.",
    "Confidence rating (H/M/L)": "Simple qualifier applied to every assumption. High = observed from pilot data; Medium = triangulated from analogous workloads; Low = expert guess. Drives sensitivity focus.",
    "Cost anomaly": "Observed cost that deviates from forecast by more than a threshold (e.g., ±15% at daily granularity). Requires playbook-driven triage.",
}


DOMAIN_OVERLAY_KEYS = [
    "generic",
    "banking",
    "retail",
    "energy_oil_gas",
    "aerospace",
    "public_sector",
    "telecom",
    "entertainment",
]


# =====================================================================
# Individual artifact content
# =====================================================================

def _artifact_1() -> dict[str, Any]:
    return {
        "id": "A01",
        "number": 1,
        "title": "Engagement Kickoff & Scope",
        "short_title": "Kickoff & Scope",
        "role_context": (
            "As the Principal AI Solutions Consultant you are the accountable owner of the engagement. "
            "This artifact is your covenant with the business, technology, finance, risk, and compliance partners. "
            "Signed scope prevents the two most expensive failure modes in enterprise AI work: silent scope creep "
            "and disputed acceptance criteria at the go/no-go review."
        ),
        "purpose": (
            "Create a shared, auditable agreement on what you will model, what you will not, what success means, "
            "and who approves decisions. Every downstream artifact in this pack inherits its boundaries from here."
        ),
        "when_to_use": (
            "Immediately at engagement start (Week 0–1). Re-open only when scope materially changes; then log the "
            "change in the Decision Log with a new revision number."
        ),
        "inputs_needed": [
            "One-paragraph description of the target AI workload (current or planned)",
            "High-level architecture (diagram or bullets)",
            "Expected usage volume range (low / expected / peak)",
            "Known constraints: data residency, model governance, third-party risk, procurement",
            "Named stakeholders and owners across business, product, engineering, finance, risk, compliance",
        ],
        "learning": {
            "concepts": [
                {
                    "term": "Cost boundary",
                    "definition": GLOSSARY["Cost boundary"],
                    "why_it_matters": (
                        "The single biggest source of forecast error in AI programs is undeclared scope. "
                        "State the boundary in one paragraph AND repeat it as a checklist so approvers "
                        "cannot claim later they were unaware."
                    ),
                },
                {
                    "term": "Decision log",
                    "definition": (
                        "A tabular, timestamped record of every material decision, who made it, and why. "
                        "Fields: Date, Decision, Owner, Rationale, Link/Artifact."
                    ),
                    "why_it_matters": (
                        "Auditors, model-risk teams, and second-line reviewers will ask 'why did you choose X?' "
                        "months later. The decision log answers that in seconds."
                    ),
                },
                {
                    "term": "RACI",
                    "definition": "Responsible (does the work), Accountable (single point of ownership), Consulted (two-way input), Informed (one-way notification).",
                    "why_it_matters": (
                        "Ambiguous ownership on quality gates, cost forecasts, and chargeback is the second most "
                        "common source of program drift. Assign a single Accountable per activity."
                    ),
                },
            ],
            "how_to_use": [
                "Step 1: Interview the business owner for 30 minutes. Capture the process being changed, the KPI it moves, and the value at stake. Write it in one paragraph.",
                "Step 2: With the technical owner, walk through the current architecture and mark every component with IN, OUT, or DEFER.",
                "Step 3: Define four objectives (cost, performance, quality, adoption) and one governance objective. Each must have a measurable threshold and an owner.",
                "Step 4: Explicitly enumerate excluded costs (dev/test traffic, ingestion one-time costs, sunk platform overhead). Missing exclusions cause 'surprise' variance.",
                "Step 5: Choose the measurement approach. If any live pilot traffic exists, use it — self-reported estimates alone will not survive challenge from finance.",
                "Step 6: Publish target dates against the six-week cadence in the template. Slippage on Week 1 predicts slippage on Week 4.",
                "Step 7: Route for sign-off. Minimum sign-off set: business owner, technical owner, finance partner, risk representative.",
            ],
            "worked_example": (
                "Workload: 'Wealth-management client servicing assistant' — an internal-facing RAG assistant that helps "
                "financial advisors draft responses to client emails. In-scope: LLM inference, retrieval, vector DB, "
                "evaluation harness, HITL review. Out-of-scope: CRM integration engineering (billed separately), "
                "one-time ingestion of 3.2M documents, and executive dashboarding. Cost objective: forecast Year-1 "
                "monthly spend within ±10%. Quality objective: ≥92% advisor acceptance rate on sampled outputs. "
                "Adoption objective: 60% of eligible advisors using the assistant at least 3 times/week by month 6. "
                "Governance: SR 11-7 tier-2 model risk designation with quarterly revalidation."
            ),
            "pitfalls": [
                "Skipping the exclusions list — inclusions alone do not prevent scope creep.",
                "Assigning multiple Accountables. If two people are accountable, no one is.",
                "Vague success metrics ('improve customer experience') that cannot be measured or tied to cost.",
                "Waiting to define governance until pilot ends. Model risk teams often gate scaling; loop them in Week 1.",
                "Treating volume as a single point estimate. Always state low/expected/peak.",
            ],
            "decision_tree": [
                "If the workload touches customer-facing decisions → escalate to SR 11-7 / MRM tier assessment before Week 2.",
                "If personal or health data is involved → engage privacy office before defining measurement fields.",
                "If a vendor model is used and negotiation is open → attach the pricing effective date as an assumption and set a re-validation trigger when contracts refresh.",
            ],
            "domain_overlays": {
                "generic": "Focus on business owner, technical owner, finance partner, and one governance representative.",
                "banking": "Add second-line risk (independent model validation), compliance officer, third-party risk manager, and data-use committee approval. Reference SR 11-7 tiering explicitly and align to the firm's MRM policy for validation cadence.",
                "retail": "Add merchandising or marketing owner (revenue attribution), PCI compliance representative if payment data touched, and vendor management for any customer-data enrichment vendors.",
                "energy_oil_gas": "Add OT/IT boundary representative (never let AI systems touch SCADA without explicit safety case), HSE (health/safety/environment) approver, and reliability engineering lead. Document isolation from safety-instrumented systems.",
                "aerospace": "Add safety engineering, cyber (AS9100/DO-326A context), export control (ITAR/EAR) representative. Even if AI is not in the flight path, export classification affects data movement.",
                "public_sector": "Add authorization official (ATO owner), privacy officer, records management, procurement (FAR/DFARS), and FedRAMP/StateRAMP boundary owner if cloud-hosted.",
                "telecom": "Add CPNI custodian, network operations lead, and vendor management. Explicitly document subscriber-data flows.",
                "entertainment": "Add IP/rights holder, talent-guild compliance where relevant, and content-safety reviewer. Log the training-data provenance question explicitly.",
            },
        },
        "fields": [
            {"key": "use_case_name", "label": "Use case name", "type": "text", "help": "Short business-friendly name."},
            {"key": "lob", "label": "Line of business", "type": "text"},
            {"key": "domain", "label": "Domain overlay", "type": "select", "options": DOMAIN_OVERLAY_KEYS, "default": "generic"},
            {"key": "business_owner", "label": "Business owner", "type": "text"},
            {"key": "product_owner", "label": "Product owner", "type": "text"},
            {"key": "technical_owner", "label": "Technical owner", "type": "text"},
            {"key": "finance_partner", "label": "Finance partner", "type": "text"},
            {"key": "risk_partner", "label": "Risk/compliance partner", "type": "text"},
            {"key": "workload_paragraph", "label": "Workload one-paragraph description", "type": "textarea"},
            {"key": "in_scope", "label": "In-scope components (checklist)", "type": "multiselect", "options": [
                "Frontend/API", "Orchestrator/agent framework", "Model(s) / endpoints",
                "RAG pipeline (ingestion + retrieval)", "Vector DB", "Evaluation harness",
                "Observability/telemetry", "Human-in-the-loop workflow"
            ]},
            {"key": "out_of_scope", "label": "Out-of-scope components", "type": "textarea"},
            {"key": "environments", "label": "Environments", "type": "multiselect", "options": ["Dev", "Test", "Prod"]},
            {"key": "regions_accounts", "label": "Regions / cloud accounts", "type": "text"},
            {"key": "data_classification", "label": "Data classification constraints", "type": "textarea"},
            {"key": "cost_objective", "label": "Cost objective", "type": "text"},
            {"key": "performance_objective", "label": "Performance objective (latency/SLA)", "type": "text"},
            {"key": "quality_objective", "label": "Quality objective", "type": "text"},
            {"key": "adoption_objective", "label": "Adoption objective", "type": "text"},
            {"key": "governance_objective", "label": "Governance objective", "type": "text"},
            {"key": "boundary_statement", "label": "Cost boundary statement (one paragraph)", "type": "textarea"},
            {"key": "measurement_approach", "label": "Measurement approach", "type": "textarea"},
            {"key": "target_dates", "label": "Target dates by phase", "type": "textarea"},
        ],
        "tables": [
            {
                "key": "decision_log",
                "label": "Decision log",
                "columns": [
                    {"key": "date", "label": "Date"},
                    {"key": "decision", "label": "Decision"},
                    {"key": "owner", "label": "Owner"},
                    {"key": "rationale", "label": "Rationale"},
                    {"key": "link", "label": "Link/Artifact"},
                ],
            }
        ],
    }


def _artifact_2() -> dict[str, Any]:
    return {
        "id": "A02",
        "number": 2,
        "title": "AI Workload Decomposition & Architecture Notes",
        "short_title": "Workload Decomposition",
        "role_context": (
            "Principal consultants translate architecture into finance. This artifact is where a fuzzy 'AI assistant' "
            "becomes a set of measurable steps that finance can forecast and engineers can optimize. If you cannot "
            "reduce the workload to a request path with cost drivers, you cannot model it."
        ),
        "purpose": "Turn architecture into measurable cost-impacting steps.",
        "when_to_use": "Week 1–2 of the engagement, before pricing tables or cost modeling begin.",
        "inputs_needed": [
            "Architecture diagram or component list from Artifact 1",
            "One or more representative user journeys",
            "Access to a solution architect for a 60–90 minute working session",
        ],
        "learning": {
            "concepts": [
                {
                    "term": "Request path",
                    "definition": "The end-to-end sequence of calls triggered by one user interaction, from entry point through model calls, retrieval, tool use, post-processing, and human handoff.",
                    "why_it_matters": "Every cost driver lives on the request path. If you cannot list the steps, you cannot allocate cost or optimize.",
                },
                {
                    "term": "Workload taxonomy",
                    "definition": "The classification of requests by their cost/quality profile (e.g., 'short factual', 'long analytical', 'RAG-heavy', 'agentic multi-step').",
                    "why_it_matters": "Averaging across a mixed workload hides expensive tails. Classify first, then model per class.",
                },
                {
                    "term": "Measurement signal",
                    "definition": "The concrete log field, metric, or billing line that lets you count how often a step happens in production.",
                    "why_it_matters": "A cost driver without a signal is speculation. Every driver in Artifact 4 must map back to a signal listed here.",
                },
            ],
            "how_to_use": [
                "Run a whiteboarding session with the technical owner and one senior engineer. 90 minutes is enough for one journey.",
                "Draw the happy path first. Then add branches for retries, escalations, and cache hits.",
                "For each step, capture: name, trigger, service/model invoked, key cost driver, and the log or metric that will measure it.",
                "Repeat per user journey. Two or three journeys typically cover 80% of production traffic.",
                "Publish the workload taxonomy. Every downstream artifact refers to the request types you name here.",
            ],
            "worked_example": (
                "Journey: 'Advisor asks the assistant to draft a client email response.' Steps: (1) API entry, "
                "(2) intent classifier — small model, ~200 tokens in/50 out, (3) retrieval — 4 vector queries at "
                "top-k=8, (4) reranker on 32 candidates, (5) main model — 2,500 tokens in / 400 tokens out, "
                "(6) safety filter (moderation call), (7) HITL preview surface (no cost), (8) evaluation harness "
                "samples 5% of traffic for offline scoring. Signals: request_id in APM, prompt_tokens/completion_tokens "
                "in the inference proxy, top_k and retrieved_doc_count in RAG logs, eval_suite tag in the eval bus."
            ),
            "pitfalls": [
                "Drawing only the happy path. Retries and reranker escalations often drive 20–40% of cost.",
                "Confusing 'agent steps' with 'model calls'. One agent step can be many model calls with tool interleavings.",
                "Skipping evaluation and guardrail calls — they are quietly the third or fourth largest line item.",
                "Not identifying the correlation key (usually request_id) that lets you join across services.",
            ],
            "decision_tree": [
                "If any step calls out to a vendor API you do not proxy → add a proxy or gateway before pilot to ensure you can measure and cap spend.",
                "If any step is 'user-provided free text with no length cap' → assume worst-case tokens for forecast and add an output length cap as a lever.",
            ],
            "domain_overlays": {
                "generic": "Model 2–3 journeys covering the top 80% of traffic.",
                "banking": "Add explicit fair-lending, adverse-action, and record-retention steps for any customer-decision-adjacent workflow. Note where the decision-of-record is created.",
                "retail": "Add cart/checkout impact steps for revenue-adjacent journeys.",
                "energy_oil_gas": "Add an explicit 'safety-relevant?' branch that routes to human confirmation.",
                "aerospace": "Add configuration-management step naming the model version and prompt version that produced any output persisted to a controlled system.",
                "public_sector": "Add an audit-log persistence step (immutable) and mark every step touching PII with the applicable authority-to-operate boundary.",
                "telecom": "Add CPNI classification step at input; log purpose-of-use.",
                "entertainment": "Add rights-check step for any generative output that could substitute for licensed content.",
            },
        },
        "fields": [
            {"key": "architecture_overview", "label": "High-level architecture (paste diagram description or bullets)", "type": "textarea"},
            {"key": "entry_points", "label": "Entry points", "type": "textarea"},
            {"key": "orchestration_steps", "label": "Orchestration / agent steps", "type": "textarea"},
            {"key": "model_calls", "label": "Model calls", "type": "textarea"},
            {"key": "retrieval_steps", "label": "Retrieval (RAG) steps", "type": "textarea"},
            {"key": "tool_calls", "label": "Tool calls / function calling", "type": "textarea"},
            {"key": "post_processing", "label": "Post-processing (summarization, formatting, safety filters)", "type": "textarea"},
            {"key": "human_approvals", "label": "Human approvals / escalations", "type": "textarea"},
            {"key": "logging_eval", "label": "Logging / telemetry / eval triggers", "type": "textarea"},
        ],
        "tables": [
            {
                "key": "request_path",
                "label": "Request path (per journey)",
                "columns": [
                    {"key": "step_id", "label": "Step ID"},
                    {"key": "step_name", "label": "Step name"},
                    {"key": "trigger", "label": "Trigger"},
                    {"key": "invoked", "label": "What gets called"},
                    {"key": "drivers", "label": "Key cost drivers"},
                    {"key": "signal", "label": "Measurement signal"},
                ],
            },
            {
                "key": "workload_taxonomy",
                "label": "Workload taxonomy",
                "columns": [
                    {"key": "request_type", "label": "Request type"},
                    {"key": "description", "label": "Description"},
                    {"key": "avg_prompt_len", "label": "Avg prompt length"},
                    {"key": "avg_output_len", "label": "Avg output length"},
                    {"key": "quality_gate", "label": "Quality gate"},
                ],
            },
        ],
    }


def _artifact_3() -> dict[str, Any]:
    return {
        "id": "A03",
        "number": 3,
        "title": "AI Cost Boundary, Assumptions & Pricing Table",
        "short_title": "Boundary & Pricing",
        "role_context": (
            "This artifact is the auditable spine of the cost model. Finance and second-line risk will read this before "
            "they read your forecast. Every unit price, every effective date, every assumption is a defense against "
            "'where did this number come from?' months later. As Principal Consultant you are personally accountable "
            "for the assumption confidence ratings."
        ),
        "purpose": "Make the cost model defensible by stating assumptions and unit prices in one place.",
        "when_to_use": "Week 2 — after decomposition, before forecast. Refresh every vendor pricing change.",
        "inputs_needed": [
            "Current vendor rate cards (with contract discounts if applicable)",
            "Effective dates of each contract",
            "Pilot traffic samples for token distributions (or benchmark analogs if no pilot yet)",
        ],
        "learning": {
            "concepts": [
                {
                    "term": "Effective-date discipline",
                    "definition": "Every unit price is tagged with the date it became effective and the source URL or contract ID.",
                    "why_it_matters": "Vendor prices change 2–4 times/year. Undated prices make the forecast un-reproducible.",
                },
                {
                    "term": "Assumption confidence rating",
                    "definition": "H = observed from pilot logs; M = triangulated from similar workloads; L = expert guess.",
                    "why_it_matters": "Sensitivity analysis focuses on Low-confidence assumptions. Without this rating, you sensitize the wrong variables.",
                },
                {
                    "term": "Cached input pricing",
                    "definition": "Vendors offer 50–90% discounts on repeated portions of prompts (system prompts, few-shot examples) when marked cacheable. Available on OpenAI, Anthropic, and Google.",
                    "why_it_matters": "For any workload with a large system prompt, enabling prompt caching is one of the highest-leverage optimizations and belongs on the pricing table from day one.",
                },
                {
                    "term": "Blended token price",
                    "definition": "The realized $/1K tokens after accounting for mix of input, cached input, and output. Always higher than input list price and lower than output list price.",
                    "why_it_matters": "Reporting a single 'model cost' number is misleading. Track input, cached, and output separately, then compute the blended rate.",
                },
            ],
            "how_to_use": [
                "Write the one-paragraph cost boundary. Read it out loud to the finance partner and ask them to sign it.",
                "Populate the unit pricing table with source, currency, effective date, and notes.",
                "For any assumption used across tabs (avg tokens/request, cache hit, retry rate), give a value AND a confidence rating AND a source.",
                "Document rounding conventions. Small differences accumulate over millions of requests.",
                "Set a calendar reminder to revalidate pricing every 90 days.",
            ],
            "worked_example": (
                "Vendor: Anthropic Claude Sonnet 4.5. Input $3/M tokens, cached input $0.30/M tokens, output $15/M tokens, "
                "effective 2025-09-29 per Anthropic pricing page. Vector DB: Pinecone Serverless p1 pod-hours at "
                "$0.096/hour with $0.25/M read units, effective 2025-Q3 contract. Embeddings: OpenAI text-embedding-3-large "
                "at $0.13/M tokens. Shared assumptions: avg input tokens/request 2,500 (H, pilot log 2025-11); avg output "
                "tokens/request 400 (H); cache hit rate 45% (M, target); retry rate 6% (M)."
            ),
            "pitfalls": [
                "Using list price when your contract has a discount. Or vice versa when the discount expires.",
                "Ignoring cached input pricing when your system prompt is 4,000+ tokens.",
                "Confusing $/1K tokens and $/1M tokens units. Modern APIs quote per million; older docs quote per thousand.",
                "Currency omission — for global programs, state USD/EUR/local and the FX assumption.",
            ],
            "decision_tree": [
                "If contract expires within the forecast horizon → model a 'contract-refresh' scenario in Artifact 9.",
                "If a vendor introduces a new tier (e.g., 'Batch API' at 50% off) → decide whether it is in the base case or in an optimization option (Artifact 10).",
            ],
            "domain_overlays": {
                "generic": "One boundary paragraph; one pricing table; one assumptions table.",
                "banking": "Add 'model inventory ID' column to the pricing table so entries tie back to the model risk inventory. Include validation-cost line items (independent-validation hours × loaded rate).",
                "retail": "Add seasonal-load assumption (peak/valley multiplier). Peak volume can be 5–15x average.",
                "energy_oil_gas": "Add data egress line item — remote sites often incur meaningful egress costs.",
                "aerospace": "Add classification-boundary column — some models cannot process ITAR-controlled inputs.",
                "public_sector": "Add FedRAMP-authorized-vendor column. If a component is not authorized, it is not in the boundary.",
                "telecom": "Add per-region regulatory constraint column (data localization).",
                "entertainment": "Add training-data-provenance column — some models are inadmissible for certain productions.",
            },
        },
        "fields": [
            {"key": "boundary_paragraph", "label": "Cost boundary statement (one paragraph)", "type": "textarea"},
            {"key": "rounding_conventions", "label": "Rounding and estimation conventions", "type": "textarea"},
            {"key": "currency", "label": "Reporting currency", "type": "text", "default": "USD"},
            {"key": "fx_assumption", "label": "FX assumption (if multi-currency)", "type": "text"},
        ],
        "tables": [
            {
                "key": "unit_pricing",
                "label": "Unit pricing sources",
                "columns": [
                    {"key": "component", "label": "Cost component"},
                    {"key": "unit", "label": "Unit"},
                    {"key": "source", "label": "Pricing source"},
                    {"key": "currency", "label": "Currency"},
                    {"key": "effective_date", "label": "Effective date"},
                    {"key": "notes", "label": "Notes"},
                ],
            },
            {
                "key": "assumptions",
                "label": "Shared assumptions",
                "columns": [
                    {"key": "assumption", "label": "Assumption"},
                    {"key": "value", "label": "Value"},
                    {"key": "basis", "label": "Basis"},
                    {"key": "confidence", "label": "Confidence (H/M/L)"},
                    {"key": "risk", "label": "Risk if wrong"},
                ],
            },
        ],
    }


def _artifact_4() -> dict[str, Any]:
    return {
        "id": "A04",
        "number": 4,
        "title": "AI Cost Driver Map",
        "short_title": "Cost Driver Map",
        "role_context": (
            "The Cost Driver Map is the workhorse of AI FinOps. Every dollar you forecast, allocate, or optimize flows "
            "through this table. Principal consultants who cannot produce this table on demand cannot lead an AI FinOps "
            "program."
        ),
        "purpose": "Provide the backbone table linking each cost driver to a precise definition, measurement signal, and unit cost.",
        "when_to_use": "Week 2, after Artifacts 2 and 3. Update whenever architecture or pricing changes.",
        "inputs_needed": [
            "Workload decomposition (Artifact 2)",
            "Pricing table (Artifact 3)",
            "Telemetry inventory (see Artifact 5)",
        ],
        "learning": {
            "concepts": [
                {
                    "term": "Driver definition precision",
                    "definition": "Every driver has an inclusion rule ('count only production request_ids', 'exclude health checks', 'exclude dev/test tenant').",
                    "why_it_matters": "Ambiguous drivers produce ambiguous forecasts. 'Requests' means nothing without an inclusion rule.",
                },
                {
                    "term": "Unit-cost derivation",
                    "definition": "Some drivers have direct unit prices (tokens); others are derived (cost per request = tokens × price + retrieval + tools).",
                    "why_it_matters": "Distinguishing direct vs derived unit costs prevents double-counting.",
                },
                {
                    "term": "Confidence H/M/L per driver",
                    "definition": "How well you know the value in production.",
                    "why_it_matters": "Drives sensitivity analysis and the pilot measurement plan.",
                },
            ],
            "how_to_use": [
                "For each cost driver identified in Artifact 2, add a row.",
                "Write the exact definition. If two engineers would interpret it differently, rewrite it.",
                "Specify where it is measured (log/metric/billing).",
                "Compute the unit cost from Artifact 3 pricing.",
                "Rate confidence H/M/L. Any Low-confidence driver becomes a priority for the pilot measurement plan.",
                "Publish inclusion rules in a companion paragraph.",
            ],
            "worked_example": (
                "Driver: Output tokens. Definition: sum of completion_tokens across all production request_ids in the "
                "inference proxy log, excluding request_ids tagged environment=dev. Signal: inference-proxy access log. "
                "Unit cost: $15/M tokens (Claude Sonnet 4.5 output). Confidence: H after pilot; M before pilot."
            ),
            "pitfalls": [
                "Copying token-price rows from vendor docs without stating the inclusion rule (dev vs prod).",
                "Treating 'cost per request' as a driver instead of a derived output.",
                "Leaving Low-confidence drivers un-flagged, so sensitivity analysis misses them.",
            ],
            "decision_tree": [
                "If a driver is Low confidence AND has large expected cost impact → prioritize it in Artifact 6 pilot measurement plan.",
                "If a driver cannot be measured (no signal) → either instrument it (Artifact 5) or accept modeling risk in Artifact 15.",
            ],
            "domain_overlays": {
                "generic": "Cover inference, retrieval, vector DB, embeddings, evaluation, guardrails, HITL, platform.",
                "banking": "Add validation-cost driver (SR 11-7 independent validation hours), and second-line review driver.",
                "retail": "Add peak-load surcharge driver (autoscale premium).",
                "energy_oil_gas": "Add remote-site egress driver.",
                "aerospace": "Add configuration-management driver (model version pinning cost).",
                "public_sector": "Add ATO-maintenance driver (annual assessment cost).",
                "telecom": "Add data-localization driver (multi-region duplicate infra).",
                "entertainment": "Add rights-verification driver.",
            },
        },
        "fields": [
            {"key": "inclusion_rules", "label": "Inclusion rules (paragraph)", "type": "textarea"},
        ],
        "tables": [
            {
                "key": "driver_map",
                "label": "Cost driver map",
                "columns": [
                    {"key": "driver", "label": "Cost driver"},
                    {"key": "definition", "label": "Definition (exact)"},
                    {"key": "signal", "label": "Where measured"},
                    {"key": "computed", "label": "How computed"},
                    {"key": "unit", "label": "Unit"},
                    {"key": "unit_cost", "label": "Unit cost ($/unit)"},
                    {"key": "default", "label": "Default"},
                    {"key": "confidence", "label": "Confidence"},
                ],
            }
        ],
    }


def _artifact_5() -> dict[str, Any]:
    return {
        "id": "A05",
        "number": 5,
        "title": "Metering & Instrumentation Requirements",
        "short_title": "Metering & Instrumentation",
        "role_context": (
            "You cannot manage what you cannot measure. This artifact is your contract with platform engineering to "
            "produce the telemetry that makes every downstream artifact defensible."
        ),
        "purpose": "Ensure you can actually measure the cost drivers you modeled.",
        "when_to_use": "Week 2–3, before the pilot begins. Any driver without a measurement plan is a modeling risk.",
        "inputs_needed": [
            "Driver map (Artifact 4)",
            "Access to platform engineering for log-field decisions",
            "Privacy office guidance on redaction",
        ],
        "learning": {
            "concepts": [
                {
                    "term": "Correlation key",
                    "definition": "A single ID (usually request_id) propagated across the frontend, orchestrator, retriever, model proxy, and eval bus.",
                    "why_it_matters": "Without a correlation key you cannot compute per-request cost, per-outcome cost, or attribute retries.",
                },
                {
                    "term": "Sampling strategy",
                    "definition": "Which fields are logged for every request vs sampled at a fraction of traffic.",
                    "why_it_matters": "Token counts must be always-on. High-cost eval payloads can be sampled. Getting this wrong wastes storage or blinds you.",
                },
                {
                    "term": "Redaction",
                    "definition": "Removing PII/PHI/PCI/CPNI before logs are persisted.",
                    "why_it_matters": "Logs that contain sensitive data are a compliance failure. Redaction must be designed before instrumentation begins.",
                },
            ],
            "how_to_use": [
                "For each system component, list the data required, the exact log field names, granularity, and sample method.",
                "Choose one correlation key. Document how it is propagated across services (header name, trace ID scheme).",
                "State retention and redaction rules.",
                "Publish a validation plan — compare telemetry to vendor usage dashboards and billing exports.",
            ],
            "worked_example": (
                "Correlation key: request_id (UUIDv4) set at the API edge, propagated via header X-Request-ID, included "
                "in every downstream log line. Redaction: OpenAI /chat/completions payloads redacted via a proxy that "
                "hashes user input tokens; token counts, model_id, and metadata are preserved. Retention: 90 days hot, "
                "13 months cold. Validation: monthly reconcile inference-proxy token counts to vendor usage dashboard, "
                "acceptance ±3%."
            ),
            "pitfalls": [
                "No correlation key → impossible to compute unit economics.",
                "Full-payload logging without redaction → compliance failure.",
                "Sampling token counts → blind spots exactly when volume spikes.",
                "No reconciliation to vendor usage → forecast drift invisible until finance sees the invoice.",
            ],
            "decision_tree": [
                "If any request contains regulated data → design redaction before instrumentation.",
                "If vendor usage dashboards are available → build automated reconciliation from day one.",
            ],
            "domain_overlays": {
                "generic": "Cover inference proxy, orchestrator, retriever, vector DB, eval harness, HITL.",
                "banking": "Add immutable audit log to a WORM store for any customer-decision-adjacent request.",
                "retail": "Add cart/session correlation to attribute revenue back to AI-touched sessions.",
                "energy_oil_gas": "Add safety-zone tagging so safety-relevant requests are separable in analysis.",
                "aerospace": "Add configuration-item ID (model version, prompt version) on every log line.",
                "public_sector": "Store audit logs in the ATO boundary; retention per records schedule.",
                "telecom": "Redact CPNI at ingest; log purpose-of-use.",
                "entertainment": "Log content-similarity scores where applicable to defend rights posture.",
            },
        },
        "fields": [
            {"key": "correlation_key", "label": "Correlation key and propagation rules", "type": "textarea"},
            {"key": "retention_window", "label": "Retention window", "type": "text"},
            {"key": "redaction_requirements", "label": "Privacy redaction requirements", "type": "textarea"},
        ],
        "tables": [
            {
                "key": "telemetry_checklist",
                "label": "Telemetry checklist by system",
                "columns": [
                    {"key": "component", "label": "System component"},
                    {"key": "data_required", "label": "Data required"},
                    {"key": "fields", "label": "Log fields / metrics"},
                    {"key": "granularity", "label": "Granularity"},
                    {"key": "sample_method", "label": "Sample method"},
                ],
            },
            {
                "key": "validation_plan",
                "label": "Instrumentation validation plan",
                "columns": [
                    {"key": "driver", "label": "Driver"},
                    {"key": "check", "label": "Validation check"},
                    {"key": "acceptance", "label": "Acceptance criterion"},
                ],
            },
        ],
    }


def _artifact_6() -> dict[str, Any]:
    return {
        "id": "A06",
        "number": 6,
        "title": "Pilot Measurement Plan (Sampling + Calibration)",
        "short_title": "Pilot Measurement Plan",
        "role_context": (
            "Pilots are where forecasts become defensible. Principal consultants design pilots that produce "
            "statistically usable calibration data — not just 'we tried it and users liked it.' Every distribution "
            "in the cost model traces to a pilot log."
        ),
        "purpose": "Calibrate averages and distributions so the forecast is credible.",
        "when_to_use": "Week 2–3, alongside instrumentation. Run the pilot Weeks 3–5.",
        "inputs_needed": [
            "Workload taxonomy from Artifact 2",
            "Telemetry ready to fire per Artifact 5",
            "A pilot traffic plan — limited users, sandbox, or shadow mode",
        ],
        "learning": {
            "concepts": [
                {"term": "Stratified sampling", "definition": "Sampling across defined strata (short/long, RAG-heavy/agentic) to prevent one stratum from dominating averages.", "why_it_matters": "Averages across a mixed workload lie."},
                {"term": "Calibration output", "definition": "Aggregated distributions (avg, p50, p90) exported per request type, used as inputs to Artifact 8.", "why_it_matters": "P90 tokens drive worst-case cost and latency."},
                {"term": "Acceptance criteria", "definition": "The threshold that determines whether the model is 'calibrated enough' to move to forecast.", "why_it_matters": "Without acceptance criteria, calibration is subjective."},
            ],
            "how_to_use": [
                "Set duration to at least 10 business days of representative traffic.",
                "Define strata and target proportions. Aim for statistically comparable samples in each.",
                "Extract per-request metrics per Artifact 5.",
                "Compute avg, p50, p90 per request type. Export as CSV/Parquet.",
                "Apply model-validation acceptance criteria before moving to Artifact 8.",
            ],
            "worked_example": (
                "Pilot period 2026-01-05 to 2026-01-16. Traffic: shadow mode on 15% of advisor traffic. Strata: "
                "short factual 40%, long analytical 35%, RAG-heavy 20%, agentic 5%. Metrics: input_tokens, output_tokens, "
                "tool_calls, retrieval_calls, retry_count, quality_gate_pass. Acceptance: forecast vs actual total ±12%, "
                "inference component ±10%, retrieval component ±15%."
            ),
            "pitfalls": [
                "Running the pilot on non-representative traffic (e.g., only during business hours in one region).",
                "Not tagging quality outcomes at request level → no cost-per-successful-outcome later.",
                "Failing to freeze prompt/model versions during the pilot → contaminated calibration.",
            ],
            "decision_tree": [
                "If real production traffic is not available → shadow mode against a canary. Estimate-only pilots do not survive challenge.",
                "If a stratum has too few samples → extend duration or over-sample it.",
            ],
            "domain_overlays": {
                "generic": "Cover the top 4 strata by traffic share.",
                "banking": "Include an adverse-outcome stratum (denials, disputes) — cost profile differs materially.",
                "retail": "Include peak-hour and holiday strata.",
                "energy_oil_gas": "Include field-condition strata (low bandwidth, offline-then-sync).",
                "aerospace": "Include configuration-baseline changes as a stratum.",
                "public_sector": "Include FOIA-adjacent request stratum if applicable.",
                "telecom": "Include high-tier-support stratum.",
                "entertainment": "Include high-visibility content stratum.",
            },
        },
        "fields": [
            {"key": "pilot_start", "label": "Pilot start date", "type": "date"},
            {"key": "pilot_end", "label": "Pilot end date", "type": "date"},
            {"key": "traffic_scope", "label": "Traffic scope", "type": "select", "options": ["Limited users", "Production-like sandbox", "Shadow mode + limited live"]},
            {"key": "regions_accounts", "label": "Regions / accounts", "type": "text"},
            {"key": "export_format", "label": "Calibration export format", "type": "text", "default": "Parquet + CSV summary"},
        ],
        "tables": [
            {
                "key": "sampling",
                "label": "Sampling and stratification",
                "columns": [
                    {"key": "stratum", "label": "Stratum"},
                    {"key": "definition", "label": "Definition"},
                    {"key": "target_share", "label": "Target % traffic"},
                    {"key": "why", "label": "Why it matters"},
                ],
            },
            {
                "key": "metrics",
                "label": "Metrics extracted per request",
                "columns": [
                    {"key": "metric", "label": "Metric"},
                    {"key": "definition", "label": "Definition"},
                    {"key": "granularity", "label": "Granularity"},
                    {"key": "output_format", "label": "Output format"},
                ],
            },
            {
                "key": "acceptance",
                "label": "Model validation acceptance criteria",
                "columns": [
                    {"key": "component", "label": "Component"},
                    {"key": "check", "label": "Forecast vs actual"},
                    {"key": "threshold", "label": "Threshold"},
                ],
            },
        ],
    }


def _artifact_7() -> dict[str, Any]:
    return {
        "id": "A07",
        "number": 7,
        "title": "AI Unit Economics Calculator",
        "short_title": "Unit Economics",
        "role_context": (
            "Unit economics is where AI FinOps stops being cost management and starts being value engineering. "
            "The Principal Consultant's signature deliverable is 'cost per successful outcome' — the number leadership "
            "actually cares about."
        ),
        "purpose": "Compute unit cost per request and per successful outcome by request type.",
        "when_to_use": "Week 3–4 after calibration.",
        "inputs_needed": ["Pricing (Artifact 3)", "Driver map (Artifact 4)", "Calibration data (Artifact 6)"],
        "learning": {
            "concepts": [
                {"term": "Cost per request", "definition": "Direct cost of one production request across all cost drivers.", "why_it_matters": "Baseline for optimization tracking."},
                {"term": "Cost per successful outcome", "definition": "Cost per request divided by the fraction that pass the quality gate.", "why_it_matters": "Realistic economics — failed requests still cost money."},
                {"term": "Model routing mix", "definition": "Share of requests going to small vs large model.", "why_it_matters": "Routing is the single highest-leverage cost lever."},
            ],
            "how_to_use": [
                "For each request type, populate inputs: routing mix, avg tokens in/out, retries, tool calls, retrieval calls, reranker rate, success rate.",
                "Compute cost per request (formula in worked example).",
                "Compute cost per successful outcome.",
                "Publish cost per 1K outcomes for readability.",
            ],
            "worked_example": (
                "Request type: 'short factual'. Routing: 85% small (Claude Haiku) / 15% large (Sonnet). Avg input tokens: "
                "1,200 (with 45% cached). Avg output tokens: 220. Retrieval: 2 calls. Reranker: 30% of traffic. Retry "
                "rate: 4%. Success rate: 92%. Cost calculation: "
                "small path = (1,200 × 0.55 × $0.80/M + 1,200 × 0.45 × $0.08/M + 220 × $4/M) = "
                "$0.000528 + $0.0000432 + $0.00088 ≈ $0.00145. Large path = "
                "(1,200 × 0.55 × $3/M + 1,200 × 0.45 × $0.30/M + 220 × $15/M) ≈ $0.00198 + $0.000162 + $0.0033 = $0.00544. "
                "Blended = 0.85 × $0.00145 + 0.15 × $0.00544 = $0.00205. Add retrieval $0.0004 + reranker $0.0002 × 0.30 = "
                "$0.00006 + retries factor × 1.04 = $0.00259 per request. Cost per successful outcome = $0.00259 / 0.92 = "
                "$0.00282."
            ),
            "pitfalls": [
                "Reporting only 'cost per request' without success rate.",
                "Forgetting to apply the retry multiplier.",
                "Averaging across request types instead of computing per type.",
            ],
            "decision_tree": [
                "If cost per successful outcome differs by >2x across types → address the worst type first.",
                "If retries drive >15% of cost → prioritize quality gate work (Artifact 16).",
            ],
            "domain_overlays": {
                "generic": "Compute per request type.",
                "banking": "Also compute cost per decision-of-record.",
                "retail": "Also compute cost per attributable purchase.",
                "energy_oil_gas": "Also compute cost per safe operation.",
                "aerospace": "Also compute cost per configuration-controlled artifact.",
                "public_sector": "Also compute cost per constituent served.",
                "telecom": "Also compute cost per resolved trouble ticket.",
                "entertainment": "Also compute cost per approved asset.",
            },
        },
        "fields": [],
        "tables": [
            {
                "key": "unit_inputs",
                "label": "Inputs by request type",
                "columns": [
                    {"key": "request_type", "label": "Request type"},
                    {"key": "routing_mix", "label": "Routing mix (small/large)"},
                    {"key": "avg_in", "label": "Avg tokens in"},
                    {"key": "cached_share", "label": "Cached share"},
                    {"key": "avg_out", "label": "Avg tokens out"},
                    {"key": "retrieval_calls", "label": "Retrieval calls"},
                    {"key": "reranker_rate", "label": "Reranker rate"},
                    {"key": "tool_calls", "label": "Tool calls"},
                    {"key": "retry_rate", "label": "Retry rate"},
                    {"key": "success_rate", "label": "Success rate"},
                ],
            },
            {
                "key": "unit_outputs",
                "label": "Outputs",
                "columns": [
                    {"key": "request_type", "label": "Request type"},
                    {"key": "cost_per_request", "label": "Cost per request"},
                    {"key": "cost_per_success", "label": "Cost per successful outcome"},
                    {"key": "cost_per_1k", "label": "Cost per 1K outcomes"},
                ],
            },
        ],
    }


def _artifact_8() -> dict[str, Any]:
    return {
        "id": "A08",
        "number": 8,
        "title": "AI Cost Forecast Model (Monthly, by Component)",
        "short_title": "Cost Forecast",
        "role_context": (
            "This is the number finance and executives will remember. Everything upstream feeds it. Everything "
            "downstream is judged against it."
        ),
        "purpose": "Produce a monthly forecast finance can use and auditors can trace.",
        "when_to_use": "Week 4, immediately after unit economics.",
        "inputs_needed": [
            "Assumptions (Artifact 3)", "Unit economics (Artifact 7)", "Volume forecast from business",
            "Calibration data (Artifact 6)",
        ],
        "learning": {
            "concepts": [
                {"term": "Volume forecast", "definition": "Requests/day by request type, seasonality-adjusted.", "why_it_matters": "Volume is the primary swing variable in AI cost."},
                {"term": "Component breakout", "definition": "Cost separated by inference, retrieval, vector DB, embeddings, eval, guardrails, HITL, platform.", "why_it_matters": "Component visibility lets you target optimizations."},
                {"term": "Inclusion rules", "definition": "Explicit rules for pilot traffic exclusion, dev/test exclusion, one-time vs run-rate.", "why_it_matters": "Prevents surprise reclassification during audit."},
            ],
            "how_to_use": [
                "Build 6 tabs: Assumptions, Unit_Economics, Volume_Forecast, Cost_Forecast, Variance_And_Validation, Scenarios.",
                "Populate volume by month by request type.",
                "Compute cost by component by month.",
                "State inclusion rules on the forecast face.",
                "Run reconciliation: month-1 forecast vs actual bill.",
            ],
            "worked_example": (
                "Month 2026-08. Requests: 380k short factual, 120k long analytical, 50k RAG-heavy, 10k agentic. "
                "Cost: inference $1,180, retrieval $220, vector DB $190, embeddings (re-embed 5%) $60, eval $140, "
                "guardrails $95, HITL $2,300, platform allocation $410. Total $4,595."
            ),
            "pitfalls": [
                "Reporting a single total without component breakout.",
                "Not stating inclusion rules on the forecast face.",
                "Modeling forever-linear volume growth. Real adoption follows an S-curve.",
            ],
            "decision_tree": [
                "If HITL cost > 40% of total → optimizing HITL sampling/review time may dominate all model-side optimization.",
                "If one component is >60% → focus optimization there in Artifact 10.",
            ],
            "domain_overlays": {
                "generic": "Standard tabs.",
                "banking": "Add validation and second-line review as separate components.",
                "retail": "Add peak-season overlay tab.",
                "energy_oil_gas": "Add remote-site egress line.",
                "aerospace": "Add configuration-management overhead line.",
                "public_sector": "Add ATO-maintenance and audit-support lines.",
                "telecom": "Add multi-region infrastructure duplication line.",
                "entertainment": "Add rights-verification cost line.",
            },
        },
        "fields": [
            {"key": "inclusion_rules_forecast", "label": "Inclusion rules on forecast face", "type": "textarea"},
        ],
        "tables": [
            {
                "key": "volume_forecast",
                "label": "Volume forecast",
                "columns": [
                    {"key": "month", "label": "Month"},
                    {"key": "request_type", "label": "Request type"},
                    {"key": "req_per_day", "label": "Requests/day"},
                    {"key": "op_days", "label": "Operating days"},
                    {"key": "total_req", "label": "Total requests"},
                    {"key": "success_rate", "label": "Success rate"},
                    {"key": "cache_hit", "label": "Avg cache hit"},
                ],
            },
            {
                "key": "cost_forecast",
                "label": "Cost forecast",
                "columns": [
                    {"key": "month", "label": "Month"},
                    {"key": "component", "label": "Component"},
                    {"key": "request_type", "label": "Request type"},
                    {"key": "quantity", "label": "Quantity driver"},
                    {"key": "unit_cost", "label": "Unit cost"},
                    {"key": "total_cost", "label": "Total cost"},
                ],
            },
        ],
    }


def _artifact_9() -> dict[str, Any]:
    return {
        "id": "A09",
        "number": 9,
        "title": "Scenario Planning & Sensitivity",
        "short_title": "Scenarios & Sensitivity",
        "role_context": (
            "One point estimate is a target for attack. Ranges let you defend the forecast and pre-negotiate cost "
            "guardrails. Principal Consultants ship a range, not a number."
        ),
        "purpose": "Translate uncertainty into decision options.",
        "when_to_use": "Week 5, immediately after the base forecast.",
        "inputs_needed": ["Base forecast (Artifact 8)", "Assumption confidence ratings (Artifact 3)"],
        "learning": {
            "concepts": [
                {"term": "Scenario", "definition": "A named, internally consistent set of assumption values (downside/base/upside).", "why_it_matters": "Communicates the shape of risk, not just its magnitude."},
                {"term": "Tornado diagram", "definition": "Ranked bar chart showing NPV/cost sensitivity to each variable holding others constant.", "why_it_matters": "Focuses management attention on the 2–3 variables that actually matter."},
                {"term": "Two-variable table", "definition": "Grid showing cost as a function of two key drivers.", "why_it_matters": "Useful for capacity planning and negotiation."},
            ],
            "how_to_use": [
                "Define scenarios by varying a coherent set of drivers together.",
                "Run tornado analysis on 6–8 variables.",
                "Produce three exec-ready outputs: monthly cost range, NPV range, top-3 cost risk statement.",
            ],
            "worked_example": (
                "Downside: -20% volume, +30% output tokens, cache hit falls to 25%. Base: as forecast. Upside: +40% "
                "volume, -10% output tokens (prompt work), cache hit rises to 65%. Tornado ranks output tokens, cache hit, "
                "and routing share as top-3 drivers."
            ),
            "pitfalls": [
                "Varying only one lever at a time — misses coherent stress scenarios.",
                "Producing dozens of scenarios that execs cannot process. Three is enough.",
                "Not linking scenarios to Artifact 12 NPV outputs.",
            ],
            "decision_tree": [
                "If downside NPV negative but base positive → require optimization commitments before scaling.",
                "If tornado top variable is volume → engage business owner on adoption plan explicitly.",
            ],
            "domain_overlays": {
                "generic": "Three scenarios.",
                "banking": "Add regulatory-tightening scenario (increased validation/HITL cost).",
                "retail": "Add peak-season stress.",
                "energy_oil_gas": "Add extended-outage stress.",
                "aerospace": "Add certification-delay scenario.",
                "public_sector": "Add continuing-resolution / budget-flat scenario.",
                "telecom": "Add spectrum-auction outcome scenario for adjacent workloads.",
                "entertainment": "Add rights-holder-refusal scenario.",
            },
        },
        "fields": [],
        "tables": [
            {
                "key": "scenarios",
                "label": "Scenarios",
                "columns": [
                    {"key": "scenario", "label": "Scenario"},
                    {"key": "volume", "label": "Volume"},
                    {"key": "avg_tokens", "label": "Avg tokens"},
                    {"key": "routing_mix", "label": "Routing mix"},
                    {"key": "top_k", "label": "RAG top-k"},
                    {"key": "cache_hit", "label": "Cache hit"},
                    {"key": "retry_rate", "label": "Retry rate"},
                    {"key": "adoption", "label": "Adoption"},
                ],
            },
            {
                "key": "tornado",
                "label": "Sensitivity tornado",
                "columns": [
                    {"key": "variable", "label": "Variable"},
                    {"key": "low", "label": "Low"},
                    {"key": "base", "label": "Base"},
                    {"key": "high", "label": "High"},
                    {"key": "impact", "label": "Expected impact on NPV/cost"},
                ],
            },
        ],
    }


def _artifact_10() -> dict[str, Any]:
    return {
        "id": "A10",
        "number": 10,
        "title": "Optimization Options Catalog",
        "short_title": "Optimization Catalog",
        "role_context": (
            "Ideas are cheap; quantified options are the deliverable. Principal Consultants publish an options catalog "
            "with expected impact ranges and go/no-go criteria."
        ),
        "purpose": "Turn analysis into actionable options with quantified impacts.",
        "when_to_use": "Week 5–6.",
        "inputs_needed": ["Cost driver map (Artifact 4)", "Unit economics (Artifact 7)", "Scenarios (Artifact 9)"],
        "learning": {
            "concepts": [
                {"term": "Lever type", "definition": "Category of optimization (prompt efficiency, routing, caching, RAG tuning, guardrails, eval efficiency, HITL sampling, infra).", "why_it_matters": "Categorization helps portfolio-level planning."},
                {"term": "Impact triangle", "definition": "Every lever has (a) cost impact, (b) quality impact, (c) performance/latency impact.", "why_it_matters": "Silent quality regressions negate cost wins."},
                {"term": "Proof plan", "definition": "Small experiment to validate the option before scaling.", "why_it_matters": "Ideas that look great in spreadsheets can flop in production."},
            ],
            "how_to_use": [
                "Populate the option register with expected impact ranges (based on published benchmarks + your data).",
                "Attach a proof plan per option.",
                "Prioritize by expected impact × confidence ÷ effort.",
                "Track adopted options monthly.",
            ],
            "worked_example": (
                "OPT-002 Routing: send short factual to Claude Haiku. Effort M, Risk S. Expected cost impact -35%. "
                "Quality impact: pass rate falls from 94% to 92% (still above 90% gate). Proof plan: 2-week A/B on 20% "
                "of traffic. Go criterion: pass rate ≥ 90% AND cost/success down ≥ 25%."
            ),
            "pitfalls": [
                "Options with impact ranges but no proof plan — leadership will pick the top of the range.",
                "Ignoring quality/latency effects.",
                "Stacking multiple options and taking credit for the sum. Effects rarely fully compound.",
            ],
            "decision_tree": [
                "If quality gate margin is thin → prefer options that increase quality (better RAG, reranker) even if cost impact is smaller.",
                "If HITL dominates cost → prioritize HITL-sampling and confidence-threshold options.",
            ],
            "domain_overlays": {
                "generic": "Levers span prompt, routing, caching, RAG, guardrails, eval, HITL, infra.",
                "banking": "Add second-line-review sampling option; validation efficiency.",
                "retail": "Add peak-shift options (defer non-urgent to off-peak).",
                "energy_oil_gas": "Add edge-inference options.",
                "aerospace": "Add configuration-freeze options.",
                "public_sector": "Add ATO-scope reduction options (narrower boundary).",
                "telecom": "Add regional model consolidation options.",
                "entertainment": "Add rights-cached-response options.",
            },
        },
        "fields": [],
        "tables": [
            {
                "key": "option_register",
                "label": "Option register",
                "columns": [
                    {"key": "id", "label": "Option ID"},
                    {"key": "lever", "label": "Lever type"},
                    {"key": "description", "label": "Description"},
                    {"key": "drivers", "label": "Cost drivers affected"},
                    {"key": "effort", "label": "Effort (S/M/L)"},
                    {"key": "risk", "label": "Risk (S/M/L)"},
                    {"key": "metric", "label": "Metric to watch"},
                    {"key": "cost_impact", "label": "Expected impact (cost)"},
                    {"key": "quality_impact", "label": "Expected impact (quality/perf)"},
                ],
            },
            {
                "key": "proof_plans",
                "label": "Proof plans",
                "columns": [
                    {"key": "id", "label": "Option ID"},
                    {"key": "design", "label": "Pilot test design"},
                    {"key": "data", "label": "Data needed"},
                    {"key": "duration", "label": "Duration"},
                    {"key": "go_criteria", "label": "Go/No-go criteria"},
                ],
            },
        ],
    }


def _artifact_11() -> dict[str, Any]:
    return {
        "id": "A11",
        "number": 11,
        "title": "Benefits Value Calculator (Incremental & Attributable)",
        "short_title": "Benefits Calculator",
        "role_context": (
            "The number-one credibility killer of AI business cases is claiming benefits that would have happened "
            "anyway. Incremental attribution is the Principal Consultant's most-defended discipline."
        ),
        "purpose": "Ensure ROI does not assume benefits that would not happen otherwise.",
        "when_to_use": "Week 5–6.",
        "inputs_needed": ["Operations baseline metrics", "Adoption plan", "Attribution methodology agreed with finance"],
        "learning": {
            "concepts": [
                {"term": "Baseline", "definition": "Current-state operational metric before AI (e.g., avg handle time = 8 min).", "why_it_matters": "Without a baseline you cannot compute a delta."},
                {"term": "Counterfactual", "definition": "Estimate of what the metric would be without AI, accounting for other initiatives.", "why_it_matters": "Baselines drift. Counterfactual = baseline + expected drift."},
                {"term": "Attribution window", "definition": "Time between AI-touched event and observed outcome for which credit is claimed.", "why_it_matters": "Overly long windows over-attribute; too short misses lagged effects."},
                {"term": "Adoption curve", "definition": "The rate at which eligible users actually use the AI in production.", "why_it_matters": "Even good tools take 6–18 months to reach steady-state adoption."},
            ],
            "how_to_use": [
                "List benefit categories: labor efficiency, cycle time, deflection, revenue uplift, risk reduction.",
                "For each, define measurement, unit value, adoption %, and attribution logic.",
                "Explicitly write the counterfactual paragraph and the attribution window.",
                "Compute monthly benefit as eligible × adoption × increment × unit value.",
            ],
            "worked_example": (
                "Labor efficiency: advisor time saved per assisted email = 4 min. Loaded rate $110/hour = $1.83/min. "
                "Unit value = $7.32. Eligible = 60,000 emails/mo. Adoption ramps 10% → 65% over 9 months. "
                "Attribution: matched-cohort A/B during shadow, projected forward with adoption curve. Counterfactual: "
                "baseline handle-time already declining 2%/yr from process work; net delta after 2% detraction."
            ),
            "pitfalls": [
                "Gross benefits without counterfactual = fantasy.",
                "Adoption 100% at month 1 → unrealistic.",
                "Double-counting benefits (labor + cycle time when they measure the same thing).",
                "Claiming risk-reduction benefits without a modeled probability × impact basis.",
            ],
            "decision_tree": [
                "If benefits rely on measurement outside AI system → engage the operations analytics owner early.",
                "If revenue uplift is claimed → require finance sign-off on the attribution method.",
            ],
            "domain_overlays": {
                "generic": "Labor, cycle time, deflection, revenue, risk.",
                "banking": "Add fair-lending compliance / adverse-action quality benefits carefully — cost avoidance only, no revenue.",
                "retail": "Add conversion rate and average-order-value benefits.",
                "energy_oil_gas": "Add safety-incident-avoidance (probability × impact).",
                "aerospace": "Add certification-cycle time savings.",
                "public_sector": "Add constituent-satisfaction and processing-time.",
                "telecom": "Add churn reduction and first-call resolution.",
                "entertainment": "Add asset-turnaround time.",
            },
        },
        "fields": [
            {"key": "counterfactual_paragraph", "label": "Counterfactual (paragraph)", "type": "textarea"},
            {"key": "attribution_method", "label": "Attribution method", "type": "textarea"},
            {"key": "attribution_window", "label": "Attribution window", "type": "text"},
        ],
        "tables": [
            {
                "key": "benefit_categories",
                "label": "Benefit categories",
                "columns": [
                    {"key": "category", "label": "Category"},
                    {"key": "metric", "label": "Benefit metric"},
                    {"key": "measurement", "label": "How measured"},
                    {"key": "unit_value", "label": "Unit value"},
                    {"key": "adoption", "label": "Adoption (% eligible)"},
                ],
            },
            {
                "key": "benefit_forecast",
                "label": "Benefits forecast",
                "columns": [
                    {"key": "month", "label": "Month"},
                    {"key": "eligible", "label": "Eligible volume"},
                    {"key": "adoption", "label": "Adoption"},
                    {"key": "increment", "label": "Increment per unit"},
                    {"key": "incremental_units", "label": "Incremental units"},
                    {"key": "benefit", "label": "$ benefit"},
                ],
            },
        ],
    }


def _artifact_12() -> dict[str, Any]:
    return {
        "id": "A12",
        "number": 12,
        "title": "ROI / NPV Model",
        "short_title": "ROI / NPV",
        "role_context": (
            "Finance-ready NPV is the price of admission for scaling. Get the mechanics right: discount rate, horizon, "
            "one-time vs run-rate, tax treatment."
        ),
        "purpose": "Compute NPV, IRR (optional), payback, and show sensitivity transparently.",
        "when_to_use": "Week 6.",
        "inputs_needed": ["Cost forecast (Artifact 8)", "Benefits forecast (Artifact 11)", "Discount rate from finance"],
        "learning": {
            "concepts": [
                {"term": "Discount rate", "definition": "Enterprise WACC or the finance partner's specified hurdle rate.", "why_it_matters": "NPV signs flip at high discount rates."},
                {"term": "Payback period", "definition": "Months until cumulative net cashflow is positive.", "why_it_matters": "Executives anchor on payback more than NPV."},
                {"term": "Benefit-to-cost ratio", "definition": "NPV of benefits / NPV of costs.", "why_it_matters": "Ratio comparisons across the portfolio."},
            ],
            "how_to_use": [
                "Pull discount rate from finance policy.",
                "Set horizon (typically 3 years for AI programs).",
                "Populate monthly cashflows from Artifacts 8 and 11.",
                "Compute NPV, payback, and (optionally) IRR.",
                "Link tornado (Artifact 9) variables to NPV outputs.",
            ],
            "worked_example": (
                "Discount rate 10%. Horizon 36 months. Implementation $850k. Run-rate cost from Artifact 8 ramps "
                "$4.6k → $18k/mo. Benefits from Artifact 11 ramp $0 → $110k/mo. NPV = +$1.9M. Payback: month 14. "
                "BCR = 3.1x."
            ),
            "pitfalls": [
                "Netting one-time and run-rate cashflows without a line item for each.",
                "Assuming benefits begin month 1.",
                "Not showing NPV per scenario (Artifact 9).",
            ],
            "decision_tree": [
                "If downside NPV negative → require optimization commitments.",
                "If payback > 24 months → escalate to portfolio committee.",
            ],
            "domain_overlays": {
                "generic": "3-year horizon standard.",
                "banking": "Add regulatory-capital treatment note (rare, but sometimes material).",
                "retail": "Use fiscal calendar quarters (peak alignment).",
                "energy_oil_gas": "Add commodity-price sensitivity note.",
                "aerospace": "Use program-baseline reporting periods.",
                "public_sector": "Use fiscal year boundaries and appropriation cycles.",
                "telecom": "Include CAPEX/OPEX classification notes.",
                "entertainment": "Use production cycles.",
            },
        },
        "fields": [
            {"key": "discount_rate", "label": "Discount rate", "type": "number", "help": "e.g., 0.10 for 10%"},
            {"key": "horizon_months", "label": "Horizon (months)", "type": "number", "default": 36},
            {"key": "implementation_cost", "label": "Implementation cost (one-time)", "type": "number"},
            {"key": "benefits_start_month", "label": "Benefits start month", "type": "number"},
        ],
        "tables": [
            {
                "key": "cashflows",
                "label": "Monthly cashflows",
                "columns": [
                    {"key": "month", "label": "Month"},
                    {"key": "cost_run", "label": "Cost (run-rate)"},
                    {"key": "cost_onetime", "label": "One-time costs"},
                    {"key": "cost_total", "label": "Total cost"},
                    {"key": "benefits", "label": "Benefits"},
                    {"key": "net", "label": "Net cashflow"},
                ],
            },
            {
                "key": "outputs",
                "label": "Outputs",
                "columns": [
                    {"key": "scenario", "label": "Scenario"},
                    {"key": "npv", "label": "NPV"},
                    {"key": "payback", "label": "Payback (months)"},
                    {"key": "irr", "label": "IRR"},
                    {"key": "bcr", "label": "Benefit-to-cost ratio"},
                ],
            },
        ],
    }


def _artifact_13() -> dict[str, Any]:
    return {
        "id": "A13",
        "number": 13,
        "title": "Executive One-Pager (Business Case)",
        "short_title": "Exec One-Pager",
        "role_context": "The single most-read document in the pack. Every sentence must earn its place.",
        "purpose": "A concise decision document for leadership.",
        "when_to_use": "Week 6–7.",
        "inputs_needed": ["Everything upstream."],
        "learning": {
            "concepts": [
                {"term": "Recommendation-first", "definition": "State the ask in the first sentence.", "why_it_matters": "Executives skim; put the decision at the top."},
                {"term": "Range communication", "definition": "Always show base + range, not a single point.", "why_it_matters": "Ranges survive challenge; points do not."},
            ],
            "how_to_use": [
                "State the ask (approve pilot / scale / optimization).",
                "Two sentences on why now.",
                "Three-line solution overview.",
                "Cost outlook: base and range.",
                "Benefits: incremental only.",
                "ROI headline: NPV, payback, top-3 risks.",
                "Next step: date, owner, success criteria.",
            ],
            "worked_example": (
                "Recommendation: approve $2.4M Year-1 scale funding for the wealth-management client servicing assistant. "
                "Why now: advisor headcount pressure, competitor deployments launched Q4 2025. Solution: RAG + HITL over "
                "internal knowledge base. Cost: $220k/month base ($165k–$310k range). Benefits: $8.2M incremental Year-1 "
                "(matched-cohort attribution). NPV $12.9M (range $6M–$18M). Payback 9 months. Top risks: adoption slower "
                "than plan; regulatory validation cycle time. Next step: kick off scale phase 2026-Q3 with quality gate at 92%."
            ),
            "pitfalls": [
                "More than one page.",
                "No numeric ranges.",
                "No risks.",
                "No next step / owner.",
            ],
            "decision_tree": ["If unable to fit on one page → cut examples, keep decision-relevant numbers."],
            "domain_overlays": {k: "Same structure; adjust regulatory framing." for k in DOMAIN_OVERLAY_KEYS},
        },
        "fields": [
            {"key": "recommendation", "label": "Recommendation", "type": "textarea"},
            {"key": "budget_range", "label": "Budget range", "type": "text"},
            {"key": "timeline", "label": "Timeline", "type": "text"},
            {"key": "why_now", "label": "Why now", "type": "textarea"},
            {"key": "solution_summary", "label": "Solution summary", "type": "textarea"},
            {"key": "cost_outlook", "label": "Cost outlook", "type": "textarea"},
            {"key": "expected_benefits", "label": "Expected benefits", "type": "textarea"},
            {"key": "roi_headline", "label": "ROI headline", "type": "textarea"},
            {"key": "next_step", "label": "Next step", "type": "textarea"},
        ],
        "tables": [],
    }


def _artifact_14() -> dict[str, Any]:
    return {
        "id": "A14",
        "number": 14,
        "title": "Full Business Case Narrative",
        "short_title": "Business Case Narrative",
        "role_context": "The auditable long-form companion to the one-pager. Governance committees will read this.",
        "purpose": "Support governance committees with a thorough, auditable narrative.",
        "when_to_use": "Week 6–7.",
        "inputs_needed": ["All prior artifacts."],
        "learning": {
            "concepts": [
                {"term": "Auditable narrative", "definition": "Every quantitative claim is traceable back to an artifact number and a specific cell/row.", "why_it_matters": "Second-line reviewers will spot untraceable claims immediately."},
            ],
            "how_to_use": [
                "Section A: Use case & objectives (from Artifact 1).",
                "Section B: Solution overview (from Artifact 2).",
                "Section C: Cost model (Artifacts 3–8).",
                "Section D: Benefits model (Artifact 11).",
                "Section E: ROI results (Artifact 12) + sensitivity (Artifact 9).",
                "Section F: Implementation plan + governance (Artifact 15/16/17).",
                "Appendix: pricing table, driver map, pilot summary, data dictionary.",
            ],
            "worked_example": "Every heading fills to 2–5 paragraphs; forecast tables reproduced or referenced.",
            "pitfalls": ["Repeating the one-pager verbatim.", "Missing appendix (auditors will ask)."],
            "decision_tree": ["If governance body is bank/regulator-facing → treat as a submission and route through legal."],
            "domain_overlays": {k: "Adjust governance headings to your control framework." for k in DOMAIN_OVERLAY_KEYS},
        },
        "fields": [
            {"key": "section_a", "label": "Section A: Use case & objectives", "type": "textarea"},
            {"key": "section_b", "label": "Section B: Solution overview", "type": "textarea"},
            {"key": "section_c", "label": "Section C: Cost model", "type": "textarea"},
            {"key": "section_d", "label": "Section D: Benefits model", "type": "textarea"},
            {"key": "section_e", "label": "Section E: ROI results", "type": "textarea"},
            {"key": "section_f", "label": "Section F: Implementation plan", "type": "textarea"},
            {"key": "appendix", "label": "Appendix", "type": "textarea"},
        ],
        "tables": [],
    }


def _artifact_15() -> dict[str, Any]:
    return {
        "id": "A15",
        "number": 15,
        "title": "Risk Register & Controls Checklist",
        "short_title": "Risk & Controls",
        "role_context": (
            "The Principal Consultant is a de facto risk practitioner. Even in domains without an enforced framework, "
            "producing a risk register with cost impact makes the business case defensible."
        ),
        "purpose": "Prove the business case accounts for operational and governance risks that affect cost, quality, and compliance.",
        "when_to_use": "Week 6, alongside business case.",
        "inputs_needed": ["Full architecture, forecast, governance context"],
        "learning": {
            "concepts": [
                {"term": "Likelihood × impact", "definition": "Standard risk scoring on 3- or 5-point scales.", "why_it_matters": "Common language across risk domains."},
                {"term": "Detection metric", "definition": "A monitoring signal that indicates the risk is materializing.", "why_it_matters": "Risks without detection metrics are stories, not risks."},
                {"term": "Control effectiveness", "definition": "Preventative vs detective vs corrective.", "why_it_matters": "Preventative controls prevent cost; detective controls limit blast radius."},
            ],
            "how_to_use": [
                "Populate the register with at least: prompt bloat, quality drift, RAG recall drop, data governance gaps, eval scale, prompt injection, supply chain, dependency.",
                "For each, specify likelihood, impact, cost impact yes/no, control, owner, detection metric, mitigation plan.",
                "Verify the controls checklist against the OWASP LLM Top 10 and NIST AI RMF measure/manage functions.",
            ],
            "worked_example": (
                "R-001 Prompt bloat: L=M, I=H, cost impact yes, control=prompt-length caps + monthly review, "
                "owner=platform, detection=avg input tokens/request trending >20% MoM, mitigation=roll back prompt or "
                "add cache."
            ),
            "pitfalls": [
                "Risks without owners.",
                "Detection metrics that no dashboard actually shows.",
                "Ignoring supply-chain risk (model deprecation, vendor outage).",
            ],
            "decision_tree": [
                "If any risk × cost impact > 5% of monthly spend → escalate to the FinOps operating cadence (Artifact 17).",
                "If regulated data touched → route to compliance for control-adequacy sign-off.",
            ],
            "domain_overlays": {
                "generic": "Baseline risks above.",
                "banking": "Map to SR 11-7 model-risk tiering; add third-party-risk residual risk; add fair-lending disparate impact monitoring.",
                "retail": "Add PCI-scope creep, marketing-attribution disputes.",
                "energy_oil_gas": "Add safety-critical isolation and OT boundary controls.",
                "aerospace": "Add export-control classification error and configuration-item drift.",
                "public_sector": "Add ATO-boundary drift and records-management non-compliance.",
                "telecom": "Add CPNI leakage.",
                "entertainment": "Add rights-holder claim and training-data provenance.",
            },
        },
        "fields": [
            {"key": "controls_checklist", "label": "Controls checklist (freeform notes)", "type": "textarea"},
        ],
        "tables": [
            {
                "key": "risk_register",
                "label": "Risk register",
                "columns": [
                    {"key": "id", "label": "Risk ID"},
                    {"key": "description", "label": "Description"},
                    {"key": "category", "label": "Category"},
                    {"key": "likelihood", "label": "Likelihood"},
                    {"key": "impact", "label": "Impact"},
                    {"key": "cost_impact", "label": "Cost impact?"},
                    {"key": "control", "label": "Control"},
                    {"key": "owner", "label": "Owner"},
                    {"key": "detection", "label": "Detection metric"},
                    {"key": "mitigation", "label": "Mitigation"},
                ],
            }
        ],
    }


def _artifact_16() -> dict[str, Any]:
    return {
        "id": "A16",
        "number": 16,
        "title": "Evaluation & Quality Gate",
        "short_title": "Evaluation & Quality",
        "role_context": (
            "Quality is a cost driver. Failed requests trigger retries, longer outputs, more retrieval, more human review. "
            "The evaluation strategy IS a FinOps strategy."
        ),
        "purpose": "Define quality gates that influence retry rates, output length, escalations — and therefore cost.",
        "when_to_use": "Week 4–5.",
        "inputs_needed": ["Workload taxonomy", "Domain SMEs for labeled data", "Eval harness capability"],
        "learning": {
            "concepts": [
                {"term": "Offline eval", "definition": "Suite of prompts scored against golden outputs; run pre-release.", "why_it_matters": "Catches regressions cheaply before prod."},
                {"term": "Live shadow eval", "definition": "Model runs on production traffic in shadow; outputs scored without user impact.", "why_it_matters": "Captures real-distribution drift."},
                {"term": "Human review sampling", "definition": "Sampled outputs scored by SMEs periodically.", "why_it_matters": "Ground-truths automated scoring."},
                {"term": "Quality-cost coupling", "definition": "When quality falls, cost rises via retries, escalations, HITL time.", "why_it_matters": "Model the linkage in Artifact 8."},
            ],
            "how_to_use": [
                "Define suite coverage per request type.",
                "Set pass-rate, hallucination-rate, and escalation-rate targets and triggers.",
                "Define gate decision rules for prompt/RAG/routing changes.",
                "Model quality-to-cost coupling explicitly.",
            ],
            "worked_example": (
                "Offline suite: 320 prompts across 4 request types. Live shadow: 5% traffic. Human review: 100 outputs/week. "
                "Targets: pass rate 92%, hallucination rate <1%, escalation rate <8%. Any prompt change requires pass rate "
                "≥ 92% and hallucination ≤ 1% before merge."
            ),
            "pitfalls": [
                "Offline-only eval → misses live distribution drift.",
                "Not tracking eval-run cost → surprise line item.",
                "Gates that everyone bypasses under deadline pressure.",
            ],
            "decision_tree": [
                "If quality-cost coupling is high → invest more in RAG quality and reranker precision.",
                "If eval cost > 3% of run-rate → adopt staged eval (Artifact 10 OPT-006).",
            ],
            "domain_overlays": {
                "generic": "Baseline suites.",
                "banking": "Add adverse-action-language eval, fair-lending eval, and consumer-protection eval.",
                "retail": "Add product-safety and pricing-integrity eval.",
                "energy_oil_gas": "Add safety-relevant hallucination eval.",
                "aerospace": "Add regulatory-language integrity eval.",
                "public_sector": "Add accessibility/plain-language eval.",
                "telecom": "Add CPNI leakage eval.",
                "entertainment": "Add rights and content-safety eval.",
            },
        },
        "fields": [
            {"key": "eval_scope", "label": "Evaluation scope", "type": "textarea"},
        ],
        "tables": [
            {
                "key": "quality_metrics",
                "label": "Quality metrics",
                "columns": [
                    {"key": "metric", "label": "Metric"},
                    {"key": "definition", "label": "Definition"},
                    {"key": "target", "label": "Target"},
                    {"key": "trigger", "label": "Trigger"},
                ],
            },
            {
                "key": "gate_rules",
                "label": "Gate decision rules",
                "columns": [
                    {"key": "change", "label": "Change type"},
                    {"key": "gate_required", "label": "Gate required?"},
                    {"key": "condition", "label": "Approval condition"},
                ],
            },
        ],
    }


def _artifact_17() -> dict[str, Any]:
    return {
        "id": "A17",
        "number": 17,
        "title": "FinOps Operating Model (RACI + Cadence)",
        "short_title": "Operating Model",
        "role_context": (
            "Consulting engagements end; operating models remain. Principal Consultants leave behind a running "
            "operating model, not a one-time deliverable."
        ),
        "purpose": "Make cost management sustainable and repeatable after the consultant phase.",
        "when_to_use": "Week 7+.",
        "inputs_needed": ["Named leaders across product, engineering, finance, risk, compliance"],
        "learning": {
            "concepts": [
                {"term": "Cadence", "definition": "Fixed-frequency operating rhythm (weekly triage, monthly forecast, quarterly roadmap).", "why_it_matters": "Cadence is what keeps FinOps alive between crises."},
                {"term": "Dashboards", "definition": "Standing visual reports of cost by driver, cost per outcome, distributions, and anomalies.", "why_it_matters": "One source of truth reduces meeting time."},
                {"term": "Anomaly triage", "definition": "Standing meeting to review variance and route to owners.", "why_it_matters": "Anomalies compound if unaddressed."},
            ],
            "how_to_use": [
                "Publish RACI covering the seven activities in the template.",
                "Publish cadence: weekly (anomaly triage), monthly (forecast refresh), quarterly (optimization roadmap), per-change (quality gate).",
                "Publish dashboard requirements.",
                "Assign each dashboard to an owner.",
            ],
            "worked_example": (
                "Weekly Wednesday 30-min anomaly triage: platform, finance, product. Monthly first-Thursday 60-min "
                "forecast refresh: finance + workload owners. Quarterly optimization roadmap: leadership + AI CoE. "
                "Per-change quality gate: governance officer + independent validator."
            ),
            "pitfalls": [
                "RACI with multiple accountables.",
                "Cadences that never get run.",
                "Dashboards no one owns.",
            ],
            "decision_tree": ["If cadence attendance drops below 60% → reduce frequency or consolidate meetings."],
            "domain_overlays": {
                "generic": "Baseline cadence.",
                "banking": "Add first-line/second-line/third-line seats at forecast refresh.",
                "retail": "Align cadence to fiscal quarters and peak seasons.",
                "energy_oil_gas": "Include safety and reliability engineering.",
                "aerospace": "Include configuration control board.",
                "public_sector": "Align to appropriation cycles and OMB reporting.",
                "telecom": "Include NOC/reliability.",
                "entertainment": "Include IP counsel at production milestones.",
            },
        },
        "fields": [
            {"key": "dashboards", "label": "Dashboards required (list)", "type": "textarea"},
        ],
        "tables": [
            {
                "key": "raci",
                "label": "RACI",
                "columns": [
                    {"key": "activity", "label": "Activity"},
                    {"key": "r", "label": "Responsible"},
                    {"key": "a", "label": "Accountable"},
                    {"key": "c", "label": "Consulted"},
                    {"key": "i", "label": "Informed"},
                ],
            },
            {
                "key": "cadence",
                "label": "Cadence",
                "columns": [
                    {"key": "cadence", "label": "Cadence"},
                    {"key": "meeting", "label": "Meeting"},
                    {"key": "outputs", "label": "Outputs"},
                    {"key": "attendees", "label": "Attendees"},
                ],
            },
        ],
    }


def _artifact_18() -> dict[str, Any]:
    return {
        "id": "A18",
        "number": 18,
        "title": "Chargeback / Showback Allocation",
        "short_title": "Chargeback / Showback",
        "role_context": (
            "Allocation drives behavior. Wrong allocation basis creates perverse incentives (e.g., LOBs avoid AI to "
            "avoid cost). Principal Consultants pick the basis that aligns with the value being created."
        ),
        "purpose": "Allocate AI spend to cost centers/products in a way that aligns incentives.",
        "when_to_use": "Week 7+ once cost drivers and unit economics are stable.",
        "inputs_needed": ["Cost driver map", "Unit economics", "Finance policy on chargeback vs showback"],
        "learning": {
            "concepts": [
                {"term": "Allocation basis", "definition": "The primary key used to split cost (requests, tokens, cost per outcome, feature usage).", "why_it_matters": "Basis affects who bears cost — and therefore adoption behavior."},
                {"term": "Shared platform cost", "definition": "Non-attributable overhead (eval harness, observability).", "why_it_matters": "Must be allocated fairly (usage share) not equally."},
                {"term": "Showback first, chargeback later", "definition": "Report allocated cost for 2–3 cycles before actually moving budgets.", "why_it_matters": "Reduces first-year disputes."},
            ],
            "how_to_use": [
                "Pick the allocation basis. Cost per successful outcome × volume is the most defensible.",
                "Write allocation rules including fallback when metadata is missing.",
                "Publish monthly by cost center × workload.",
                "Start with showback; move to chargeback after 2 clean cycles.",
            ],
            "worked_example": (
                "Basis: cost per request type × request volume by cost center, plus 8% shared-platform allocation "
                "weighted by usage share. Monthly report to LOB CFOs. Chargeback effective July 2026 following 3 clean "
                "showback cycles."
            ),
            "pitfalls": [
                "Equal-share allocation of shared platform → penalizes early adopters.",
                "Chargeback without showback first → immediate disputes.",
                "Missing metadata → cost lands in the wrong bucket silently.",
            ],
            "decision_tree": [
                "If workload metadata coverage < 95% → stay in showback.",
                "If any LOB will bear >30% of the shared pool → renegotiate the basis.",
            ],
            "domain_overlays": {
                "generic": "Baseline allocation.",
                "banking": "Add LOB, product family, and (where regulated) capital-attribution notes.",
                "retail": "Split by banner, region, and campaign.",
                "energy_oil_gas": "Split by asset and business unit.",
                "aerospace": "Split by program and contract.",
                "public_sector": "Split by appropriation and program.",
                "telecom": "Split by segment and geography.",
                "entertainment": "Split by title/production.",
            },
        },
        "fields": [
            {"key": "allocation_basis", "label": "Allocation basis", "type": "select", "options": ["Requests", "Tokens", "Cost per successful outcome", "Feature usage / workload contribution", "Ticket deflection count"]},
            {"key": "showback_or_chargeback", "label": "Showback or chargeback?", "type": "select", "options": ["Showback", "Chargeback"]},
        ],
        "tables": [
            {
                "key": "rules",
                "label": "Allocation rules",
                "columns": [
                    {"key": "id", "label": "Rule ID"},
                    {"key": "condition", "label": "If condition"},
                    {"key": "method", "label": "Allocation method"},
                    {"key": "example", "label": "Formula / Example"},
                ],
            },
            {
                "key": "output",
                "label": "Monthly allocation output",
                "columns": [
                    {"key": "month", "label": "Month"},
                    {"key": "cost_center", "label": "Cost center"},
                    {"key": "workload", "label": "Workload"},
                    {"key": "inference", "label": "Allocated inference"},
                    {"key": "retrieval", "label": "Allocated retrieval"},
                    {"key": "platform", "label": "Allocated platform"},
                    {"key": "total", "label": "Total"},
                ],
            },
        ],
    }


def _artifact_19() -> dict[str, Any]:
    return {
        "id": "A19",
        "number": 19,
        "title": "Vendor & Pricing Negotiation Tracker",
        "short_title": "Vendor Tracker",
        "role_context": "Vendor pricing changes are the largest exogenous shock to the forecast. Track them.",
        "purpose": "Track vendor pricing, terms, and negotiation status.",
        "when_to_use": "Continuous.",
        "inputs_needed": ["Contract inventory", "Procurement contacts"],
        "learning": {
            "concepts": [
                {"term": "Effective date", "definition": "When the pricing took effect. Every row must have one.", "why_it_matters": "Retroactive forecast rebuilds need effective dates."},
                {"term": "Volume commitment / true-up", "definition": "Committed volume in exchange for lower unit price.", "why_it_matters": "Under-utilization can burn cash; over-utilization can burn overage."},
                {"term": "Renewal window", "definition": "Time before contract auto-renew when renegotiation is possible.", "why_it_matters": "Miss the window, lose the leverage."},
            ],
            "how_to_use": [
                "One row per vendor per contract line.",
                "Track renewal date, term, and negotiation levers.",
                "Feed the pricing table (Artifact 3) whenever a contract changes.",
            ],
            "worked_example": "Anthropic Enterprise 12-month contract, 20% off list at $12M/yr committed spend, renewal 2026-Q3.",
            "pitfalls": ["Missing effective dates.", "Not tracking overage exposure."],
            "decision_tree": ["If renewal within 90 days → open negotiation plan; feed procurement."],
            "domain_overlays": {k: "Add domain-specific procurement approvers." for k in DOMAIN_OVERLAY_KEYS},
        },
        "fields": [],
        "tables": [
            {
                "key": "vendors",
                "label": "Vendor pricing tracker",
                "columns": [
                    {"key": "vendor", "label": "Vendor"},
                    {"key": "term", "label": "Contract term"},
                    {"key": "inference_pricing", "label": "Inference pricing"},
                    {"key": "retrieval_pricing", "label": "Retrieval / vector pricing"},
                    {"key": "effective_date", "label": "Effective date"},
                    {"key": "notes", "label": "Notes"},
                ],
            }
        ],
    }


def _artifact_20() -> dict[str, Any]:
    return {
        "id": "A20",
        "number": 20,
        "title": "Data Dictionary",
        "short_title": "Data Dictionary",
        "role_context": "Every field in every log, every dashboard, every allocation feed traces back to this dictionary.",
        "purpose": "Provide an audit-ready dictionary of all data fields used across the pack.",
        "when_to_use": "Continuous.",
        "inputs_needed": ["Full telemetry inventory", "Privacy office guidance"],
        "learning": {
            "concepts": [
                {"term": "Source of truth", "definition": "The single system that owns the definition of a field.", "why_it_matters": "Ambiguous ownership creates conflicting numbers."},
                {"term": "PII handling", "definition": "How each field is classified and redacted.", "why_it_matters": "Legal risk if wrong."},
            ],
            "how_to_use": [
                "Every field used in any artifact appears here.",
                "Approve with privacy office before pilot begins.",
            ],
            "worked_example": "request_id (UUIDv4) — inference proxy — string — no PII — retention 13 months.",
            "pitfalls": ["Stale definitions."],
            "decision_tree": ["If a field appears in an artifact but not here → block release."],
            "domain_overlays": {k: "Add domain-specific classification schemes." for k in DOMAIN_OVERLAY_KEYS},
        },
        "fields": [],
        "tables": [
            {
                "key": "dictionary",
                "label": "Data dictionary",
                "columns": [
                    {"key": "field", "label": "Field"},
                    {"key": "meaning", "label": "Meaning"},
                    {"key": "source", "label": "Source system"},
                    {"key": "format", "label": "Format"},
                    {"key": "pii", "label": "PII handling"},
                ],
            }
        ],
    }


def _artifact_21() -> dict[str, Any]:
    return {
        "id": "A21",
        "number": 21,
        "title": "Cost Anomaly Playbook",
        "short_title": "Anomaly Playbook",
        "role_context": "When the daily bill jumps 40%, the playbook decides how fast you find and fix it.",
        "purpose": "Provide standing triage steps for cost anomalies.",
        "when_to_use": "Every anomaly.",
        "inputs_needed": ["Dashboard access", "Contact list for owners"],
        "learning": {
            "concepts": [
                {"term": "Threshold", "definition": "The variance level that triggers the playbook (e.g., ±15% daily vs 30-day baseline).", "why_it_matters": "Undefined thresholds → nothing gets investigated."},
                {"term": "First-check / second-check", "definition": "Ordered diagnostic steps that eliminate common causes fast.", "why_it_matters": "Speed matters; a playbook halves triage time."},
            ],
            "how_to_use": [
                "For each symptom (spike in tokens, retries, retrieval calls, vector reads, HITL escalations), list likely cause, first check, second check, fix.",
                "Assign a rotating owner.",
                "Log every anomaly and outcome (feeds Artifact 1 decision log).",
            ],
            "worked_example": (
                "Symptom: daily inference cost +48%. Likely cause: prompt regression added tokens. First check: "
                "compare avg input tokens vs prior 7 days. Second check: git blame the prompt file. Fix: roll back or "
                "apply caching."
            ),
            "pitfalls": ["Playbook that nobody reads.", "Alerts without owners."],
            "decision_tree": ["If anomaly recurs 2x in 30 days → escalate to Artifact 15 risk register."],
            "domain_overlays": {k: "Domain-specific first-checks." for k in DOMAIN_OVERLAY_KEYS},
        },
        "fields": [],
        "tables": [
            {
                "key": "playbook",
                "label": "Anomaly playbook",
                "columns": [
                    {"key": "symptom", "label": "Symptom"},
                    {"key": "likely_cause", "label": "Likely cause"},
                    {"key": "first_check", "label": "First check"},
                    {"key": "second_check", "label": "Second check"},
                    {"key": "fix", "label": "Fix"},
                ],
            }
        ],
    }


ARTIFACTS: list[dict[str, Any]] = [
    _artifact_1(), _artifact_2(), _artifact_3(), _artifact_4(), _artifact_5(),
    _artifact_6(), _artifact_7(), _artifact_8(), _artifact_9(), _artifact_10(),
    _artifact_11(), _artifact_12(), _artifact_13(), _artifact_14(), _artifact_15(),
    _artifact_16(), _artifact_17(), _artifact_18(), _artifact_19(), _artifact_20(),
    _artifact_21(),
]


def get_artifact(artifact_id: str) -> dict[str, Any] | None:
    for a in ARTIFACTS:
        if a["id"] == artifact_id:
            return a
    return None


def list_artifacts_summary() -> list[dict[str, Any]]:
    return [
        {
            "id": a["id"],
            "number": a["number"],
            "title": a["title"],
            "short_title": a["short_title"],
            "purpose": a["purpose"],
        }
        for a in ARTIFACTS
    ]
