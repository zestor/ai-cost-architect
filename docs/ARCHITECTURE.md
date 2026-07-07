# Architecture

## High-level

```
┌──────────────────────┐        ┌───────────────────────────────┐
│  React SPA (Vite)    │  /api  │  FastAPI backend              │
│  - Dashboard         │◀──────▶│  - CRUD (projects, entries)   │
│  - Projects          │        │  - DOCX render on demand      │
│  - ProjectDetail     │        │  - Portfolio summary          │
│  - ArtifactEditor    │        │  - Blank template pack        │
│  - TemplateLibrary   │        │                               │
│  - ArtifactReference │        │  SQLite (finops.db)           │
└──────────────────────┘        │  Auto-seeded on empty DB      │
                                └───────────────────────────────┘
                                            │
                                            ▼
                                ┌───────────────────────────────┐
                                │ artifacts_content.py          │
                                │  = single source of truth     │
                                │  used by both DOCX renderer   │
                                │  and API surface              │
                                └───────────────────────────────┘
```

## Single source of truth

`backend/artifacts_content.py` exports a single Python list `ARTIFACTS` where each element is a dict with:

- `id` (`A01`–`A21`), `number`, `title`, `short_title`, `role_context`, `purpose`, `when_to_use`, `inputs_needed`
- `learning`:
  - `concepts` — list of `{term, definition}` pairs
  - `how_to_use` — ordered steps
  - `worked_example` — narrative with numbers
  - `pitfalls` — list of common mistakes
  - `decision_tree` — plain-text branching guidance
  - `domain_overlays` — dict keyed by domain (`generic`, `banking`, etc.)
- `fields` — form definitions: `{key, label, type, help?, options?, placeholder?, rows?}`
- `tables` — table definitions: `{key, label, columns: [{key, label}]}`

Both the DOCX renderer (`docx_render.py`) and the FastAPI backend (`main.py`) import from this single file. To add fields, tables, or overlays: edit `artifacts_content.py` and both surfaces update on next request/build.

## Adding a new domain

1. Add the key to `DOMAIN_OVERLAY_KEYS` in `artifacts_content.py`.
2. For each artifact, add a paragraph under `learning.domain_overlays[<new_key>]` describing what changes in that industry.
3. Update `frontend/src/pages/ArtifactReference.jsx`'s `DOMAIN_LABELS` to give the key a human-readable label.
4. Update the domain dropdown lists in `frontend/src/pages/Projects.jsx` and `frontend/src/pages/ArtifactEditor.jsx`.

That's it — the DOCX renderer picks up the new overlay automatically from the same dict.

## Deployment options

- **Single-port prod**: `npm run build` in `frontend/`, then run the backend — FastAPI serves both the API and `../frontend/dist/`.
- **Split**: run frontend behind any static host, point it at the backend URL by setting the base in `api.js`.
- **Placeholder-based deploy**: `api.js` has a `__PORT_8765__` sentinel that certain hosting proxies (Perplexity Sites, etc.) can replace at deploy time. Safe to ignore for standard deployments.

## Security notes

The included backend has no authentication — add your enterprise SSO / IAM in front of it before exposing beyond localhost. Any user with API access can create, edit, delete projects and export documents. For a bank-style deployment, wire this behind your standard identity gateway and audit-log the export endpoints.
