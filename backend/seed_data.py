"""Seed 3 realistic AI use cases across LOBs.

Values chosen to reflect realistic 2025-2026 pricing benchmarks and unit economics.
"""

SEED_PROJECTS = [
    # -------------------------------------------------------------------
    # Project 1: Contact Center RAG Assistant (Consumer Banking LOB)
    # -------------------------------------------------------------------
    {
        "name": "Contact Center RAG Assistant",
        "lob": "Consumer Banking",
        "domain": "banking",
        "summary": (
            "Agent-assist RAG copilot for the consumer banking contact center. Retrieves policy, procedure, and "
            "account-specific context and drafts responses that human agents edit and send."
        ),
        "status": "pilot",
        "owner": "Chris Clark (Principal AI Solutions Consultant)",
        "entries": {
            "A01": {
                "fields": {
                    "use_case_name": "Contact Center RAG Assistant",
                    "lob": "Consumer Banking",
                    "domain": "banking",
                    "business_owner": "VP, Contact Center Operations",
                    "product_owner": "Director, Digital Servicing",
                    "technical_owner": "Principal Engineer, AI Platform",
                    "finance_partner": "Director, Servicing Finance",
                    "risk_partner": "SVP, Model Risk Management",
                    "workload_paragraph": (
                        "Contact center agents ask the assistant a question about a customer's account or a policy. "
                        "The assistant retrieves relevant knowledge-base articles and account context, drafts a "
                        "suggested response, and the agent edits before sending. HITL is mandatory for every customer-"
                        "facing message."
                    ),
                    "in_scope": [
                        "Frontend/API", "Orchestrator/agent framework", "Model(s) / endpoints",
                        "RAG pipeline (ingestion + retrieval)", "Vector DB", "Evaluation harness",
                        "Observability/telemetry", "Human-in-the-loop workflow",
                    ],
                    "out_of_scope": (
                        "CRM system engineering, one-time ingestion of 3.1M policy documents, and "
                        "downstream analytics dashboards."
                    ),
                    "environments": ["Dev", "Test", "Prod"],
                    "regions_accounts": "US East (primary), US West (DR)",
                    "data_classification": "PII + confidential customer data. GLBA scope. No PCI.",
                    "cost_objective": "Forecast Year-1 monthly cost within +/-10% of actuals",
                    "performance_objective": "P90 latency < 2.5s end-to-end",
                    "quality_objective": "Agent acceptance rate >= 92% (sampled QA)",
                    "adoption_objective": "70% of eligible agents use the assistant >= 5 times/shift by month 9",
                    "governance_objective": "SR 11-7 Tier 2 model risk designation with quarterly revalidation",
                    "boundary_statement": (
                        "Costs included: LLM inference (input, cached input, output tokens), retrieval search, "
                        "vector DB storage and query, embedding generation, evaluation harness runs, "
                        "safety/guardrail calls, and human-in-the-loop reviewer time. Excluded: CRM integration "
                        "engineering, one-time document ingestion, and executive dashboarding."
                    ),
                    "measurement_approach": (
                        "Shadow mode on 15% of live agent traffic for 10 business days. Extract token counts, "
                        "retrieval calls, retry rates, and quality-gate outcomes per request_id."
                    ),
                    "target_dates": (
                        "Week 1 (2026-01-06): boundary + drivers. Week 3: instrumentation live. Week 5: pilot "
                        "closes. Week 6: cost model + scenarios. Week 7: business case + governance handoff."
                    ),
                },
                "tables": {
                    "decision_log": [
                        {"date": "2026-01-06", "decision": "Adopt Claude Sonnet 4.5 as default; Haiku for classification",
                         "owner": "Principal Engineer", "rationale": "Best cost-quality on internal eval suite",
                         "link": "Eval report EV-2026-014"},
                        {"date": "2026-01-13", "decision": "Retention 90 days hot / 13 months cold for request logs",
                         "owner": "Privacy Office", "rationale": "GLBA + internal records policy alignment",
                         "link": "Privacy memo PM-2026-021"},
                    ]
                },
            },
            "A03": {
                "fields": {
                    "boundary_paragraph": (
                        "This model covers only production traffic in US-East and US-West. Dev/test excluded. "
                        "One-time ingestion of 3.1M policy documents is capitalized separately and excluded."
                    ),
                    "rounding_conventions": "Token counts rounded to nearest 1,000. Percentages rounded to nearest 0.5%.",
                    "currency": "USD",
                    "fx_assumption": "n/a - single currency",
                },
                "tables": {
                    "unit_pricing": [
                        {"component": "Claude Sonnet 4.5 - Input", "unit": "$/M tokens", "source": "Anthropic list",
                         "currency": "USD", "effective_date": "2025-09-29", "notes": "20% enterprise discount applied"},
                        {"component": "Claude Sonnet 4.5 - Cached Input", "unit": "$/M tokens", "source": "Anthropic list",
                         "currency": "USD", "effective_date": "2025-09-29", "notes": "$0.30/M with discount = $0.24/M"},
                        {"component": "Claude Sonnet 4.5 - Output", "unit": "$/M tokens", "source": "Anthropic list",
                         "currency": "USD", "effective_date": "2025-09-29", "notes": "$15/M list, $12/M after discount"},
                        {"component": "Claude Haiku 4 - Input", "unit": "$/M tokens", "source": "Anthropic list",
                         "currency": "USD", "effective_date": "2025-09-29", "notes": ""},
                        {"component": "Claude Haiku 4 - Output", "unit": "$/M tokens", "source": "Anthropic list",
                         "currency": "USD", "effective_date": "2025-09-29", "notes": ""},
                        {"component": "Pinecone Serverless read", "unit": "$/M read units", "source": "Contract",
                         "currency": "USD", "effective_date": "2025-11-01", "notes": ""},
                        {"component": "Pinecone Serverless storage", "unit": "$/GB-month", "source": "Contract",
                         "currency": "USD", "effective_date": "2025-11-01", "notes": ""},
                        {"component": "OpenAI text-embedding-3-large", "unit": "$/M tokens", "source": "OpenAI list",
                         "currency": "USD", "effective_date": "2025-08-15", "notes": "Used at ingest and periodic re-embed"},
                        {"component": "Reviewer time", "unit": "$/minute", "source": "Loaded rate",
                         "currency": "USD", "effective_date": "2026-01-01", "notes": "$110/hr agent loaded rate"},
                    ],
                    "assumptions": [
                        {"assumption": "Avg input tokens/request", "value": "2,400", "basis": "Pilot log 2026-01",
                         "confidence": "H", "risk": "OOM budget surprise if bloated"},
                        {"assumption": "Cached share of input", "value": "50%", "basis": "System prompt caching target",
                         "confidence": "M", "risk": "Total inference cost overstated"},
                        {"assumption": "Avg output tokens/request", "value": "380", "basis": "Pilot log 2026-01",
                         "confidence": "H", "risk": "Latency and cost"},
                        {"assumption": "RAG top-k", "value": "8", "basis": "Design spec", "confidence": "H",
                         "risk": "Recall drop if lowered"},
                        {"assumption": "Retry rate", "value": "6%", "basis": "Quality gate policy",
                         "confidence": "M", "risk": "Spend spikes if gate too strict"},
                        {"assumption": "Reviewer time per assist", "value": "1.8 min", "basis": "Ops sample",
                         "confidence": "M", "risk": "HITL cost dominates model cost"},
                    ],
                },
            },
            "A04": {
                "fields": {"inclusion_rules": (
                    "Count only production request_ids tagged env=prod. Exclude health checks. Exclude "
                    "dev/test tenant requests. Include shadow-mode requests only when calibrating, not when "
                    "reporting monthly actuals."
                )},
                "tables": {
                    "driver_map": [
                        {"driver": "Input tokens (prod)", "definition": "sum(prompt_tokens) where env=prod",
                         "signal": "inference proxy access log", "computed": "sum in query",
                         "unit": "tokens", "unit_cost": "$2.40/M (blended after cache)",
                         "default": "2400/req", "confidence": "H"},
                        {"driver": "Output tokens (prod)", "definition": "sum(completion_tokens) where env=prod",
                         "signal": "inference proxy access log", "computed": "sum in query",
                         "unit": "tokens", "unit_cost": "$12/M (Sonnet output, discount)",
                         "default": "380/req", "confidence": "H"},
                        {"driver": "Retrieval calls", "definition": "count of RAG retriever queries per request",
                         "signal": "retriever telemetry", "computed": "count",
                         "unit": "queries", "unit_cost": "$0.25/M read units",
                         "default": "2/req", "confidence": "H"},
                        {"driver": "Reranker calls", "definition": "count(reranker invocation)",
                         "signal": "reranker service log", "computed": "count",
                         "unit": "calls", "unit_cost": "$0.60/M tokens",
                         "default": "0.3/req", "confidence": "M"},
                        {"driver": "Eval runs", "definition": "count(offline eval + shadow eval runs)",
                         "signal": "eval harness log", "computed": "count",
                         "unit": "runs", "unit_cost": "$8/run avg",
                         "default": "180/mo", "confidence": "M"},
                        {"driver": "Vector DB storage", "definition": "GB-months of indexed content",
                         "signal": "Pinecone billing", "computed": "monthly rollup",
                         "unit": "GB-month", "unit_cost": "$0.33/GB-month",
                         "default": "82 GB", "confidence": "H"},
                        {"driver": "Reviewer minutes", "definition": "sum of HITL edit + approval minutes",
                         "signal": "review queue timestamps", "computed": "sum",
                         "unit": "minutes", "unit_cost": "$1.83/min",
                         "default": "1.8/req", "confidence": "M"},
                    ]
                },
            },
            "A07": {
                "tables": {
                    "unit_inputs": [
                        {"request_type": "Short factual", "routing_mix": "85% Haiku / 15% Sonnet",
                         "avg_in": "1200", "cached_share": "45%", "avg_out": "220",
                         "retrieval_calls": "2", "reranker_rate": "30%", "tool_calls": "0.2",
                         "retry_rate": "4%", "success_rate": "92%"},
                        {"request_type": "Long analytical", "routing_mix": "20% Haiku / 80% Sonnet",
                         "avg_in": "3200", "cached_share": "55%", "avg_out": "550",
                         "retrieval_calls": "4", "reranker_rate": "70%", "tool_calls": "0.4",
                         "retry_rate": "8%", "success_rate": "89%"},
                        {"request_type": "RAG-heavy", "routing_mix": "10% Haiku / 90% Sonnet",
                         "avg_in": "4600", "cached_share": "40%", "avg_out": "620",
                         "retrieval_calls": "6", "reranker_rate": "100%", "tool_calls": "0.1",
                         "retry_rate": "9%", "success_rate": "88%"},
                    ],
                    "unit_outputs": [
                        {"request_type": "Short factual", "cost_per_request": "$0.0028",
                         "cost_per_success": "$0.0030", "cost_per_1k": "$3.03"},
                        {"request_type": "Long analytical", "cost_per_request": "$0.0154",
                         "cost_per_success": "$0.0173", "cost_per_1k": "$17.31"},
                        {"request_type": "RAG-heavy", "cost_per_request": "$0.0212",
                         "cost_per_success": "$0.0241", "cost_per_1k": "$24.09"},
                    ],
                },
            },
            "A08": {
                "fields": {"inclusion_rules_forecast": (
                    "Production only. Excludes one-time ingestion. HITL cost included as a separate line."
                )},
                "tables": {
                    "cost_forecast": [
                        {"month": "2026-08", "component": "Inference (Haiku)", "request_type": "Short factual",
                         "quantity": "76M input / 14M output", "unit_cost": "blended", "total_cost": "$920"},
                        {"month": "2026-08", "component": "Inference (Sonnet)", "request_type": "All",
                         "quantity": "112M input / 21M output", "unit_cost": "blended", "total_cost": "$3,180"},
                        {"month": "2026-08", "component": "Retrieval", "request_type": "All",
                         "quantity": "1.1M queries", "unit_cost": "$0.25/M reads", "total_cost": "$275"},
                        {"month": "2026-08", "component": "Vector DB storage", "request_type": "n/a",
                         "quantity": "82 GB-month", "unit_cost": "$0.33/GB", "total_cost": "$27"},
                        {"month": "2026-08", "component": "Embeddings (re-embed 5%)", "request_type": "n/a",
                         "quantity": "18M tokens", "unit_cost": "$0.13/M", "total_cost": "$2"},
                        {"month": "2026-08", "component": "Evaluation", "request_type": "All",
                         "quantity": "220 runs", "unit_cost": "$8/run", "total_cost": "$1,760"},
                        {"month": "2026-08", "component": "Guardrails", "request_type": "All",
                         "quantity": "560k calls", "unit_cost": "avg", "total_cost": "$210"},
                        {"month": "2026-08", "component": "HITL reviewer time", "request_type": "All",
                         "quantity": "1.05M minutes", "unit_cost": "$1.83/min", "total_cost": "$1,921,500"},
                        {"month": "2026-08", "component": "Platform allocation", "request_type": "n/a",
                         "quantity": "usage share", "unit_cost": "n/a", "total_cost": "$3,600"},
                    ]
                },
            },
            "A12": {
                "fields": {
                    "discount_rate": 0.10,
                    "horizon_months": 36,
                    "implementation_cost": 850000,
                    "benefits_start_month": 3,
                },
                "tables": {
                    "outputs": [
                        {"scenario": "Downside", "npv": "$3.2M", "payback": "18", "irr": "42%", "bcr": "1.7x"},
                        {"scenario": "Base", "npv": "$9.8M", "payback": "11", "irr": "94%", "bcr": "3.1x"},
                        {"scenario": "Upside", "npv": "$16.4M", "payback": "8", "irr": "148%", "bcr": "4.8x"},
                    ]
                },
            },
            "A13": {
                "fields": {
                    "recommendation": "Approve $2.4M Year-1 scale funding to expand the contact center RAG assistant from pilot to production across the consumer banking servicing organization.",
                    "budget_range": "$2.1M - $2.8M Year-1 all-in",
                    "timeline": "Scale phase: 2026-Q3 through 2026-Q4",
                    "why_now": "Contact center volumes projected to grow 12% next fiscal. Competitor deployments launched Q4 2025. Current pilot shows sustained 92% acceptance and 4-minute per-assist time savings.",
                    "solution_summary": "RAG-based agent copilot with strict HITL. Claude Sonnet 4.5 primary with Haiku for classification. Pinecone Serverless vector DB. SR 11-7 Tier 2 model.",
                    "cost_outlook": "Year-1 monthly base $220k, range $165k - $310k. HITL cost dominates.",
                    "expected_benefits": "$8.2M incremental Year-1 (matched-cohort attribution). Labor efficiency: 4 min/assist * $1.83/min * volume.",
                    "roi_headline": "NPV $9.8M base (range $3.2M - $16.4M). Payback 11 months base. Top risks: adoption slower than plan; second-line validation timeline.",
                    "next_step": "Kick off scale phase 2026-Q3 with quality gate at 92% and reviewer sampling at 15%. Independent validation cadence: quarterly.",
                },
                "tables": {},
            },
            "A15": {
                "tables": {
                    "risk_register": [
                        {"id": "R-001", "description": "Prompt bloat increases tokens", "category": "Cost",
                         "likelihood": "M", "impact": "H", "cost_impact": "Yes",
                         "control": "Prompt length caps + monthly review",
                         "owner": "AI Platform", "detection": "Avg input tokens trend > 20% MoM",
                         "mitigation": "Roll back prompt or enable prompt caching"},
                        {"id": "R-002", "description": "Quality drift causes retries and escalations", "category": "Cost/Perf",
                         "likelihood": "M", "impact": "H", "cost_impact": "Yes",
                         "control": "Quality gate + regression suite before any change",
                         "owner": "AI Platform", "detection": "Pass rate < 90% or retry rate > 8%",
                         "mitigation": "Revert model/prompt; re-tune"},
                        {"id": "R-003", "description": "RAG recall drop", "category": "Cost/Quality",
                         "likelihood": "M", "impact": "M", "cost_impact": "Yes",
                         "control": "RAG monitoring; metadata filters",
                         "owner": "AI Platform", "detection": "Retrieval hit rate < baseline",
                         "mitigation": "Re-tune top-k or reranker"},
                        {"id": "R-004", "description": "GLBA data leakage in logs", "category": "Compliance",
                         "likelihood": "L", "impact": "H", "cost_impact": "Indirect",
                         "control": "Redaction at ingest; audit logs; DLP",
                         "owner": "Privacy Office", "detection": "DLP alerts",
                         "mitigation": "Purge; incident response"},
                        {"id": "R-005", "description": "SR 11-7 validation delay", "category": "Governance",
                         "likelihood": "M", "impact": "H", "cost_impact": "Yes (opex delay)",
                         "control": "Early engagement with MRM; documented tiering",
                         "owner": "MRM", "detection": "Validation calendar slippage",
                         "mitigation": "Escalate; adjust scale timeline"},
                        {"id": "R-006", "description": "Vendor deprecation of Claude Sonnet 4.5", "category": "Supply chain",
                         "likelihood": "M", "impact": "M", "cost_impact": "Yes",
                         "control": "Vendor-independent prompt store; multi-model eval suite",
                         "owner": "AI Platform", "detection": "Vendor announcements",
                         "mitigation": "Migrate to next-gen model with re-validation"},
                    ]
                },
            },
        },
    },

    # -------------------------------------------------------------------
    # Project 2: Underwriting Document Assist (Commercial Lending LOB)
    # -------------------------------------------------------------------
    {
        "name": "Underwriting Document Assist",
        "lob": "Commercial Lending",
        "domain": "banking",
        "summary": (
            "Analyst-assist tool that summarizes borrower financials, extracts covenants, and drafts memo sections. "
            "Every output is reviewed and approved by a human underwriter."
        ),
        "status": "business_case",
        "owner": "Chris Clark (Principal AI Solutions Consultant)",
        "entries": {
            "A01": {
                "fields": {
                    "use_case_name": "Underwriting Document Assist",
                    "lob": "Commercial Lending",
                    "domain": "banking",
                    "business_owner": "Head of Middle Market Underwriting",
                    "product_owner": "Director, Credit Product",
                    "technical_owner": "Senior Principal, AI Engineering",
                    "finance_partner": "Director, Commercial Finance",
                    "risk_partner": "Chief Model Risk Officer",
                    "workload_paragraph": (
                        "Underwriter uploads a set of borrower financials (tax returns, statements, appraisals). "
                        "The assistant extracts key metrics, flags covenant items, and drafts memo sections. "
                        "Underwriter reviews and edits before submission to committee."
                    ),
                    "cost_objective": "Forecast Year-1 within +/-12%",
                    "performance_objective": "Full document pass < 90s",
                    "quality_objective": "Extraction precision >= 95% on covenant items",
                    "adoption_objective": "80% of eligible middle-market deals use the assistant by month 12",
                    "governance_objective": "SR 11-7 Tier 1 (higher tier due to decision influence)",
                    "boundary_statement": (
                        "Costs included: inference, retrieval, embeddings, evaluation, guardrails, HITL. "
                        "Excluded: document management engineering, credit committee workflow, and legal review."
                    ),
                },
                "tables": {},
            },
            "A07": {
                "tables": {
                    "unit_inputs": [
                        {"request_type": "Financial extraction", "routing_mix": "0% Haiku / 100% Sonnet",
                         "avg_in": "18000", "cached_share": "25%", "avg_out": "1400",
                         "retrieval_calls": "0", "reranker_rate": "0%", "tool_calls": "3.2",
                         "retry_rate": "5%", "success_rate": "94%"},
                        {"request_type": "Memo drafting", "routing_mix": "0% Haiku / 100% Sonnet",
                         "avg_in": "22000", "cached_share": "60%", "avg_out": "2800",
                         "retrieval_calls": "6", "reranker_rate": "100%", "tool_calls": "0.8",
                         "retry_rate": "7%", "success_rate": "90%"},
                    ],
                    "unit_outputs": [
                        {"request_type": "Financial extraction", "cost_per_request": "$0.09",
                         "cost_per_success": "$0.096", "cost_per_1k": "$95.74"},
                        {"request_type": "Memo drafting", "cost_per_request": "$0.13",
                         "cost_per_success": "$0.145", "cost_per_1k": "$144.44"},
                    ],
                },
            },
            "A13": {
                "fields": {
                    "recommendation": "Approve $3.8M investment to move Underwriting Document Assist from business case to production pilot across middle-market commercial lending.",
                    "budget_range": "$3.2M - $4.4M Year-1",
                    "timeline": "Pilot Q3 2026, scale Q1 2027",
                    "why_now": "Middle-market deal volume up 18%; underwriter capacity constrained. Extraction accuracy has cleared internal thresholds in bench testing.",
                    "solution_summary": "Extraction pipeline with structured output; retrieval-grounded memo drafting; mandatory underwriter approval.",
                    "cost_outlook": "Year-1 monthly base $148k (range $110k - $205k). HITL is the majority.",
                    "expected_benefits": "$11.2M incremental Year-1 through underwriter cycle-time reduction, holding pull-through constant.",
                    "roi_headline": "NPV $18.4M base; payback 14 months; top risks: SR 11-7 Tier 1 validation timeline and adverse-language regression.",
                    "next_step": "Independent model validation kickoff 2026-Q2; pilot 2026-Q3.",
                }, "tables": {},
            },
        },
    },

    # -------------------------------------------------------------------
    # Project 3: Developer Productivity Copilot (Technology Enablement LOB)
    # -------------------------------------------------------------------
    {
        "name": "Developer Productivity Copilot",
        "lob": "Technology Enablement",
        "domain": "generic",
        "summary": (
            "Internal developer copilot with codebase-aware retrieval, PR review assist, and doc generation. "
            "Multi-agent orchestration for complex refactors."
        ),
        "status": "scale",
        "owner": "Chris Clark (Principal AI Solutions Consultant)",
        "entries": {
            "A01": {
                "fields": {
                    "use_case_name": "Developer Productivity Copilot",
                    "lob": "Technology Enablement",
                    "domain": "generic",
                    "business_owner": "CTO Office",
                    "product_owner": "Head of Developer Experience",
                    "technical_owner": "Distinguished Engineer, DevX",
                    "finance_partner": "Director, Technology Finance",
                    "risk_partner": "Head of Application Security",
                    "workload_paragraph": (
                        "IDE-integrated copilot for internal developers. Codebase-aware retrieval, PR review "
                        "commentary, test scaffolding, and multi-agent refactor workflows."
                    ),
                    "cost_objective": "Cost per accepted suggestion < $0.05",
                    "performance_objective": "Suggestion latency < 800ms P90",
                    "quality_objective": "Acceptance rate >= 38%",
                    "adoption_objective": "90% of eligible engineers active weekly",
                    "governance_objective": "Standard software controls + data-loss prevention",
                    "boundary_statement": "Costs included: inference (per suggestion, per PR review, per multi-agent run), retrieval over private codebases, embeddings, evaluation, guardrails. Excluded: IDE plugin engineering, one-time codebase ingest.",
                },
                "tables": {},
            },
            "A07": {
                "tables": {
                    "unit_inputs": [
                        {"request_type": "Autocomplete", "routing_mix": "100% small (Haiku-tier)",
                         "avg_in": "480", "cached_share": "70%", "avg_out": "60",
                         "retrieval_calls": "1", "reranker_rate": "0%", "tool_calls": "0",
                         "retry_rate": "3%", "success_rate": "38%"},
                        {"request_type": "PR review", "routing_mix": "50% Haiku / 50% Sonnet",
                         "avg_in": "12000", "cached_share": "50%", "avg_out": "800",
                         "retrieval_calls": "4", "reranker_rate": "60%", "tool_calls": "1.2",
                         "retry_rate": "6%", "success_rate": "72%"},
                        {"request_type": "Multi-agent refactor", "routing_mix": "10% Haiku / 90% Sonnet",
                         "avg_in": "38000", "cached_share": "40%", "avg_out": "5200",
                         "retrieval_calls": "18", "reranker_rate": "100%", "tool_calls": "9.4",
                         "retry_rate": "12%", "success_rate": "68%"},
                    ],
                    "unit_outputs": [
                        {"request_type": "Autocomplete", "cost_per_request": "$0.0004",
                         "cost_per_success": "$0.0011", "cost_per_1k": "$1.05"},
                        {"request_type": "PR review", "cost_per_request": "$0.019",
                         "cost_per_success": "$0.026", "cost_per_1k": "$26.39"},
                        {"request_type": "Multi-agent refactor", "cost_per_request": "$0.68",
                         "cost_per_success": "$1.00", "cost_per_1k": "$1,000"},
                    ],
                },
            },
            "A13": {
                "fields": {
                    "recommendation": "Continue scale of Developer Productivity Copilot with a $6.1M Year-2 run-rate budget.",
                    "budget_range": "$5.4M - $7.0M Year-2",
                    "timeline": "Continuous",
                    "why_now": "Adoption at 88% weekly-active; acceptance rate rising; multi-agent refactor cohort showing 22% cycle-time reduction on sampled projects.",
                    "solution_summary": "IDE plugin + codebase RAG + multi-agent orchestration. Guardrails + DLP mandatory.",
                    "cost_outlook": "Year-2 monthly $505k base; multi-agent workloads are the swing driver.",
                    "expected_benefits": "$22.5M incremental Year-2; PR cycle-time reduction and defect deflection.",
                    "roi_headline": "NPV $42.0M base; payback fully paid at end of Year-1; top risks: multi-agent runaway loops and IP-exfiltration through prompts.",
                    "next_step": "Cap multi-agent step budget at 40 per run; expand PR review coverage.",
                }, "tables": {},
            },
        },
    },
]
