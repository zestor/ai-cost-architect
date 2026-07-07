// AI Cost Architect — canonical artifact + phase data
// Used by the interactive picker and search on the home page.

window.ACA = window.ACA || {};

window.ACA.phases = [
  { num: 0, key: "intake",           name: "Portfolio Intake",             weeks: "Pre-week",  purpose: "Decide whether to take the project and at what tier.",
    exit: "Project accepted with tier assigned. Five named owners. Sponsor confirmed for kickoff." },
  { num: 1, key: "kickoff",          name: "Engagement Kickoff",           weeks: "Week 0–1",  purpose: "Establish a signed, shared scope with named owners.",
    exit: "Artifact 1 has zero blank fields. All five owners have signed. Decision log has ≥ 3 entries." },
  { num: 2, key: "decomposition",    name: "Decomposition & Boundary",     weeks: "Week 1–2",  purpose: "Turn architecture into measurable steps with a defensible cost boundary.",
    exit: "Artifacts 2, 3, 4 approved. Drivers map 1:1 to instrumentation plan." },
  { num: 3, key: "instrumentation",  name: "Instrumentation & Measurement", weeks: "Week 2–4",  purpose: "Get real per-request cost data flowing into a queryable store.",
    exit: "Instrumentation live in prod. One billing cycle reconciled within ±10%." },
  { num: 4, key: "modeling",         name: "Modeling",                     weeks: "Week 3–5",  purpose: "Build unit economics, componentized forecast, and scenarios.",
    exit: "Cost/successful-outcome stated in one sentence. Forecast reconciles. Top 3 sensitivities identified." },
  { num: 5, key: "optimization",     name: "Optimization & Benefits",      weeks: "Week 4–5",  purpose: "Turn cost model into an action plan and honest attributable benefits.",
    exit: "≥ 6 quantified levers with owners. Attributable benefit signed by Business Owner." },
  { num: 6, key: "business_case",    name: "Business Case & Governance",   weeks: "Week 5–6",  purpose: "Deliver a decision-ready package for the executive committee.",
    exit: "Exec committee decision recorded in the Artifact 1 Decision Log." },
  { num: 7, key: "operate",          name: "Operate & Steady State",       weeks: "Ongoing",   purpose: "Sustainable governance after the consultant leaves.",
    exit: "First monthly close on time with the new operating model. Anomaly playbook rehearsed." }
];

window.ACA.artifacts = [
  { id: "A01", num: 1,  slug: "kickoff-scope",              phase: 1, owner: "Product",
    file: "Artifact_01_Kickoff_&_Scope.docx",
    title: "Engagement Kickoff & Scope",
    purpose: "Create a shared, auditable agreement on what you will model, what you will not, what success means, and who approves decisions. Every downstream artifact inherits its boundaries from here.",
    when: "Immediately at engagement start (Week 0–1). Re-open only when scope materially changes; then log the change in the Decision Log with a new revision number.",
    tiers: { T1: "required", T2: "required", T3: "required" }
  },
  { id: "A02", num: 2,  slug: "workload-decomposition",     phase: 2, owner: "Technical",
    file: "Artifact_02_Workload_Decomposition.docx",
    title: "Workload Decomposition & Architecture Notes",
    purpose: "Turn architecture into measurable, cost-impacting steps. Every box and arrow becomes a candidate cost driver.",
    when: "Week 1. Before you touch a cost model. HITL must be drawn explicitly.",
    tiers: { T1: "required", T2: "required", T3: "required" }
  },
  { id: "A03", num: 3,  slug: "boundary-pricing",           phase: 2, owner: "Finance",
    file: "Artifact_03_Boundary_&_Pricing.docx",
    title: "Cost Boundary, Assumptions & Pricing Table",
    purpose: "Make the cost model defensible by stating assumptions and unit prices in one place. Prices from actual invoices or dated rate cards.",
    when: "Week 1–2, after Artifact 2 and 4 exist. Never write prices before drivers.",
    tiers: { T1: "required", T2: "required", T3: "optional" }
  },
  { id: "A04", num: 4,  slug: "cost-driver-map",            phase: 2, owner: "Technical",
    file: "Artifact_04_Cost_Driver_Map.docx",
    title: "Cost Driver Map",
    purpose: "Backbone table linking each cost driver to a precise definition, measurement signal, and unit cost. No component in Artifact 2 may lack a driver row here.",
    when: "Week 1–2, immediately after Artifact 2.",
    tiers: { T1: "required", T2: "required", T3: "required" }
  },
  { id: "A05", num: 5,  slug: "metering-instrumentation",   phase: 3, owner: "Technical",
    file: "Artifact_05_Metering_&_Instrumentation.docx",
    title: "Metering & Instrumentation Requirements",
    purpose: "Ensure you can actually measure the drivers you modeled. Specifies per-request events, sampling policy, retention, and PII handling.",
    when: "Week 2. Do NOT wait for the forecast to define instrumentation.",
    tiers: { T1: "required", T2: "required", T3: "optional" }
  },
  { id: "A06", num: 6,  slug: "pilot-measurement-plan",     phase: 3, owner: "Technical + Finance",
    file: "Artifact_06_Pilot_Measurement_Plan.docx",
    title: "Pilot Measurement Plan (Sampling + Calibration)",
    purpose: "Calibrate averages, distributions, and reconcile client-side cost estimates to actual invoice within ±10%.",
    when: "Week 3, as soon as instrumentation is live in shadow or pilot.",
    tiers: { T1: "required", T2: "required", T3: "optional" }
  },
  { id: "A07", num: 7,  slug: "unit-economics",             phase: 4, owner: "Finance + Product",
    file: "Artifact_07_Unit_Economics.docx",
    title: "AI Unit Economics Calculator",
    purpose: "Compute per-request and per-successful-outcome cost by request type. Cost per outcome is the number that survives executive review.",
    when: "Week 3–4, once Artifact 6 has yielded reconciled data.",
    tiers: { T1: "required", T2: "required", T3: "required" }
  },
  { id: "A08", num: 8,  slug: "cost-forecast",              phase: 4, owner: "Finance",
    file: "Artifact_08_Cost_Forecast.docx",
    title: "AI Cost Forecast Model (Monthly, by Component)",
    purpose: "Produce a monthly forecast finance can trace and auditors can reconcile. Never one line — always 8 components.",
    when: "Week 4, immediately after Artifact 7.",
    tiers: { T1: "required", T2: "required", T3: "required" }
  },
  { id: "A09", num: 9,  slug: "scenarios-sensitivity",      phase: 4, owner: "Finance + Product",
    file: "Artifact_09_Scenarios_&_Sensitivity.docx",
    title: "Scenario Planning & Sensitivity",
    purpose: "Translate uncertainty into decision options. Base + upside + downside, tornado on top 3 drivers, break-even lines.",
    when: "Week 4–5, immediately after Artifact 8.",
    tiers: { T1: "required", T2: "optional", T3: "optional" }
  },
  { id: "A10", num: 10, slug: "optimization-catalog",       phase: 5, owner: "Product + Technical",
    file: "Artifact_10_Optimization_Catalog.docx",
    title: "Optimization Options Catalog",
    purpose: "Turn analysis into actionable levers with quantified impact, effort, risk, and named owners. Only optimize top-2 cost components.",
    when: "Week 4–5, once Artifact 8 has identified dominant components.",
    tiers: { T1: "required", T2: "optional", T3: "optional" }
  },
  { id: "A11", num: 11, slug: "benefits-calculator",        phase: 5, owner: "Business + Finance",
    file: "Artifact_11_Benefits_Calculator.docx",
    title: "Benefits Value Calculator (Incremental & Attributable)",
    purpose: "Ensure ROI does not assume benefits that would not have happened otherwise. Attributable-only benefits with signed baseline.",
    when: "Week 4–5, in parallel with Artifact 10.",
    tiers: { T1: "required", T2: "optional", T3: "optional" }
  },
  { id: "A12", num: 12, slug: "roi-npv",                    phase: 6, owner: "Finance",
    file: "Artifact_12_ROI_-_NPV.docx",
    title: "ROI / NPV Model",
    purpose: "Compute NPV, IRR (optional), payback, and show sensitivity transparently. Include the 'do-nothing' NPV alongside.",
    when: "Week 5, after Artifacts 8, 9, 11 are frozen.",
    tiers: { T1: "required", T2: "required", T3: "required" }
  },
  { id: "A13", num: 13, slug: "exec-one-pager",             phase: 6, owner: "Product + Business",
    file: "Artifact_13_Exec_One-Pager.docx",
    title: "Executive One-Pager (Business Case)",
    purpose: "A concise decision document. The one page the executive committee actually reads.",
    when: "Week 5–6, distilled last from Artifacts 12 and 14.",
    tiers: { T1: "required", T2: "required", T3: "required" }
  },
  { id: "A14", num: 14, slug: "business-case-narrative",    phase: 6, owner: "Business + Consultant",
    file: "Artifact_14_Business_Case_Narrative.docx",
    title: "Full Business Case Narrative",
    purpose: "Support governance committees with a thorough, auditable narrative that internal audit can follow.",
    when: "Week 5–6, drafted in parallel with Artifact 12.",
    tiers: { T1: "required", T2: "optional", T3: "optional" }
  },
  { id: "A15", num: 15, slug: "risk-controls",              phase: 6, owner: "Risk/Compliance",
    file: "Artifact_15_Risk_&_Controls.docx",
    title: "Risk Register & Controls Checklist",
    purpose: "Prove the business case accounts for operational, model, third-party, compliance, and data risks that affect cost and quality.",
    when: "Start in Phase 1 and update through phases. Frozen at end of Phase 6.",
    tiers: { T1: "required", T2: "required", T3: "optional" }
  },
  { id: "A16", num: 16, slug: "evaluation-quality",         phase: 6, owner: "Product + Risk",
    file: "Artifact_16_Evaluation_&_Quality.docx",
    title: "Evaluation & Quality Gate",
    purpose: "Define quality gates that influence retry rates, output length, escalations — and therefore cost. Gates set BEFORE tuning.",
    when: "Draft in Phase 4, freeze in Phase 6.",
    tiers: { T1: "required", T2: "required", T3: "optional" }
  },
  { id: "A17", num: 17, slug: "operating-model",            phase: 7, owner: "Business + Finance",
    file: "Artifact_17_Operating_Model.docx",
    title: "Cost Management Operating Model (RACI + Cadence)",
    purpose: "Make cost management sustainable and repeatable after the consultant phase. Names owners for daily/weekly/monthly/quarterly cadences.",
    when: "Phase 6 draft, Phase 7 go-live. Names owned before consultant leaves.",
    tiers: { T1: "required", T2: "required", T3: "optional" }
  },
  { id: "A18", num: 18, slug: "chargeback-showback",        phase: 7, owner: "Finance",
    file: "Artifact_18_Chargeback_-_Showback.docx",
    title: "Chargeback / Showback Allocation",
    purpose: "Allocate AI spend to cost centers in a way that aligns incentives. Start showback for 2 quarters; move to chargeback once trust is established.",
    when: "Phase 7 kickoff, at first full billing cycle post-scale.",
    tiers: { T1: "required", T2: "optional", T3: "optional" }
  },
  { id: "A19", num: 19, slug: "vendor-tracker",             phase: 7, owner: "Finance + Procurement",
    file: "Artifact_19_Vendor_Tracker.docx",
    title: "Vendor & Pricing Negotiation Tracker",
    purpose: "Track vendor pricing, terms, negotiation history, and alternatives evaluated at each renewal. Optionality is leverage.",
    when: "Phase 7 and permanent. Update on every contract event.",
    tiers: { T1: "required", T2: "optional", T3: "optional" }
  },
  { id: "A20", num: 20, slug: "data-dictionary",            phase: 7, owner: "Technical",
    file: "Artifact_20_Data_Dictionary.docx",
    title: "Data Dictionary",
    purpose: "Provide an audit-ready dictionary of all data fields used across the pack. One canonical definition per field.",
    when: "Phase 3 draft (with Artifact 5), frozen in Phase 7.",
    tiers: { T1: "required", T2: "required", T3: "optional" }
  },
  { id: "A21", num: 21, slug: "anomaly-playbook",           phase: 7, owner: "Platform + Finance",
    file: "Artifact_21_Anomaly_Playbook.docx",
    title: "Cost Anomaly Playbook",
    purpose: "Standing triage steps for cost anomalies: first 30 min, first 2 hours, first 24 hours, plus a postmortem template.",
    when: "Phase 7. Rehearse a simulated incident before consultant departs.",
    tiers: { T1: "required", T2: "optional", T3: "optional" }
  }
];

window.ACA.domains = [
  { key: "generic",       name: "Generic",                 tagline: "Baseline enterprise use, no additional regulatory overlay.",
    add: "Standard 21-artifact pack." },
  { key: "banking",       name: "Banking & FSI",           tagline: "SR 11-7, GLBA, model-risk management.",
    add: "Independent second-line validation, MRM tiering explicit, data-use committee signoff." },
  { key: "retail",        name: "Retail & E-commerce",     tagline: "Peak-season variability, thin-margin, high-volume.",
    add: "Peak-season overlay row in the forecast; higher variance tolerance in pilot." },
  { key: "energy",        name: "Energy / Oil & Gas",      tagline: "Remote sites, egress costs, HSE stakes.",
    add: "Remote-site egress line; HSE risk category in the risk register." },
  { key: "aerospace",     name: "Aerospace & Defense",     tagline: "ITAR/EAR, configuration management, safety.",
    add: "Config-management overhead line; export-control review in risk register." },
  { key: "public_sector", name: "Public Sector",           tagline: "FedRAMP boundary, ATO maintenance, FISMA scope.",
    add: "ATO-maintenance and audit-support lines; explicit FedRAMP boundary in pricing table." },
  { key: "telecom",       name: "Telecommunications",      tagline: "Multi-region duplication, carrier-grade uptime.",
    add: "Multi-region infrastructure duplication line; higher SLA targets." },
  { key: "entertainment", name: "Media & Entertainment",   tagline: "Rights verification, content moderation.",
    add: "Rights-verification cost line; content-moderation gates in evaluation." }
];

// Tier -> required artifact ids
window.ACA.tiers = {
  T1: window.ACA.artifacts.map(a => a.id),
  T2: window.ACA.artifacts.filter(a => a.tiers.T2 === "required").map(a => a.id),
  T3: window.ACA.artifacts.filter(a => a.tiers.T3 === "required").map(a => a.id)
};
