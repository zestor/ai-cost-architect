import { useEffect, useMemo, useState } from 'react';
import { Link, useRoute } from 'wouter';
import { api } from '../api.js';
import { TopBar } from '../App.jsx';
import { ArrowLeft, Download, FileText, CheckCircle2, Circle, Edit3, Package } from 'lucide-react';

const STATUS_COLORS = {
  discovery: 'border-muted/40 text-muted bg-surface2',
  business_case: 'border-warn/40 text-warn bg-warn/5',
  pilot: 'border-accent/40 text-accent bg-accent/5',
  scale: 'border-ok/40 text-ok bg-ok/5',
  operate: 'border-ok/40 text-ok bg-ok/5',
  retired: 'border-muted/40 text-muted bg-surface2',
};

const STAGE_GROUPS = [
  { title: 'Foundations', ids: ['A01', 'A02', 'A03'] },
  { title: 'Design & Build', ids: ['A04', 'A05', 'A06', 'A07'] },
  { title: 'Cost & Unit Economics', ids: ['A08', 'A09', 'A10', 'A11'] },
  { title: 'Operate & Govern', ids: ['A12', 'A13', 'A14', 'A15', 'A16'] },
  { title: 'Scale & Executive', ids: ['A17', 'A18', 'A19', 'A20', 'A21'] },
];

export default function ProjectDetail() {
  const [, params] = useRoute('/projects/:pid');
  const pid = params?.pid;
  const [project, setProject] = useState(null);
  const [entries, setEntries] = useState({});
  const [artifacts, setArtifacts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!pid) return;
    Promise.all([api.getProject(pid), api.listArtifacts()])
      .then(([proj, arts]) => {
        setProject(proj);
        setEntries(proj.entries || {});
        setArtifacts(arts);
      })
      .finally(() => setLoading(false));
  }, [pid]);

  const artIndex = useMemo(() => Object.fromEntries(artifacts.map((a) => [a.id, a])), [artifacts]);

  const completedCount = artifacts.filter((a) => entries[a.id]?.fields || entries[a.id]?.tables).length;
  const pct = artifacts.length ? Math.round((100 * completedCount) / artifacts.length) : 0;

  const isFilled = (aid) => {
    const e = entries[aid];
    if (!e) return false;
    const hasFields = e.fields && Object.keys(e.fields).some((k) => (e.fields[k] || '').toString().trim() !== '');
    const hasTables = e.tables && Object.keys(e.tables).some((k) => Array.isArray(e.tables[k]) && e.tables[k].length > 0);
    return hasFields || hasTables;
  };

  if (loading) return <><TopBar><div className="text-sm text-muted">Loading…</div></TopBar><main className="p-6" /></>;
  if (!project) return <><TopBar><div className="text-sm text-err">Project not found</div></TopBar></>;

  return (
    <>
      <TopBar>
        <div className="flex items-center gap-3 min-w-0">
          <Link href="/projects"><a className="btn-ghost" data-testid="button-back-projects"><ArrowLeft size={14} /></a></Link>
          <div className="min-w-0">
            <div className="text-sm font-semibold text-ink truncate">{project.name}</div>
            <div className="text-xs text-muted truncate">{project.summary || 'No summary'}</div>
          </div>
        </div>
        <div className="flex items-center gap-2 shrink-0">
          <a href={api.exportAllUrl(project.id)} className="btn-primary" data-testid="button-export-all">
            <Package size={14} /> Export all 21 as DOCX (zip)
          </a>
        </div>
      </TopBar>
      <main className="p-6 flex-1 overflow-auto">
        {/* Meta bar */}
        <div className="card p-5 mb-6">
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4 text-sm">
            <div>
              <div className="text-xs uppercase tracking-wider text-muted">LOB</div>
              <div className="text-ink mt-0.5">{project.lob || '—'}</div>
            </div>
            <div>
              <div className="text-xs uppercase tracking-wider text-muted">Domain</div>
              <div className="text-ink capitalize mt-0.5">{(project.domain || 'generic').replaceAll('_', ' ')}</div>
            </div>
            <div>
              <div className="text-xs uppercase tracking-wider text-muted">Status</div>
              <div className="mt-0.5">
                <span className={`chip ${STATUS_COLORS[project.status] || 'border-border text-muted'}`}>
                  {project.status.replaceAll('_', ' ')}
                </span>
              </div>
            </div>
            <div>
              <div className="text-xs uppercase tracking-wider text-muted">Owner</div>
              <div className="text-ink mt-0.5 text-xs">{project.owner || '—'}</div>
            </div>
            <div>
              <div className="text-xs uppercase tracking-wider text-muted">Completeness</div>
              <div className="flex items-center gap-2 mt-1">
                <div className="h-2 rounded-full bg-surface2 flex-1 overflow-hidden">
                  <div className="h-full bg-accent" style={{ width: `${pct}%` }} />
                </div>
                <div className="text-xs tabular-nums text-muted w-14 text-right">{completedCount}/{artifacts.length}</div>
              </div>
            </div>
          </div>
        </div>

        {/* Artifact groups */}
        {STAGE_GROUPS.map((group) => (
          <section key={group.title} className="mb-8">
            <h2 className="text-sm font-semibold text-ink mb-3">{group.title}</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
              {group.ids.map((aid) => {
                const art = artIndex[aid];
                if (!art) return null;
                const filled = isFilled(aid);
                return (
                  <div key={aid} className="card p-4 hover:border-accent/40 transition-colors" data-testid={`card-artifact-${aid}`}>
                    <div className="flex items-start justify-between gap-2">
                      <div className="min-w-0">
                        <div className="flex items-center gap-2">
                          <div className="text-[11px] font-mono text-muted">{aid}</div>
                          {filled ? (
                            <CheckCircle2 size={13} className="text-ok" />
                          ) : (
                            <Circle size={13} className="text-faint" />
                          )}
                        </div>
                        <div className="text-sm font-medium text-ink mt-0.5 leading-snug">{art.title}</div>
                        <div className="text-[11px] text-muted mt-1 line-clamp-2">{art.purpose}</div>
                      </div>
                    </div>
                    <div className="flex items-center gap-1 mt-3">
                      <Link href={`/projects/${project.id}/artifacts/${aid}`}>
                        <a className="btn text-xs flex-1 justify-center" data-testid={`button-edit-${aid}`}>
                          <Edit3 size={12} /> {filled ? 'Edit' : 'Fill in'}
                        </a>
                      </Link>
                      <a href={api.exportOneUrl(project.id, aid)} className="btn-ghost text-xs" data-testid={`button-download-${aid}`}>
                        <Download size={12} /> DOCX
                      </a>
                      <Link href={`/reference/${aid}`}>
                        <a className="btn-ghost text-xs" data-testid={`button-reference-${aid}`}>
                          <FileText size={12} />
                        </a>
                      </Link>
                    </div>
                  </div>
                );
              })}
            </div>
          </section>
        ))}
      </main>
    </>
  );
}
