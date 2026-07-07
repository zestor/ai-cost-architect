"""FastAPI backend for the AI Cost Architect Portfolio Manager.

Endpoints
---------
GET    /api/artifacts                       -> list of 21 artifact definitions (summary)
GET    /api/artifacts/{artifact_id}         -> full artifact definition (fields, tables, learning)
GET    /api/projects                        -> list projects
POST   /api/projects                        -> create project
GET    /api/projects/{id}                   -> project with entries
PUT    /api/projects/{id}                   -> update project meta
DELETE /api/projects/{id}                   -> delete project
GET    /api/projects/{id}/entries/{aid}     -> get entry (fields + table rows)
PUT    /api/projects/{id}/entries/{aid}     -> upsert entry
GET    /api/projects/{id}/export/{aid}      -> generate DOCX for one artifact
GET    /api/projects/{id}/export_all        -> zip of all 21 filled DOCX
GET    /api/templates/blank/{aid}           -> blank DOCX template
GET    /api/templates/blank_all             -> zip of all 21 blank templates
GET    /api/domains                         -> list of supported domain overlays
GET    /api/portfolio/summary               -> portfolio-level KPIs
"""

from __future__ import annotations

import io
import json
import os
import sqlite3
import zipfile
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from artifacts_content import ARTIFACTS, DOMAIN_OVERLAY_KEYS, get_artifact, list_artifacts_summary
from docx_render import render_artifact


# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------

DB_PATH = os.environ.get("ACA_DB_PATH", "/home/user/workspace/ai_cost_architect/app/backend/aicost.db")


def _init_db() -> None:
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                lob TEXT,
                domain TEXT NOT NULL DEFAULT 'generic',
                summary TEXT,
                status TEXT NOT NULL DEFAULT 'discovery',
                owner TEXT,
                created_at TEXT NOT NULL DEFAULT (datetime('now')),
                updated_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
        """)
        con.execute("""
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                artifact_id TEXT NOT NULL,
                fields_json TEXT NOT NULL DEFAULT '{}',
                tables_json TEXT NOT NULL DEFAULT '{}',
                updated_at TEXT NOT NULL DEFAULT (datetime('now')),
                UNIQUE(project_id, artifact_id),
                FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE CASCADE
            )
        """)
        con.commit()


@contextmanager
def db():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    try:
        yield con
        con.commit()
    finally:
        con.close()


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

class ProjectIn(BaseModel):
    name: str
    lob: str | None = None
    domain: str = "generic"
    summary: str | None = None
    status: str = "discovery"
    owner: str | None = None


class ProjectUpdate(BaseModel):
    name: str | None = None
    lob: str | None = None
    domain: str | None = None
    summary: str | None = None
    status: str | None = None
    owner: str | None = None


class EntryIn(BaseModel):
    fields: dict[str, Any] = {}
    tables: dict[str, list[dict[str, Any]]] = {}


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

app = FastAPI(title="AI Cost Architect Portfolio Manager")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    _init_db()
    _seed_if_empty()


# ---------------------------------------------------------------------------
# Artifacts
# ---------------------------------------------------------------------------

@app.get("/api/artifacts")
def artifacts_list():
    return list_artifacts_summary()


@app.get("/api/artifacts/{artifact_id}")
def artifacts_get(artifact_id: str):
    a = get_artifact(artifact_id)
    if not a:
        raise HTTPException(404, "Artifact not found")
    return a


@app.get("/api/domains")
def domains_list():
    return [
        {"key": "generic", "label": "Generic Enterprise"},
        {"key": "banking", "label": "Banking / Financial Services"},
        {"key": "retail", "label": "Retail & E-commerce"},
        {"key": "energy_oil_gas", "label": "Energy / Oil & Gas"},
        {"key": "aerospace", "label": "Aerospace & Defense"},
        {"key": "public_sector", "label": "Public Sector"},
        {"key": "telecom", "label": "Telecommunications"},
        {"key": "entertainment", "label": "Entertainment & Media"},
    ]


# ---------------------------------------------------------------------------
# Projects
# ---------------------------------------------------------------------------

def _row_to_project(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "id": row["id"],
        "name": row["name"],
        "lob": row["lob"],
        "domain": row["domain"],
        "summary": row["summary"],
        "status": row["status"],
        "owner": row["owner"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }


@app.get("/api/projects")
def projects_list():
    with db() as con:
        rows = con.execute("SELECT * FROM projects ORDER BY id DESC").fetchall()
        return [_row_to_project(r) for r in rows]


@app.post("/api/projects", status_code=201)
def projects_create(payload: ProjectIn):
    if payload.domain not in DOMAIN_OVERLAY_KEYS:
        raise HTTPException(400, f"Unknown domain '{payload.domain}'")
    with db() as con:
        cur = con.execute(
            """INSERT INTO projects(name, lob, domain, summary, status, owner)
               VALUES(?,?,?,?,?,?)""",
            (payload.name, payload.lob, payload.domain, payload.summary, payload.status, payload.owner),
        )
        pid = cur.lastrowid
        row = con.execute("SELECT * FROM projects WHERE id=?", (pid,)).fetchone()
        return _row_to_project(row)


@app.get("/api/projects/{pid}")
def projects_get(pid: int):
    with db() as con:
        row = con.execute("SELECT * FROM projects WHERE id=?", (pid,)).fetchone()
        if not row:
            raise HTTPException(404, "Project not found")
        entries = con.execute(
            "SELECT artifact_id, fields_json, tables_json, updated_at FROM entries WHERE project_id=?",
            (pid,),
        ).fetchall()
        entry_map = {
            e["artifact_id"]: {
                "artifact_id": e["artifact_id"],
                "fields": json.loads(e["fields_json"] or "{}"),
                "tables": json.loads(e["tables_json"] or "{}"),
                "updated_at": e["updated_at"],
            }
            for e in entries
        }
        project = _row_to_project(row)
        project["entries"] = entry_map
        # completeness stats
        project["completeness"] = {
            "artifacts_touched": len(entry_map),
            "total_artifacts": len(ARTIFACTS),
        }
        return project


@app.put("/api/projects/{pid}")
def projects_update(pid: int, payload: ProjectUpdate):
    with db() as con:
        row = con.execute("SELECT * FROM projects WHERE id=?", (pid,)).fetchone()
        if not row:
            raise HTTPException(404, "Project not found")
        fields = {k: v for k, v in payload.model_dump().items() if v is not None}
        if not fields:
            return _row_to_project(row)
        if "domain" in fields and fields["domain"] not in DOMAIN_OVERLAY_KEYS:
            raise HTTPException(400, f"Unknown domain '{fields['domain']}'")
        set_clause = ", ".join(f"{k}=?" for k in fields)
        values = list(fields.values()) + [pid]
        con.execute(f"UPDATE projects SET {set_clause}, updated_at=datetime('now') WHERE id=?", values)
        row = con.execute("SELECT * FROM projects WHERE id=?", (pid,)).fetchone()
        return _row_to_project(row)


@app.delete("/api/projects/{pid}", status_code=204)
def projects_delete(pid: int):
    with db() as con:
        con.execute("DELETE FROM projects WHERE id=?", (pid,))
    return Response(status_code=204)


# ---------------------------------------------------------------------------
# Entries
# ---------------------------------------------------------------------------

@app.get("/api/projects/{pid}/entries/{aid}")
def entry_get(pid: int, aid: str):
    if not get_artifact(aid):
        raise HTTPException(404, "Artifact not found")
    with db() as con:
        row = con.execute(
            "SELECT fields_json, tables_json, updated_at FROM entries WHERE project_id=? AND artifact_id=?",
            (pid, aid),
        ).fetchone()
        if not row:
            return {"artifact_id": aid, "fields": {}, "tables": {}, "updated_at": None}
        return {
            "artifact_id": aid,
            "fields": json.loads(row["fields_json"] or "{}"),
            "tables": json.loads(row["tables_json"] or "{}"),
            "updated_at": row["updated_at"],
        }


@app.put("/api/projects/{pid}/entries/{aid}")
def entry_upsert(pid: int, aid: str, payload: EntryIn):
    if not get_artifact(aid):
        raise HTTPException(404, "Artifact not found")
    with db() as con:
        exists = con.execute("SELECT id FROM projects WHERE id=?", (pid,)).fetchone()
        if not exists:
            raise HTTPException(404, "Project not found")
        con.execute(
            """INSERT INTO entries(project_id, artifact_id, fields_json, tables_json)
               VALUES(?,?,?,?)
               ON CONFLICT(project_id, artifact_id) DO UPDATE SET
                    fields_json=excluded.fields_json,
                    tables_json=excluded.tables_json,
                    updated_at=datetime('now')""",
            (pid, aid, json.dumps(payload.fields), json.dumps(payload.tables)),
        )
        con.execute("UPDATE projects SET updated_at=datetime('now') WHERE id=?", (pid,))
    return {"ok": True}


# ---------------------------------------------------------------------------
# Exports
# ---------------------------------------------------------------------------

def _render_for_project(pid: int, aid: str) -> tuple[bytes, str]:
    artifact = get_artifact(aid)
    if not artifact:
        raise HTTPException(404, "Artifact not found")
    with db() as con:
        proj = con.execute("SELECT * FROM projects WHERE id=?", (pid,)).fetchone()
        if not proj:
            raise HTTPException(404, "Project not found")
        entry = con.execute(
            "SELECT fields_json, tables_json FROM entries WHERE project_id=? AND artifact_id=?",
            (pid, aid),
        ).fetchone()
    fields = json.loads(entry["fields_json"]) if entry else {}
    tables = json.loads(entry["tables_json"]) if entry else {}
    data = render_artifact(
        artifact,
        project_name=proj["name"],
        domain=proj["domain"],
        field_values=fields,
        table_rows=tables,
    )
    safe = artifact["short_title"].replace("/", "-").replace(" ", "_")
    fname = f"Artifact_{artifact['number']:02d}_{safe}.docx"
    return data, fname


@app.get("/api/projects/{pid}/export/{aid}")
def export_one(pid: int, aid: str):
    data, fname = _render_for_project(pid, aid)
    return Response(
        content=data,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f'attachment; filename="{fname}"'},
    )


@app.get("/api/projects/{pid}/export_all")
def export_all(pid: int):
    with db() as con:
        proj = con.execute("SELECT * FROM projects WHERE id=?", (pid,)).fetchone()
        if not proj:
            raise HTTPException(404, "Project not found")
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for a in ARTIFACTS:
            data, fname = _render_for_project(pid, a["id"])
            z.writestr(fname, data)
    buf.seek(0)
    safe = proj["name"].replace("/", "-").replace(" ", "_")
    return Response(
        content=buf.getvalue(),
        media_type="application/zip",
        headers={"Content-Disposition": f'attachment; filename="{safe}_AI_Cost_Pack.zip"'},
    )


@app.get("/api/templates/blank/{aid}")
def blank_one(aid: str):
    a = get_artifact(aid)
    if not a:
        raise HTTPException(404, "Artifact not found")
    data = render_artifact(a)
    safe = a["short_title"].replace("/", "-").replace(" ", "_")
    fname = f"Artifact_{a['number']:02d}_{safe}.docx"
    return Response(
        content=data,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f'attachment; filename="{fname}"'},
    )


@app.get("/api/templates/blank_all")
def blank_all():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for a in ARTIFACTS:
            data = render_artifact(a)
            safe = a["short_title"].replace("/", "-").replace(" ", "_")
            z.writestr(f"Artifact_{a['number']:02d}_{safe}.docx", data)
    buf.seek(0)
    return Response(
        content=buf.getvalue(),
        media_type="application/zip",
        headers={"Content-Disposition": 'attachment; filename="AI_Cost_Architect_Template_Pack.zip"'},
    )


# ---------------------------------------------------------------------------
# Portfolio summary
# ---------------------------------------------------------------------------

@app.get("/api/portfolio/summary")
def portfolio_summary():
    with db() as con:
        projects = con.execute("SELECT * FROM projects").fetchall()
        entries = con.execute("SELECT project_id, COUNT(*) AS c FROM entries GROUP BY project_id").fetchall()
    entry_counts = {r["project_id"]: r["c"] for r in entries}
    by_lob: dict[str, int] = {}
    by_status: dict[str, int] = {}
    by_domain: dict[str, int] = {}
    total_completeness = 0
    for p in projects:
        by_lob[p["lob"] or "Unassigned"] = by_lob.get(p["lob"] or "Unassigned", 0) + 1
        by_status[p["status"]] = by_status.get(p["status"], 0) + 1
        by_domain[p["domain"]] = by_domain.get(p["domain"], 0) + 1
        total_completeness += entry_counts.get(p["id"], 0)
    total_possible = len(projects) * len(ARTIFACTS)
    return {
        "project_count": len(projects),
        "artifact_count": len(ARTIFACTS),
        "by_lob": by_lob,
        "by_status": by_status,
        "by_domain": by_domain,
        "avg_completeness_pct": round(100 * total_completeness / total_possible, 1) if total_possible else 0,
    }


# ---------------------------------------------------------------------------
# Static frontend
# ---------------------------------------------------------------------------

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend" / "dist"

if FRONTEND_DIR.exists():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIR / "assets"), name="assets")

    @app.get("/{path:path}")
    def spa(path: str, request: Request):
        # Do not intercept API
        if path.startswith("api/"):
            raise HTTPException(404)
        target = FRONTEND_DIR / path
        if target.is_file():
            return Response(
                content=target.read_bytes(),
                media_type=_guess_mime(target.suffix),
            )
        # SPA fallback
        index = FRONTEND_DIR / "index.html"
        if index.exists():
            return Response(content=index.read_bytes(), media_type="text/html")
        raise HTTPException(404)


def _guess_mime(suffix: str) -> str:
    return {
        ".html": "text/html",
        ".js": "application/javascript",
        ".css": "text/css",
        ".svg": "image/svg+xml",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".ico": "image/x-icon",
        ".json": "application/json",
        ".woff": "font/woff",
        ".woff2": "font/woff2",
    }.get(suffix.lower(), "application/octet-stream")


# ---------------------------------------------------------------------------
# Seed data (three-LOB portfolio)
# ---------------------------------------------------------------------------

def _seed_if_empty() -> None:
    with db() as con:
        n = con.execute("SELECT COUNT(*) AS c FROM projects").fetchone()["c"]
        if n:
            return

    from seed_data import SEED_PROJECTS
    with db() as con:
        for sp in SEED_PROJECTS:
            cur = con.execute(
                """INSERT INTO projects(name, lob, domain, summary, status, owner)
                   VALUES(?,?,?,?,?,?)""",
                (sp["name"], sp["lob"], sp["domain"], sp["summary"], sp["status"], sp["owner"]),
            )
            pid = cur.lastrowid
            for aid, entry in sp["entries"].items():
                con.execute(
                    """INSERT INTO entries(project_id, artifact_id, fields_json, tables_json)
                       VALUES(?,?,?,?)""",
                    (pid, aid, json.dumps(entry.get("fields", {})), json.dumps(entry.get("tables", {}))),
                )
