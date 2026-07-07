# AI Cost Architect — End-to-End Methodology

**Audience:** Principal AI Solutions Consultant leading enterprise AI cost management engagements.
**Scope:** How to run an engagement from first stakeholder conversation to steady-state operate.
**Deliverable framework:** The 21 reference artifacts in [`../templates/`](../templates/), managed by the portfolio app in [`../backend/`](../backend/) + [`../frontend/`](../frontend/).

This document tells you **what to do, in what order, with what artifact, and why**. Every artifact link below points at the actual DOCX template in this repo — click through, fill it in, or press "DOCX" in the running app to generate a filled copy from project data.

---

## Table of Contents

1. [Operating Principles](#1-operating-principles)
2. [Roles and Responsibilities](#2-roles-and-responsibilities)
3. [The 7 Phases at a Glance](#3-the-7-phases-at-a-glance)
4. [Phase 0 — Portfolio Intake](#4-phase-0--portfolio-intake)
5. [Phase 1 — Engagement Kickoff (Week 0–1)](#5-phase-1--engagement-kickoff-week-01)
6. [Phase 2 — Decomposition & Boundary (Week 1–2)](#6-phase-2--decomposition--boundary-week-12)
7. [Phase 3 — Instrumentation & Measurement (Week 2–4)](#7-phase-3--instrumentation--measurement-week-24)
8. [Phase 4 — Modeling: Unit Economics, Forecast, Scenarios (Week 3–5)](#8-phase-4--modeling-unit-economics-forecast-scenarios-week-35)
9. [Phase 5 — Optimization & Benefits (Week 4–5)](#9-phase-5--optimization--benefits-week-45)
10. [Phase 6 — Business Case & Governance Handoff (Week 5–6)](#10-phase-6--business-case--governance-handoff-week-56)
11. [Phase 7 — Operate & Steady State (Ongoing)](#11-phase-7--operate--steady-state-ongoing)
12. [Domain Overlays](#12-domain-overlays)
13. [Common Failure Modes and How to Avoid Them](#13-common-failure-modes-and-how-to-avoid-them)
14. [Governance Cadence Cheatsheet](#14-governance-cadence-cheatsheet)
15. [Appendix — Artifact Index](#15-appendix--artifact-index)

---

## 1. Operating Principles

These are the beliefs the methodology rests on. Break them only with a written justification in the Decision Log (Artifact 1).

1. **Cost is a design output, not a monthly surprise.** You decide most of the cost when you decide the architecture in Artifact 2 and the drivers in Artifact 4. Everything after is measurement.
2. **Unit economics or nothing.** Total spend is a fundraising number. Cost per successful outcome (Artifact 7) is the number that drives decisions.
3. **Every forecast is componentized.** Never model AI as one line item. Split into inference, retrieval, vector DB, embeddings, evaluation, guardrails, HITL, and platform (Artifact 8). Optimizations target components; totals do not.
4. **Measurement precedes optimization.** Do not accept an optimization proposal until Artifact 5 is live in production and Artifact 6 has reconciled a full pilot week within ±10%.
5. **Business case ROI must survive scrutiny.** Attributable benefit only (Artifact 11). Base case + downside (Artifact 9). Payback ≤ 18 months for enterprise AI. Show your assumptions and your sources.
6. **Governance is a design constraint, not a review gate.** Bake in second-line review, model-risk tiering, and audit trails from Phase 1 (Artifact 15) or you will retrofit them at 3× the cost.
7. **Steady-state operate is the actual product.** Consulting delivers Artifacts 1–16 once. Artifacts 17–21 run forever. Design them for the accountable Product/Finance/Platform triad, not for you.

---

## 2. Roles and Responsibilities

Named on every project via Artifact 1. Never leave any of these blank.

| Role                            | Owns                                                                                      | Signs off on                                                                                            |
| ------------------------------- | ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| **Business Owner**              | Outcome, adoption, benefits realization                                                   | [Artifact 1](../templates/Artifact_01_Kickoff_&_Scope.docx), [Artifact 13](../templates/Artifact_13_Exec_One-Pager.docx), [Artifact 14](../templates/Artifact_14_Business_Case_Narrative.docx), [Artifact 18](../templates/Artifact_18_Chargeback_-_Showback.docx) |
| **Product Owner**               | Requirements, roadmap, prioritization                                                     | [Artifact 1](../templates/Artifact_01_Kickoff_&_Scope.docx), [Artifact 2](../templates/Artifact_02_Workload_Decomposition.docx), [Artifact 16](../templates/Artifact_16_Evaluation_&_Quality.docx), [Artifact 17](../templates/Artifact_17_Operating_Model.docx) |
| **Technical Owner**             | Architecture, model choices, instrumentation                                              | [Artifact 2](../templates/Artifact_02_Workload_Decomposition.docx), [Artifact 4](../templates/Artifact_04_Cost_Driver_Map.docx), [Artifact 5](../templates/Artifact_05_Metering_&_Instrumentation.docx), [Artifact 10](../templates/Artifact_10_Optimization_Catalog.docx), [Artifact 20](../templates/Artifact_20_Data_Dictionary.docx) |
| **Finance Partner**             | Cost model, chargeback, ROI                                                               | [Artifact 3](../templates/Artifact_03_Boundary_&_Pricing.docx), [Artifact 8](../templates/Artifact_08_Cost_Forecast.docx), [Artifact 12](../templates/Artifact_12_ROI_-_NPV.docx), [Artifact 18](../templates/Artifact_18_Chargeback_-_Showback.docx) |
| **Risk/Compliance Partner**     | Model risk, controls, audit                                                               | [Artifact 15](../templates/Artifact_15_Risk_&_Controls.docx), [Artifact 16](../templates/Artifact_16_Evaluation_&_Quality.docx) |
| **AI Solutions Consultant (you)** | Methodology, artifact quality, cross-project consistency, portfolio view, escalation path | Every artifact — you are the editor of record.                                                          |

The Consultant is a **facilitator with veto power on artifact quality**, not the accountable executive. Push accountability to the named owner on every artifact.

---

## 3. The 7 Phases at a Glance

| Phase                                                                                          | Weeks         | Purpose                                          | Exit Criteria                                                            | Primary Artifacts |
| ---------------------------------------------------------------------------------------------- | ------------- | ------------------------------------------------ | ------------------------------------------------------------------------ | ----------------- |
| **[0. Portfolio Intake](#4-phase-0--portfolio-intake)**                                        | Pre-week      | Decide whether to take the project               | Project accepted into portfolio with tier assignment                     | Portfolio triage checklist (below) |
| **[1. Engagement Kickoff](#5-phase-1--engagement-kickoff-week-01)**                            | 0–1           | Shared, signed scope                             | [Artifact 1](../templates/Artifact_01_Kickoff_&_Scope.docx) signed by all named owners | 1 |
| **[2. Decomposition & Boundary](#6-phase-2--decomposition--boundary-week-12)**                 | 1–2           | Auditable architecture and cost boundary         | Artifacts 2, 3, 4 approved                                               | 2, 3, 4 |
| **[3. Instrumentation & Measurement](#7-phase-3--instrumentation--measurement-week-24)**       | 2–4           | Real cost data flowing                           | Artifact 5 in prod, Artifact 6 reconciled ±10%                           | 5, 6 |
| **[4. Modeling](#8-phase-4--modeling-unit-economics-forecast-scenarios-week-35)**              | 3–5           | Defensible unit econ and forecast                | Artifacts 7, 8, 9 with signed assumptions                                | 7, 8, 9 |
| **[5. Optimization & Benefits](#9-phase-5--optimization--benefits-week-45)**                   | 4–5           | Actionable cost levers and honest benefits       | Artifacts 10 and 11 with quantified impact                               | 10, 11 |
| **[6. Business Case & Governance](#10-phase-6--business-case--governance-handoff-week-56)**    | 5–6           | Decision-ready package                           | Executive committee decision recorded                                    | 12, 13, 14, 15, 16 |
| **[7. Operate](#11-phase-7--operate--steady-state-ongoing)**                                   | Ongoing       | Sustainable governance and cost discipline       | Monthly close on time for 3 consecutive months                           | 17, 18, 19, 20, 21 |

Phases 3 and 4 overlap. So do 5 and 6. Do not treat them as strict waterfall.

---

## 4. Phase 0 — Portfolio Intake

**Purpose:** Decide whether this use case belongs in the AI cost management portfolio at all, and at what tier.

**When to use:** Every new AI initiative surfaces here before you spend a day on it.

### Intake Questions (Consultant asks the sponsor)

1. **What outcome, in one sentence?** If they cannot answer, they are not ready.
2. **Who is the accountable business executive?** Not the sponsor of the sponsor. The one whose bonus moves.
3. **What is the funded budget, in dollars, this fiscal year?** If "TBD," come back when it is not.
4. **Is there existing production traffic, or is this greenfield?** Determines whether Artifact 6 has data to sample.
5. **Regulated data (PII/PHI/PCI/GLBA)?** Determines whether banking / healthcare / public-sector overlays kick in (see [§12](#12-domain-overlays)).
6. **Does another LOB have a lookalike?** If yes, you may accelerate by cloning artifacts. If no, expect full 6-week engagement.

### Tier Assignment

| Tier   | Budget signal              | Engagement length | Artifacts required                                    |
| ------ | -------------------------- | ----------------- | ----------------------------------------------------- |
| **T1** | > $5M/yr or SR 11-7 tiered | 6 weeks           | All 21                                                |
| **T2** | $500K–$5M/yr               | 4 weeks           | 1, 2, 3, 4, 5, 7, 8, 12, 13, 15, 16, 17, 20           |
| **T3** | < $500K/yr, low risk       | 2 weeks           | 1, 2, 4, 7, 8, 13                                     |

Record the tier on the project record in the app (`GET /api/projects/{id}` returns the tier field once set). This drives which artifacts show as **required** vs. **optional** in the Project Detail view.

### Portfolio Sequencing Rules

- **Never** start two engagements in the same LOB in the same week — you will burn the SME.
- Sequence T1 engagements so that Phase 3 measurement doesn't overlap with another T1's Phase 3 (data engineering contention).
- Cap active portfolio at 5 concurrent T1 + T2 for a single Consultant.

**Exit criteria for Phase 0:** Project accepted into portfolio with tier assigned. Business Owner, Product Owner, Technical Owner, Finance Partner, Risk/Compliance Partner all named. Sponsor confirms they will attend Kickoff.

---

## 5. Phase 1 — Engagement Kickoff (Week 0–1)

**Purpose:** Establish a shared, signed agreement on what you will model, what you will not, what success means, and who approves what.

**Primary artifact:** [Artifact 1 — Kickoff & Scope](../templates/Artifact_01_Kickoff_&_Scope.docx)

### What Artifact 1 must contain (all fields non-blank at end of Phase 1)

- Use case name, LOB, domain overlay
- Five named owners (Business, Product, Technical, Finance, Risk)
- Workload one-paragraph description — plain English, no jargon
- **In-scope components** (multi-select): Frontend/API, Orchestrator, Model(s)/endpoints, RAG pipeline, Vector DB, Evaluation harness, Observability/telemetry, Human-in-the-loop workflow, other
- **Out-of-scope components** — this is the field that saves you in Week 5. Write down every adjacent system that will not be part of the cost boundary. CRM integration, one-time data ingestion, executive dashboards, upstream data platform — spell them out.
- Environments (Dev/Test/Prod) and Regions/cloud accounts
- Data classification constraints (PII, PHI, PCI, GLBA scope, export controls)
- Success objectives across **five dimensions:** Cost, Performance (latency/SLA), Quality, Adoption, Governance
- Cost boundary paragraph — the definitive prose version of what's in and out
- Measurement approach — how you will collect data in Phase 3
- Target dates by phase — commit to specific weeks

### How to run the Kickoff meeting (2 hours)

1. **First 30 minutes — Owners in the room, in person or video-on.** Read the Purpose and Boundary sections of Artifact 1 aloud. Watch faces. Any surprise means you have not scoped it correctly.
2. **Next 45 minutes — Decompose to components (preview of Artifact 2).** Sketch the pipeline on a whiteboard. Every arrow implies a cost driver.
3. **Next 30 minutes — Success objectives.** Force numeric answers. "Faster" is not an objective. "P90 latency < 2.5s end-to-end" is.
4. **Final 15 minutes — Decision Log seeding.** Log the first three decisions from this meeting into Artifact 1's decision log with dates, owners, rationale, and links.

### Exit criteria

- Artifact 1 has zero blank fields.
- All five owners have signed (in the app: check `signoff` field).
- Decision log has ≥ 3 entries.
- Next-phase meeting is on the calendar.

### Common pitfalls

- **Skipping "out-of-scope."** You will build a $2M forecast, then Finance will ask why the CRM integration isn't in it. Have that answer in writing.
- **Using verbs like "improve" or "reduce."** These are not objectives. Force numeric targets in Artifact 1.
- **Sponsor not in the room.** Their delegate cannot commit. Postpone until the sponsor can attend.

---

## 6. Phase 2 — Decomposition & Boundary (Week 1–2)

**Purpose:** Turn the architecture into a set of measurable cost-impacting steps, then bound the cost model at the boundaries of that architecture with unit prices you can defend.

**Primary artifacts:**
- [Artifact 2 — Workload Decomposition & Architecture Notes](../templates/Artifact_02_Workload_Decomposition.docx)
- [Artifact 3 — Cost Boundary, Assumptions & Pricing Table](../templates/Artifact_03_Boundary_&_Pricing.docx)
- [Artifact 4 — Cost Driver Map](../templates/Artifact_04_Cost_Driver_Map.docx)

### When to use each

- **Artifact 2 first.** Draw the pipeline before you cost it. Every box and arrow becomes a candidate cost driver.
- **Artifact 4 second.** For every architectural component in Artifact 2, define the cost driver: input tokens? output tokens? retrievals? indexed documents? guardrail calls? Each driver gets a precise definition and a measurement signal.
- **Artifact 3 third.** Now you can freeze the unit prices — token prices, embedding prices, vector-DB storage/query prices, evaluation costs, HITL fully-loaded hourly. Assumptions get versioned; every change goes into the Decision Log.

### Sequencing note

You cannot write a defensible Artifact 3 without Artifact 2 and Artifact 4. If Finance is pressuring you to jump straight to a price sheet, resist. Prices attached to undefined drivers are theater.

### Artifact 2 quality bar

- Every architectural component is named with a **single owner** (person, not team).
- Every arrow (data flow) is labeled with **payload class** (PII/non-PII), **volume estimate**, and **latency budget**.
- HITL step is drawn explicitly if it exists. AI accountants forget HITL and then wonder why the cost model is off by 40%.
- Diagram lives in the artifact, not in Confluence. If it's in Confluence, embed the image.

### Artifact 4 quality bar

- Every driver has: definition, measurement signal (what event, what field, where logged), unit, and expected order of magnitude.
- **Sanity check:** if you multiplied every driver's unit price × expected volume, does it get you to a total in the right ballpark? If off by an order of magnitude, one of the drivers is wrong.
- Cross-check that every component in Artifact 2 appears in Artifact 4 and vice versa. No orphans.

### Artifact 3 quality bar

- Prices sourced from **actual invoices or published rate cards**, dated. "$0.003/1k tokens" is meaningless without which model and which date.
- Assumptions listed one per row with owner, source, and last-verified date.
- Currency, tax treatment, and discount tier explicit.
- Decision Log entry for every assumption change.

### Exit criteria

- Artifacts 2, 3, 4 approved by Technical Owner and Finance Partner.
- Drivers in Artifact 4 map 1:1 to instrumentation events planned for Artifact 5.
- Sanity check total is within ±25% of Sponsor's budget expectation, or a variance memo exists.

### Common pitfalls

- **One giant "LLM" line.** Split at least into input tokens, output tokens, retrieval (embedding + query), vector DB storage, evaluation, guardrails, HITL, and platform. Otherwise Artifact 10 will have nothing to optimize.
- **Assuming API list prices.** Enterprise discounts, committed-use pricing, and reserved capacity change the model materially. Get the actual rate card.
- **Ignoring egress and data movement.** For multi-region and hybrid, egress can be a top-5 line.

---

## 7. Phase 3 — Instrumentation & Measurement (Week 2–4)

**Purpose:** Stop guessing. Get real per-request data flowing into a place where Finance can query it and Product can dashboard it.

**Primary artifacts:**
- [Artifact 5 — Metering & Instrumentation Requirements](../templates/Artifact_05_Metering_&_Instrumentation.docx)
- [Artifact 6 — Pilot Measurement Plan (Sampling + Calibration)](../templates/Artifact_06_Pilot_Measurement_Plan.docx)

### When to use each

- **Artifact 5** during Week 2 — this is the specification the platform team implements. Do not wait for Artifact 8 to define instrumentation; you cannot forecast what you cannot measure.
- **Artifact 6** as soon as instrumentation lands in shadow or pilot traffic. Reconcile against invoice at end of first billing cycle.

### Artifact 5 must specify (per event/per request)

- `request_id`, `user_id_hash`, `session_id`, `route`, `model_id`, `prompt_version`, `retrieval_topk`, `input_tokens`, `output_tokens`, `cache_hit_flag`, `retrieval_latency_ms`, `total_latency_ms`, `guardrail_calls`, `outcome_flag` (success/failure/deflection), `hitl_flag`, `cost_estimate_usd` (client-side calculation as a check).
- Sampling policy: **100% for pilot, ≥ 10% for prod.** Sampling below 10% breaks Artifact 8 monthly variance analysis.
- Retention: raw events 90d, aggregates 3 years.
- PII handling: hashing rules, redaction requirements, do-not-log fields (see [§12](#12-domain-overlays) for domain-specific rules).

### Artifact 6 quality bar

- Sample size **statistically justified** — usually 380k+ requests across a full weekly cycle for a 95% CI at ±5% on unit cost.
- Volume sampling matches production **mix**, not uniform — weight by request type (short factual, long analytical, RAG-heavy, agentic).
- **Calibration procedure:** for one billing period, sum client-side `cost_estimate_usd` and compare to actual invoice. Target ≤ ±10% variance. If wider, one of Artifact 3's prices or Artifact 4's drivers is wrong. Fix and re-reconcile.
- Variance memo in Decision Log for any reconciliation outside ±10%.

### Exit criteria

- Instrumentation live in production (or in shadow if pre-launch).
- One full billing cycle reconciled within ±10%.
- Data accessible to Finance via query, not screenshot.

### Common pitfalls

- **Client-side token counting drift.** Model providers change tokenization. Reconcile monthly, not once.
- **Sampling below 10%.** Statistical power collapses. Finance loses confidence in variance analysis. Never below 10% in prod.
- **Failing to log cache hits.** You will over-forecast by 20-40% for any RAG workload if you don't track cache hit rate.

---

## 8. Phase 4 — Modeling: Unit Economics, Forecast, Scenarios (Week 3–5)

**Purpose:** Convert measured drivers into a defensible unit economics story, a monthly forecast Finance will use, and a scenario range that makes uncertainty explicit.

**Primary artifacts:**
- [Artifact 7 — AI Unit Economics Calculator](../templates/Artifact_07_Unit_Economics.docx)
- [Artifact 8 — AI Cost Forecast Model (Monthly, by Component)](../templates/Artifact_08_Cost_Forecast.docx)
- [Artifact 9 — Scenario Planning & Sensitivity](../templates/Artifact_09_Scenarios_&_Sensitivity.docx)

### When to use each

- **Artifact 7 first, always.** Cost per successful outcome is the number that survives executive review. If you don't have this, your business case is a total-spend story that any CFO can shoot down.
- **Artifact 8 second.** Forecast by component (inference, retrieval, vector DB, embeddings, eval, guardrails, HITL, platform) by month. Never present a single-total forecast.
- **Artifact 9 third.** Base + upside + downside, with **sensitivity** on the top 3 drivers.

### Artifact 7 must show

- Per-request cost by **request type** (short factual, long analytical, RAG-heavy, agentic — different types have wildly different costs).
- Per-**successful-outcome** cost = per-request cost × requests-per-outcome. This ratio is the single most important number in the engagement.
- Unit economics **trajectory** — Month 1 vs Month 6 vs Month 12. Adoption follows an S-curve; cost/outcome typically improves as the model of use matures and prompt engineering settles.
- Comparison to **best alternative** (do-nothing baseline, existing rules-based automation, human-only baseline). If cost/outcome isn't below the alternative, you don't have a business case.

### Artifact 8 must show

- Monthly cost for 12–24 months, split by 8 components.
- Volume assumptions from Artifact 6 or from business's own volume forecast — with source.
- Inclusion rules stated on the face of the forecast: pilot exclusion? dev/test exclusion? one-time vs. run-rate?
- Reconciliation column: month-1 forecast vs. month-1 actual bill, once available.

### Artifact 9 must show

- **Base case** with mean assumptions.
- **Upside case** with more favorable pricing, higher cache hit, better prompt design.
- **Downside case** with adoption faster than expected (volume up), pricing worse than expected, and one plausible operational shock.
- **Tornado diagram** or ranked table showing which 3 drivers move the answer most.
- **Break-even lines** on the top 3 drivers.

### Exit criteria

- Cost per successful outcome is a single sentence you can say from memory.
- Forecast is componentized and reconciles to Artifact 6.
- Scenarios show the range and identify the top 3 sensitivities.

### Common pitfalls

- **Reporting a monthly total without components.** You cannot optimize what you have not decomposed.
- **Modeling linear volume growth.** Real adoption is an S-curve. Downside case must include faster-than-linear ramp for popular use cases.
- **Ignoring HITL cost.** For any high-stakes workflow, HITL is often > 30% of total cost. Treat it as a first-class component.

---

## 9. Phase 5 — Optimization & Benefits (Week 4–5)

**Purpose:** Turn the cost model into an action plan. Turn the outcome model into an honest benefits statement.

**Primary artifacts:**
- [Artifact 10 — Optimization Options Catalog](../templates/Artifact_10_Optimization_Catalog.docx)
- [Artifact 11 — Benefits Value Calculator (Incremental & Attributable)](../templates/Artifact_11_Benefits_Calculator.docx)

### When to use each

- **Artifact 10** once Artifact 8 shows which component dominates. Optimize the top 2 components; ignore the bottom 4.
- **Artifact 11** in parallel — Finance will not sign the business case without an attributable-benefits page.

### Artifact 10 catalog structure

For each optimization, record:

| Field                       | Notes                                                                                     |
| --------------------------- | ----------------------------------------------------------------------------------------- |
| Lever name                  | e.g., "Cache high-frequency prompts," "Route short queries to smaller model"              |
| Target component            | Inference / Retrieval / Vector DB / Embeddings / Eval / Guardrails / HITL / Platform      |
| Expected % reduction        | Range, based on measured driver signal                                                    |
| Effort                      | S / M / L in engineer-weeks                                                               |
| Risk (quality/latency)      | What could get worse                                                                      |
| Prerequisites               | e.g., "requires prompt versioning in Artifact 20"                                         |
| Owner                       | Named person                                                                              |
| Status                      | Proposed / In progress / Live / Rejected                                                  |

**Rule:** Do not accept a lever without a measurement plan proving it worked. Every accepted lever must feed back into Artifact 8's next reconciliation.

### Common lever families to always consider

1. **Model routing.** Send short factual queries to a smaller/cheaper model. Save large models for genuinely hard requests.
2. **Prompt caching.** Provider-level (Anthropic, OpenAI, Bedrock) and app-level caching of common prefixes.
3. **Retrieval tuning.** Top-k reduction, chunk size optimization, re-ranking to cut candidates before expensive scoring.
4. **Batch embeddings.** Ingest-time embeddings are cheaper batched than streamed.
5. **Guardrail consolidation.** Combine input classification + output redaction + PII scrub into one call where possible.
6. **HITL sampling.** Reduce HITL from 100% to risk-tiered sampling (100% high-risk, 20% medium, 5% low). Requires Artifact 15 sign-off.
7. **Reserved capacity.** For predictable steady-state workloads, committed-use discounts often 30-50%.

### Artifact 11 must distinguish

- **Gross benefit** — what happens with the AI in place.
- **Attributable benefit** — what would not have happened without it. This is the number that goes in ROI.
- **Baseline** — human-only, rules-only, or do-nothing baseline explicitly documented.

**Rule:** No benefit counts unless (a) it maps to a KPI Finance already tracks and (b) it survives the "would this have happened anyway?" test.

### Exit criteria

- Optimization catalog with ≥ 6 levers, each with quantified impact and owner.
- Benefits calculator with attributable benefit signed by Business Owner.
- At least one lever is already in progress or live.

### Common pitfalls

- **Claiming productivity gains without a baseline study.** Finance will discount the ROI to zero. Include a measurement plan for the productivity claim in Artifact 6.
- **Ignoring quality/latency trade-offs.** A lever that saves 30% but breaks P90 latency is not a lever. Log it as rejected with rationale.
- **Optimizing the smallest component.** If HITL is 40% of cost, tuning the vector DB from 3% to 2.4% saves nothing worth doing.

---

## 10. Phase 6 — Business Case & Governance Handoff (Week 5–6)

**Purpose:** Deliver a decision-ready package. The exec committee decides scale/hold/kill from these five artifacts.

**Primary artifacts:**
- [Artifact 12 — ROI / NPV Model](../templates/Artifact_12_ROI_-_NPV.docx)
- [Artifact 13 — Executive One-Pager (Business Case)](../templates/Artifact_13_Exec_One-Pager.docx)
- [Artifact 14 — Full Business Case Narrative](../templates/Artifact_14_Business_Case_Narrative.docx)
- [Artifact 15 — Risk Register & Controls Checklist](../templates/Artifact_15_Risk_&_Controls.docx)
- [Artifact 16 — Evaluation & Quality Gate](../templates/Artifact_16_Evaluation_&_Quality.docx)

### When to use each

- **Artifact 12** consolidates Artifacts 8, 9, and 11 into NPV, IRR (optional), payback, and sensitivity.
- **Artifact 13** is the one page the exec committee reads. Everything else backs it up.
- **Artifact 14** is the auditable narrative. Governance and Internal Audit read this one.
- **Artifact 15** is the operational-risk sign-off. Risk Committee owns this one.
- **Artifact 16** is the quality-gate sign-off. Product + Risk co-own.

### Sequencing note

- Draft Artifacts 12 and 14 first (they have the most content).
- Distill Artifact 13 from them last — the one-pager is the hardest artifact because it forces prioritization.
- Artifacts 15 and 16 can run in parallel with 12/14 if you have Risk and Product engaged.

### Artifact 12 quality bar

- 12- or 24-month NPV at company hurdle rate (default 10%, confirm with Finance Partner).
- Payback in months.
- Sensitivity table: NPV at ±20% on top 3 drivers from Artifact 9.
- Explicit inclusion of one-time vs. run-rate costs and benefits.
- "Do nothing" alternative NPV shown alongside.

### Artifact 13 must contain (one page, no exceptions)

1. Use case in one sentence.
2. Cost per successful outcome and the alternative it beats.
3. Year-1 cost, Year-2 cost, 3-year NPV, payback.
4. Top 3 risks and their mitigations (from Artifact 15).
5. Adoption target and how you'll measure it (from Artifacts 1, 6).
6. The decision requested. Not "approve budget" — "approve $X for months Y-Z at tier T."

### Artifact 14 must contain

- Executive summary (drawn from Artifact 13).
- Business context and outcome.
- Solution overview and architecture (drawn from Artifact 2).
- Cost, benefits, and ROI (drawn from 8, 11, 12).
- Risks and controls (drawn from 15).
- Adoption and change management plan.
- Governance and operating model (drawn from 17 preview).
- Decision requested with alternatives considered.

### Artifact 15 quality bar

- Risk register organized by type (model risk, operational risk, compliance risk, third-party risk, data risk).
- Each risk: description, likelihood, impact, inherent rating, controls, residual rating, owner, review cadence.
- For regulated LOBs, explicitly map to the applicable framework (see [§12](#12-domain-overlays)).
- Independent second-line reviewer signature required for banking, healthcare, and public-sector projects.

### Artifact 16 quality bar

- Quality gates defined **before** they can be tuned to whatever the model happens to score.
- Ground-truth set size ≥ 500, with domain expert labeling.
- Reject rate, retry rate, guardrail-trigger rate, HITL escalation rate — with thresholds.
- Regression test procedure for every model/prompt version change.

### Exit criteria

- Exec committee decision recorded in Artifact 1 Decision Log.
- If approved: scale plan in place (Phase 7).
- If held: what would need to be true to approve — written.
- If killed: postmortem and knowledge capture to portfolio wiki.

### Common pitfalls

- **Artifact 13 becoming Artifact 14 in miniature.** The one-pager is a decision instrument, not a compression of everything. Cut ruthlessly.
- **NPV without payback.** Exec committees look at payback first. Show both.
- **Skipping the "do nothing" baseline.** Every business case has an implicit alternative. Make it explicit or the exec committee will pick it silently.

---

## 11. Phase 7 — Operate & Steady State (Ongoing)

**Purpose:** Sustainable governance. The consultant leaves; the framework stays.

**Primary artifacts:**
- [Artifact 17 — Cost Management Operating Model (RACI + Cadence)](../templates/Artifact_17_Operating_Model.docx)
- [Artifact 18 — Chargeback / Showback Allocation](../templates/Artifact_18_Chargeback_-_Showback.docx)
- [Artifact 19 — Vendor & Pricing Negotiation Tracker](../templates/Artifact_19_Vendor_Tracker.docx)
- [Artifact 20 — Data Dictionary](../templates/Artifact_20_Data_Dictionary.docx)
- [Artifact 21 — Cost Anomaly Playbook](../templates/Artifact_21_Anomaly_Playbook.docx)

### When to use each

- **Artifact 17** at handoff. Defines who does what at what cadence, forever.
- **Artifact 18** goes live at first full billing cycle post-scale.
- **Artifact 19** is a living document — every negotiation, every price change, every commit.
- **Artifact 20** is the shared vocabulary. Field definitions, allowed values, computation rules.
- **Artifact 21** is the on-call runbook when the bill spikes.

### Artifact 17 must define

- **RACI** across Product, Finance, Platform, Risk, Security for: forecasting, month-end close, variance analysis, model change approval, cost anomaly response, quarterly business review.
- **Cadences:**
  - Daily: cost anomaly dashboard review by platform on-call
  - Weekly: unit-economics review by Product + Finance
  - Monthly: close + variance memo by Finance
  - Quarterly: portfolio review with LOB leadership + optimization catalog refresh
- **Escalation path:** when does an anomaly become an executive escalation.

### Artifact 18 must define

- Allocation dimensions: LOB, cost center, product, environment.
- Allocation method: direct usage (preferred) vs. usage-proxy vs. flat allocation. Direct usage requires Artifact 5 tags. Usage-proxy requires a documented driver.
- Showback vs. chargeback: start showback for two quarters, then chargeback once trust is established.
- Dispute resolution procedure: what happens when a cost center disputes a bill. Named arbiter.

### Artifact 19 must track

- Vendor, product, contract term, list price, discount tier, effective price, commitment level, renewal date.
- Negotiation history: date, ask, counter, outcome, next-step owner.
- Alternatives evaluated at last renewal — even if not selected. Optionality is leverage.

### Artifact 20 must standardize

- Every field name used in Artifacts 5, 6, 7, 8 — one canonical definition each.
- Allowed values (enums) for status, request_type, outcome_flag, environment, region.
- Derived-field computation rules (e.g., "cost per successful outcome = sum(cost_estimate_usd) / count(outcome_flag='success')").
- Owner per definition.

### Artifact 21 must standardize

- Triage checklist when the daily cost dashboard shows > 20% deviation from run rate.
- First 30 minutes: check volume, check price change, check bug (retry loop, prompt regression).
- First 2 hours: identify component (which of the 8), pull sample requests, compare to Artifact 8 forecast.
- First 24 hours: root cause, remediation, decision on rollback vs. patch, notification.
- Postmortem template: what changed, when, blast radius, action items.

### Exit criteria (for consultant handoff)

- Owners for 17, 18, 19, 20, 21 named and trained.
- First monthly close completed on time with the new operating model.
- First anomaly (real or simulated) worked through Artifact 21 process.

### Common pitfalls

- **Chargeback before trust.** Cost centers will fight your allocation forever. Run showback for 6 months to prove the numbers, then move to chargeback.
- **Anomaly playbook only used after a real incident.** Simulate one before you leave.
- **Operating model owned by "everyone."** If everyone owns it, no one owns it. Name a single accountable executive per cadence.

---

## 12. Domain Overlays

The methodology is domain-agnostic; the controls layered on top depend on the industry. Every artifact in the app has a `domain_overlay_note` field that surfaces the applicable overlay guidance.

| Domain               | Overlay applies to                                                                                                                    | Key additional artifacts / signoffs                                                                                                             |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| **Generic**          | Baseline for enterprise use with no additional regulatory overlay.                                                                    | Standard 21-artifact pack.                                                                                                                      |
| **Banking / FSI**    | Any use case handling PII, GLBA-covered data, or SR 11-7 tiered model risk.                                                            | Independent second-line validation in [Artifact 15](../templates/Artifact_15_Risk_&_Controls.docx). Model-risk tiering explicit in [Artifact 1](../templates/Artifact_01_Kickoff_&_Scope.docx). Data-use committee in signoff. |
| **Retail**           | Peak-season variability (Black Friday, back-to-school). High-volume, thin-margin.                                                     | Peak-season overlay row in [Artifact 8](../templates/Artifact_08_Cost_Forecast.docx). Higher variance tolerance in [Artifact 6](../templates/Artifact_06_Pilot_Measurement_Plan.docx). |
| **Energy / Oil & Gas** | Remote sites, egress costs, hybrid/edge deployments, HSE stakes.                                                                     | Remote-site egress line in [Artifact 8](../templates/Artifact_08_Cost_Forecast.docx). HSE risk category in [Artifact 15](../templates/Artifact_15_Risk_&_Controls.docx). |
| **Aerospace / Defense** | ITAR/EAR export controls, configuration management, DO-178 / DO-326 adjacencies.                                                    | Config-management overhead in [Artifact 8](../templates/Artifact_08_Cost_Forecast.docx). Export-control review in [Artifact 15](../templates/Artifact_15_Risk_&_Controls.docx).           |
| **Public Sector**    | FedRAMP boundary, ATO maintenance, FISMA scope, procurement rules.                                                                     | ATO-maintenance and audit-support lines in [Artifact 8](../templates/Artifact_08_Cost_Forecast.docx). Explicit FedRAMP boundary in [Artifact 3](../templates/Artifact_03_Boundary_&_Pricing.docx). |
| **Telecom**          | Multi-region infrastructure duplication, low-latency requirements, carrier-grade uptime.                                              | Multi-region duplication line in [Artifact 8](../templates/Artifact_08_Cost_Forecast.docx). Higher SLA in [Artifact 1](../templates/Artifact_01_Kickoff_&_Scope.docx). |
| **Media / Entertainment** | Rights verification, content moderation stakes, spiky demand.                                                                    | Rights-verification cost line in [Artifact 8](../templates/Artifact_08_Cost_Forecast.docx). Content-moderation gates in [Artifact 16](../templates/Artifact_16_Evaluation_&_Quality.docx). |

The app's Artifact Editor surfaces the overlay note automatically for each project's selected domain. To add a new domain (e.g., healthcare), see the "Adding a new domain" section of [`../README.md`](../README.md).

---

## 13. Common Failure Modes and How to Avoid Them

Every failure mode below has cost a real engagement time and credibility.

| Failure Mode                                                    | Symptom                                                             | Where in methodology                                            | How to avoid                                                                                          |
| --------------------------------------------------------------- | ------------------------------------------------------------------- | --------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| Skipping Phase 3, forecasting from vendor rate cards            | Monthly variance > 30% for the first quarter                        | Phase 3 (Artifacts 5, 6)                                        | Refuse to publish Artifact 8 until Artifact 6 has reconciled ±10%.                                    |
| One-line "AI cost" in Artifact 8                                | Cannot answer "which component drove the increase?"                 | Phase 4 (Artifact 8)                                            | Componentize forecast — 8 rows minimum.                                                               |
| Total-spend business case, no unit economics                    | Exec committee sends you back for more analysis                     | Phase 4 (Artifact 7)                                            | Lead with cost per successful outcome. Total-spend is a supporting number, not the headline.          |
| Benefits without attribution                                    | Finance discounts ROI to 30% of claimed                             | Phase 5 (Artifact 11)                                           | Explicit baseline. "Would this have happened anyway?" test on every benefit line.                     |
| Governance retrofit in Phase 6                                  | Risk committee blocks scale                                         | Phase 1 (Artifact 15 preview)                                   | Start Artifact 15 in Phase 1 and update through phases.                                               |
| Consultant becomes the operating model                          | Framework decays the week after consultant leaves                    | Phase 7 (Artifact 17)                                           | Name owners in Phase 1. Have them draft Artifact 17, not you.                                         |
| Chargeback before trust                                         | Cost centers dispute every allocation                                | Phase 7 (Artifact 18)                                           | Showback for 6 months first. Move to chargeback only after 3 clean monthly closes.                    |
| Optimization catalog with no owners                             | Levers stay "proposed" for a year                                    | Phase 5 (Artifact 10)                                           | Every lever gets an owner and a target month before it goes on the catalog.                           |
| Cache miss in the forecast                                      | Over-forecast by 20-40% on RAG workloads                             | Phase 3 (Artifact 5)                                            | Log `cache_hit_flag` on every request. Reconcile monthly.                                              |
| HITL ignored                                                    | Business case optimistic by 30% because reviewer time uncounted      | Phase 2 (Artifact 4)                                            | Explicitly draw HITL in Artifact 2. Count HITL as a first-class component in Artifact 4 and 8.        |
| Volume forecast is linear                                       | Downside case not credible; adoption spike breaks budget mid-year    | Phase 4 (Artifact 8, 9)                                         | S-curve for volume. Downside includes faster-than-expected ramp.                                       |
| One person owns everything                                      | Everything stalls when they take vacation                             | All phases                                                      | Every artifact has a distinct owner. Consultant is editor of record, not owner.                       |
| Anomaly playbook untested                                       | First real incident becomes an all-hands scramble                    | Phase 7 (Artifact 21)                                           | Simulate one before handoff. Time it. Iterate the runbook.                                            |

---

## 14. Governance Cadence Cheatsheet

Once the operating model is live (from [Artifact 17](../templates/Artifact_17_Operating_Model.docx)):

| Cadence   | Who                                    | What                                                                          | Backing artifacts                                          |
| --------- | -------------------------------------- | ----------------------------------------------------------------------------- | ---------------------------------------------------------- |
| Daily     | Platform on-call                       | Cost-anomaly dashboard review; run Artifact 21 if > 20% deviation             | [Artifact 21](../templates/Artifact_21_Anomaly_Playbook.docx) |
| Weekly    | Product + Finance                      | Unit-economics review; adoption trends; guardrail-trigger and reject rates    | [Artifact 7](../templates/Artifact_07_Unit_Economics.docx), [Artifact 16](../templates/Artifact_16_Evaluation_&_Quality.docx) |
| Monthly   | Finance (lead) + Product + Technical   | Close, reconcile Artifact 8 vs. invoice, publish variance memo                 | [Artifact 6](../templates/Artifact_06_Pilot_Measurement_Plan.docx), [Artifact 8](../templates/Artifact_08_Cost_Forecast.docx), [Artifact 18](../templates/Artifact_18_Chargeback_-_Showback.docx) |
| Quarterly | LOB leadership + cost management triad          | Portfolio review; refresh optimization catalog; renegotiation checkpoints     | [Artifact 10](../templates/Artifact_10_Optimization_Catalog.docx), [Artifact 19](../templates/Artifact_19_Vendor_Tracker.docx) |
| Annual    | Executive committee                    | Framework refresh; assumption re-baseline; portfolio prioritization           | Full pack, especially [Artifact 3](../templates/Artifact_03_Boundary_&_Pricing.docx), [Artifact 12](../templates/Artifact_12_ROI_-_NPV.docx), [Artifact 17](../templates/Artifact_17_Operating_Model.docx) |

---

## 15. Appendix — Artifact Index

Full list with phase, purpose, and link. The app's Artifact Reference view is the interactive version of this table.

| #   | Phase | Artifact | Primary Owner | Purpose in one line |
| --- | ----- | -------- | ------------- | ------------------- |
| 01  | 1 | [Engagement Kickoff & Scope](../templates/Artifact_01_Kickoff_&_Scope.docx) | Product | Signed shared agreement on what you will model, boundary, and success. |
| 02  | 2 | [Workload Decomposition & Architecture Notes](../templates/Artifact_02_Workload_Decomposition.docx) | Technical | Turn architecture into a set of measurable cost-impacting steps. |
| 03  | 2 | [Cost Boundary, Assumptions & Pricing Table](../templates/Artifact_03_Boundary_&_Pricing.docx) | Finance | Make the cost model defensible with stated assumptions and unit prices. |
| 04  | 2 | [Cost Driver Map](../templates/Artifact_04_Cost_Driver_Map.docx) | Technical | Backbone linking each driver to a precise definition, signal, and unit cost. |
| 05  | 3 | [Metering & Instrumentation Requirements](../templates/Artifact_05_Metering_&_Instrumentation.docx) | Technical | Ensure you can actually measure the drivers you modeled. |
| 06  | 3 | [Pilot Measurement Plan (Sampling + Calibration)](../templates/Artifact_06_Pilot_Measurement_Plan.docx) | Technical + Finance | Sample volume, request mix, and calibrate against invoice. |
| 07  | 4 | [AI Unit Economics Calculator](../templates/Artifact_07_Unit_Economics.docx) | Finance + Product | Cost per request and per successful outcome. The number that survives review. |
| 08  | 4 | [AI Cost Forecast Model (Monthly, by Component)](../templates/Artifact_08_Cost_Forecast.docx) | Finance | Monthly forecast Finance can trace and auditors can reconcile. |
| 09  | 4 | [Scenario Planning & Sensitivity](../templates/Artifact_09_Scenarios_&_Sensitivity.docx) | Finance + Product | Translate uncertainty into decision options with sensitivity ranking. |
| 10  | 5 | [Optimization Options Catalog](../templates/Artifact_10_Optimization_Catalog.docx) | Product + Technical | Actionable levers with quantified impact and named owners. |
| 11  | 5 | [Benefits Value Calculator (Incremental & Attributable)](../templates/Artifact_11_Benefits_Calculator.docx) | Business + Finance | Honest attributable benefits. What would not have happened without this. |
| 12  | 6 | [ROI / NPV Model](../templates/Artifact_12_ROI_-_NPV.docx) | Finance | NPV, payback, and sensitivity — transparent. |
| 13  | 6 | [Executive One-Pager (Business Case)](../templates/Artifact_13_Exec_One-Pager.docx) | Product + Business | The one page the exec committee reads to decide. |
| 14  | 6 | [Full Business Case Narrative](../templates/Artifact_14_Business_Case_Narrative.docx) | Business + Consultant | Auditable narrative for governance and internal audit. |
| 15  | 1–6 (running) | [Risk Register & Controls Checklist](../templates/Artifact_15_Risk_&_Controls.docx) | Risk/Compliance | Operational, model, third-party, compliance, and data risks with controls. |
| 16  | 6 (running) | [Evaluation & Quality Gate](../templates/Artifact_16_Evaluation_&_Quality.docx) | Product + Risk | Quality gates that drive retry rates, output length, escalations — and therefore cost. |
| 17  | 7 | [Cost Management Operating Model (RACI + Cadence)](../templates/Artifact_17_Operating_Model.docx) | Business + Finance | Sustainable cost management after the consultant phase. |
| 18  | 7 | [Chargeback / Showback Allocation](../templates/Artifact_18_Chargeback_-_Showback.docx) | Finance | Allocate AI spend to cost centers in a way that aligns incentives. |
| 19  | 7 | [Vendor & Pricing Negotiation Tracker](../templates/Artifact_19_Vendor_Tracker.docx) | Finance + Procurement | Track vendor pricing, terms, and negotiation status over time. |
| 20  | 7 | [Data Dictionary](../templates/Artifact_20_Data_Dictionary.docx) | Technical | Audit-ready dictionary of every field used across the pack. |
| 21  | 7 | [Cost Anomaly Playbook](../templates/Artifact_21_Anomaly_Playbook.docx) | Platform + Finance | Standing triage steps for cost anomalies. |

---

## How to use this document

**On a new engagement:**

1. Read Sections 1–3 top to bottom.
2. Read the section for the phase you're currently in.
3. Open the artifact templates linked in that phase and copy them into the app (or generate filled DOCX from the app's Artifact Editor).
4. Follow the quality bars and exit criteria to know when you're done with a phase.

**On an existing engagement mid-flight:**

- Find the current phase in Section 3, jump to that phase's section, and check exit criteria. If any are not met, that's your next work.

**On a portfolio review:**

- Section 14 (Governance Cadences) is the operating rhythm.
- Section 13 (Failure Modes) is the checklist for what's likely going wrong.

**When onboarding a new AI Solutions Consultant:**

- Sections 1, 2, 3, and 13 in the first day.
- One artifact per day for the next 21 days, using the app's Artifact Reference view.
- Shadow a live engagement for one full phase before leading independently.

---

*This methodology is a living document. Improvements go through pull request. Record every material change in the Decision Log of the affected engagement and in the [`../README.md`](../README.md) changelog.*
