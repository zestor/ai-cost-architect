# FinOps AI — Portfolio Manager

A production-grade framework for managing enterprise portfolios of AI use cases across lines of business. Includes 21 reference-manual artifacts (each covering concepts, worked example, pitfalls, decision tree, and 8 domain overlays), a React single-page application for managing multiple projects, and a FastAPI backend that generates filled DOCX reports on demand.

Built for the role of **Principal AI Solutions Consultant** — someone standing up a company-wide FinOps-for-AI practice across a large portfolio of use cases and multiple LOBs.

---

## What's in the box

```
finops-ai/
├── backend/                 FastAPI + SQLite + docx generation (single source of truth)
│   ├── artifacts_content.py 21 artifacts with concepts, examples, overlays, form fields, tables
│   ├── docx_render.py       Corporate-styled DOCX renderer (Hydra Teal accent, Calibri)
│   ├── main.py              FastAPI app — CRUD, exports, portfolio summary
│   └── seed_data.py         3 seeded projects (Consumer Banking, Commercial Lending, Tech Enablement)
├── frontend/                Vite + React + Tailwind + wouter SPA
│   ├── src/
│   │   ├── App.jsx          Router + sidebar
│   │   ├── api.js           Thin API client (dev proxy + deploy-time placeholder)
│   │   └── pages/           Dashboard, Projects, ProjectDetail, ArtifactEditor,
│   │                        TemplateLibrary, ArtifactReference
│   └── (Tailwind, Vite, PostCSS configs)
├── templates/               21 pre-generated blank DOCX + all_21_blank.zip
├── research/                Original FinOps-for-AI research brief (6,540 words, 75 citations)
└── scripts/                 One-liners for dev and prod
```

---

## Quickstart

### Prerequisites

- Python 3.10+
- Node.js 20+

### 1. Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 8765 --reload
```

The backend auto-creates `finops.db` on first run and seeds it with three realistic AI projects.

### 2. Frontend

```bash
cd frontend
npm install
npm run dev          # http://localhost:5173 (proxied /api -> 8765)
```

Or for production:

```bash
npm run build        # emits dist/
```

Then serve `dist/` behind any static host. The FastAPI backend also serves `../frontend/dist` automatically when it exists — so you can run everything from a single port in prod.

---

## Domains

Every artifact has eight domain overlays baked in — the same artifact renders with different tabs, review chains, and guidance depending on the project's domain:

- generic (enterprise baseline)
- banking (SR 11-7 tiering, second-line MRM validation)
- retail (peak-season overlay)
- energy_oil_gas (remote-site egress)
- aerospace (configuration-management overhead)
- public_sector (ATO maintenance)
- telecom (multi-region duplication)
- entertainment (rights-verification cost line)

To add a new domain (e.g. healthcare, insurance, manufacturing), add the key to `DOMAIN_OVERLAY_KEYS` in `backend/artifacts_content.py` and a paragraph per artifact under each `learning.domain_overlays` dict. The UI picks it up automatically.

---

## The 21 Artifacts

| # | Artifact | Purpose |
|---|---|---|
| A01 | Engagement Kickoff & Scope | Shared, auditable agreement on what will be modeled |
| A02 | AI Workload Decomposition & Architecture | Turn architecture into measurable cost-impacting steps |
| A03 | AI Cost Boundary, Assumptions & Pricing | Make the cost model defensible with stated assumptions |
| A04 | AI Cost Driver Map | Backbone table linking each driver to a signal and unit cost |
| A05 | Metering & Instrumentation | Ensure you can actually measure the drivers you modeled |
| A06 | Pilot Measurement Plan | Calibrate averages and distributions |
| A07 | AI Unit Economics Calculator | Cost per request and per successful outcome |
| A08 | AI Cost Forecast Model | Monthly forecast finance and auditors can trace |
| A09 | Scenario Planning & Sensitivity | Translate uncertainty into decision options |
| A10 | Optimization Options Catalog | Actionable options with quantified impacts |
| A11 | Benefits Value Calculator | Ensure ROI doesn't assume benefits that would happen anyway |
| A12 | ROI / NPV Model | NPV, IRR, payback with sensitivity |
| A13 | Executive One-Pager | Concise decision document for leadership |
| A14 | Full Business Case Narrative | Auditable narrative for governance |
| A15 | Risk Register & Controls | Operational and governance risks affecting cost, quality, compliance |
| A16 | Evaluation & Quality Gate | Quality gates that affect retry rate, output length, escalations |
| A17 | FinOps Operating Model | RACI + cadence to make cost management repeatable |
| A18 | Chargeback / Showback | Allocate AI spend in a way that aligns incentives |
| A19 | Vendor & Pricing Negotiation Tracker | Vendor pricing, terms, negotiation status |
| A20 | Data Dictionary | Audit-ready dictionary of every field |
| A21 | Cost Anomaly Playbook | Standing triage steps for cost anomalies |

Each artifact is written as a reference-manual entry for someone with no prior FinOps or AI background: purpose, when to use, role context, inputs, key concepts, step-by-step how-to, a fully worked example, common pitfalls, a decision tree, and all eight domain overlays.

---

## API

All endpoints return JSON unless noted.

| Method | Path | Description |
|---|---|---|
| GET | `/api/artifacts` | List all 21 artifacts (summary) |
| GET | `/api/artifacts/{aid}` | Full artifact detail incl. learning content |
| GET | `/api/domains` | List of domain overlay keys |
| GET | `/api/projects` | List all projects |
| POST | `/api/projects` | Create project |
| GET | `/api/projects/{pid}` | Project + all entries |
| PUT | `/api/projects/{pid}` | Update project |
| DELETE | `/api/projects/{pid}` | Delete project |
| GET | `/api/projects/{pid}/entries/{aid}` | Get one entry |
| PUT | `/api/projects/{pid}/entries/{aid}` | Upsert one entry (fields + tables) |
| GET | `/api/projects/{pid}/export/{aid}` | Download one filled DOCX |
| GET | `/api/projects/{pid}/export_all` | Download all 21 filled DOCX as zip |
| GET | `/api/templates/blank/{aid}` | Blank template DOCX |
| GET | `/api/templates/blank_all` | All 21 blank templates as zip |
| GET | `/api/portfolio/summary` | Portfolio KPIs and grouped counts |

---

## Data Model

Two SQLite tables:

```sql
CREATE TABLE projects (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  summary TEXT,
  lob TEXT,
  owner TEXT,
  domain TEXT DEFAULT 'generic',
  status TEXT DEFAULT 'discovery',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE entries (
  project_id INTEGER,
  artifact_id TEXT,
  fields_json TEXT,   -- JSON: {field_key: value}
  tables_json TEXT,   -- JSON: {table_key: [{col_key: value}]}
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (project_id, artifact_id)
);
```

The artifact definitions in `backend/artifacts_content.py` are the single source of truth. Both the DOCX renderer and the frontend read from the same file — edit an artifact once and both surfaces update.

---

## Design System

- **Accent color**: Hydra Teal `#01696F` (both DOCX and web)
- **DOCX**: Calibri, teal header rows with white text, alternating row shading `#F1EFEA`, footer with artifact ID / project / date
- **Web**: Inter via CDN, generous whitespace, one accent, chip-style status badges
- **Hash routing** in the SPA (compatible with iframe hosts)

---

## License

Provided as-is for the recipient's internal use.

---

## Credits

Framework and code by Chris Clark (Principal AI Solutions Consultant). Original research brief in `research/ai_finops_research.md`.
