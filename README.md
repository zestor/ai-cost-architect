# AI Cost Architect

A vendor-neutral, generic framework for managing the cost, unit economics, and governance of enterprise AI portfolios across lines of business. Built for the role of **Principal AI Solutions Consultant** — someone standing up a company-wide AI cost management practice across a large portfolio of use cases and multiple LOBs.

The framework includes:

- **A published methodology site** at [zestor.github.io/ai-cost-architect](https://zestor.github.io/ai-cost-architect/) — 7-phase workflow, interactive artifact picker, phase-by-phase guidance
- **21 reference-manual artifacts** — each a DOCX template with concepts, worked example, common pitfalls, decision tree, and 8 domain overlays
- **A working portfolio management app** — React SPA + FastAPI + SQLite that tracks multiple AI projects and generates filled DOCX reports on demand
- **A comprehensive methodology document** in [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md) — start-to-finish playbook

> **Naming note:** This project intentionally does not use the "FinOps" name, which is a trademark of the FinOps Foundation. This is a generic, vendor-neutral framework for AI cost management and is not affiliated with or endorsed by the FinOps Foundation.

---

## What's in the box

```
ai-cost-architect/
├── site/                    GitHub Pages source — the methodology website
│   ├── index.html           Home with interactive phase/tier picker
│   ├── phases/              Phase 1–7 detail pages
│   ├── artifacts/           21 artifact detail pages
│   └── assets/              Shared CSS/JS + canonical data
├── backend/                 FastAPI + SQLite + DOCX generation (single source of truth)
│   ├── artifacts_content.py 21 artifacts with concepts, examples, overlays, form fields, tables
│   ├── docx_render.py       Corporate-styled DOCX renderer (Hydra Teal accent, Calibri)
│   ├── main.py              FastAPI app — CRUD, exports, portfolio summary
│   └── seed_data.py         3 seeded projects across LOBs
├── frontend/                Vite + React + Tailwind + wouter SPA
│   ├── src/
│   │   ├── App.jsx          Router + sidebar
│   │   ├── api.js           Thin API client (dev proxy + deploy-time placeholder)
│   │   └── pages/           Dashboard, Projects, ProjectDetail, ArtifactEditor,
│   │                        TemplateLibrary, ArtifactReference
│   └── (Tailwind, Vite, PostCSS configs)
├── templates/               21 pre-generated blank DOCX + all_21_blank.zip
├── docs/                    METHODOLOGY.md + ARCHITECTURE.md
├── research/                Original AI cost management research brief (6,540 words)
├── scripts/                 One-liners for dev and prod
└── .github/workflows/       GitHub Pages deployment (actions/deploy-pages)
```

---

## Where to start

**If you're new here** — read the methodology site: [zestor.github.io/ai-cost-architect](https://zestor.github.io/ai-cost-architect/). Use the phase/tier picker on the home page to see which artifacts apply to your engagement right now.

**If you're running an engagement** — jump to [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md) and open the phase you're currently in.

**If you want to run the app** — see Quickstart below.

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

The backend auto-creates its SQLite database on first run and seeds it with three realistic AI projects across three LOBs.

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

Or use the helper scripts:

```bash
./scripts/dev.sh      # runs backend + frontend
./scripts/build.sh    # builds frontend + starts backend serving both
```

---

## The 7-phase methodology

| Phase | Weeks     | Purpose                                                          | Primary Artifacts |
|-------|-----------|------------------------------------------------------------------|-------------------|
| 0     | Pre-week  | Decide whether to take the project and at what tier             | Portfolio triage   |
| 1     | Week 0–1  | Establish a signed, shared scope with named owners              | 1                  |
| 2     | Week 1–2  | Decompose architecture and bound the cost model                 | 2, 3, 4            |
| 3     | Week 2–4  | Instrument production and reconcile to invoice ±10%             | 5, 6               |
| 4     | Week 3–5  | Build unit economics, componentized forecast, scenarios         | 7, 8, 9            |
| 5     | Week 4–5  | Actionable optimization levers and honest attributable benefits | 10, 11             |
| 6     | Week 5–6  | Decision-ready business case package                            | 12, 13, 14, 15, 16 |
| 7     | Ongoing   | Sustainable governance after the consultant leaves              | 17, 18, 19, 20, 21 |

Tier 1 engagement = ~6 weeks, all 21 artifacts. Tier 2 = ~4 weeks, core pack. Tier 3 = ~2 weeks, lightweight. See the [portfolio intake section](https://zestor.github.io/ai-cost-architect/phases/intake.html) of the methodology site.

---

## The 21 Artifacts

| #   | Artifact                                             | Purpose                                                                 |
| --- | ---------------------------------------------------- | ----------------------------------------------------------------------- |
| A01 | Engagement Kickoff & Scope                           | Shared, auditable agreement on what will be modeled                     |
| A02 | AI Workload Decomposition & Architecture             | Turn architecture into measurable cost-impacting steps                  |
| A03 | AI Cost Boundary, Assumptions & Pricing              | Make the cost model defensible with stated assumptions                  |
| A04 | AI Cost Driver Map                                   | Backbone table linking each driver to a signal and unit cost            |
| A05 | Metering & Instrumentation                           | Ensure you can actually measure the drivers you modeled                 |
| A06 | Pilot Measurement Plan                               | Calibrate averages, distributions, and reconcile to invoice             |
| A07 | AI Unit Economics Calculator                         | Cost per request and per successful outcome                             |
| A08 | AI Cost Forecast Model (Monthly, by Component)       | Monthly forecast finance and auditors can trace                         |
| A09 | Scenario Planning & Sensitivity                      | Translate uncertainty into decision options                             |
| A10 | Optimization Options Catalog                         | Actionable levers with quantified impacts and named owners              |
| A11 | Benefits Value Calculator (Incremental & Attributable) | Ensure ROI doesn't assume benefits that would have happened anyway    |
| A12 | ROI / NPV Model                                      | NPV, IRR (optional), payback with sensitivity                           |
| A13 | Executive One-Pager                                  | Concise decision document for leadership                                |
| A14 | Full Business Case Narrative                         | Auditable narrative for governance and internal audit                   |
| A15 | Risk Register & Controls                             | Operational, model, third-party, compliance, and data risks             |
| A16 | Evaluation & Quality Gate                            | Quality gates that affect retry rate, output length, escalations        |
| A17 | Cost Management Operating Model (RACI + Cadence)     | Sustainable, repeatable cost management after the consultant phase      |
| A18 | Chargeback / Showback                                | Allocate AI spend in a way that aligns incentives                       |
| A19 | Vendor & Pricing Negotiation Tracker                 | Vendor pricing, terms, and negotiation history over time                |
| A20 | Data Dictionary                                      | Audit-ready dictionary of every field used across the pack              |
| A21 | Cost Anomaly Playbook                                | Standing triage steps for cost anomalies                                |

Each artifact is written as a reference-manual entry for someone with no prior AI cost management or AI background: purpose, when to use, role context, inputs, key concepts, step-by-step how-to, a fully worked example, common pitfalls, a decision tree, and all eight domain overlays.

---

## Domains

Every artifact has eight domain overlays baked in — the same artifact renders with different tabs, review chains, and guidance depending on the project's domain:

| Key             | Domain                | Overlay adds                                                      |
| --------------- | --------------------- | ----------------------------------------------------------------- |
| `generic`       | Enterprise baseline   | Standard 21-artifact pack                                         |
| `banking`       | Banking / FSI         | Independent second-line validation, model-risk tiering, GLBA scope |
| `retail`        | Retail / E-commerce   | Peak-season overlay, higher variance tolerance                    |
| `energy_oil_gas`| Energy / Oil & Gas    | Remote-site egress line, HSE risk category                        |
| `aerospace`    | Aerospace / Defense   | Config-management overhead, export-control review                 |
| `public_sector`| Public Sector         | ATO-maintenance line, FedRAMP boundary                            |
| `telecom`      | Telecommunications    | Multi-region duplication, higher SLA targets                      |
| `entertainment`| Media & Entertainment | Rights-verification cost, content-moderation gates                |

### Adding a new domain

To add a new domain (e.g. healthcare, insurance, manufacturing):

1. Add the key to `DOMAIN_OVERLAY_KEYS` in `backend/artifacts_content.py`
2. Add a paragraph per artifact under each `learning.domain_overlays` dict
3. Add an entry to the `domains` array in `site/assets/data.js` so it appears on the methodology site

The UI picks it up automatically.

---

## API

All endpoints return JSON unless noted.

| Method | Path                                             | Description                             |
| ------ | ------------------------------------------------ | --------------------------------------- |
| GET    | `/api/artifacts`                                 | List all 21 artifacts (summary)         |
| GET    | `/api/artifacts/{aid}`                           | Full artifact detail incl. learning     |
| GET    | `/api/domains`                                   | List of domain overlay keys             |
| GET    | `/api/projects`                                  | List all projects                       |
| POST   | `/api/projects`                                  | Create project                          |
| GET    | `/api/projects/{pid}`                            | Project + all entries                   |
| PUT    | `/api/projects/{pid}`                            | Update project                          |
| DELETE | `/api/projects/{pid}`                            | Delete project                          |
| GET    | `/api/projects/{pid}/entries/{aid}`              | Get one entry                           |
| PUT    | `/api/projects/{pid}/entries/{aid}`              | Upsert one entry (fields + tables)      |
| GET    | `/api/projects/{pid}/export/{aid}`               | Download one filled DOCX                |
| GET    | `/api/projects/{pid}/export_all`                 | Download all 21 filled DOCX as zip      |
| GET    | `/api/templates/blank/{aid}`                     | Blank template DOCX                     |
| GET    | `/api/templates/blank_all`                       | All 21 blank templates as zip           |
| GET    | `/api/portfolio/summary`                         | Portfolio KPIs and grouped counts       |

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

## The methodology site

The `site/` directory is a static site published to GitHub Pages via `.github/workflows/pages.yml`. It uses:

- Plain HTML, CSS, and vanilla JS — no build step, no dependencies
- Inter typeface via CDN
- Nexus color palette (warm neutrals + Hydra Teal accent), light and dark mode
- An interactive phase/tier picker on the home page
- Direct download links to every DOCX template

The site publishes automatically on every push to `main` that touches `site/**` or the workflow file. To develop locally:

```bash
cd site
python -m http.server 8000
# open http://localhost:8000
```

---

## Design System

- **Accent color**: Hydra Teal `#01696F` (both DOCX and web)
- **DOCX**: Calibri, teal header rows with white text, alternating row shading `#F1EFEA`, footer with artifact ID / project / date
- **Web app**: Inter via CDN, generous whitespace, one accent, chip-style status badges
- **Methodology site**: Same Nexus palette, sidebar navigation, WCAG-AA contrast
- **Hash routing** in the SPA (compatible with iframe hosts)

---

## License

MIT. See [LICENSE](LICENSE).

---

## Credits

Framework and code by Chris Clark (Principal AI Solutions Consultant). Original research brief in [`research/ai_finops_research.md`](research/ai_finops_research.md) (filename preserved for historical continuity — the content is generic AI cost management research).
