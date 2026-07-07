import { useEffect, useState } from 'react';
import { Link } from 'wouter';
import { api } from '../api.js';
import { TopBar } from '../App.jsx';
import { PlusCircle, Download, ArrowRight } from 'lucide-react';

const STATUS_COLORS = {
  discovery: 'border-muted/40 text-muted bg-surface2',
  business_case: 'border-warn/40 text-warn bg-warn/5',
  pilot: 'border-accent/40 text-accent bg-accent/5',
  scale: 'border-ok/40 text-ok bg-ok/5',
  operate: 'border-ok/40 text-ok bg-ok/5',
  retired: 'border-muted/40 text-muted bg-surface2',
};

function StatCard({ label, value, sub }) {
  return (
    <div className="card p-5">
      <div className="text-xs uppercase tracking-wider text-muted">{label}</div>
      <div className="mt-1 text-3xl font-semibold text-ink tabular-nums">{value}</div>
      {sub && <div className="mt-1 text-xs text-muted">{sub}</div>}
    </div>
  );
}

function BarGroup({ title, data }) {
  const total = Object.values(data).reduce((a, b) => a + b, 0);
  const entries = Object.entries(data);
  return (
    <div className="card p-5">
      <div className="text-sm font-semibold text-ink mb-3">{title}</div>
      {entries.length === 0 && <div className="text-sm text-muted">No data yet.</div>}
      <div className="space-y-2">
        {entries.map(([k, v]) => (
          <div key={k}>
            <div className="flex items-center justify-between text-xs">
              <span className="text-ink capitalize">{k.replaceAll('_', ' ')}</span>
              <span className="text-muted tabular-nums">{v}</span>
            </div>
            <div className="h-2 rounded-full bg-surface2 overflow-hidden mt-1">
              <div className="h-full bg-accent" style={{ width: `${total ? (100 * v) / total : 0}%` }} />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([api.portfolioSummary(), api.listProjects()])
      .then(([s, p]) => {
        setSummary(s);
        setProjects(p);
      })
      .finally(() => setLoading(false));
  }, []);

  return (
    <>
      <TopBar>
        <div>
          <div className="text-sm font-semibold text-ink">Portfolio dashboard</div>
          <div className="text-xs text-muted">AI cost management at a glance</div>
        </div>
        <div className="flex items-center gap-2">
          <a href={api.blankAllUrl()} className="btn" data-testid="button-download-blank-pack">
            <Download size={14} /> Blank template pack
          </a>
          <Link href="/projects">
            <a className="btn-primary" data-testid="button-open-projects">
              <PlusCircle size={14} /> New project
            </a>
          </Link>
        </div>
      </TopBar>
      <main className="p-6 flex-1 overflow-auto">
        {loading && <div className="text-muted">Loading…</div>}
        {summary && (
          <>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <StatCard label="Projects" value={summary.project_count} sub="Across LOBs" />
              <StatCard label="Artifacts per project" value={summary.artifact_count} sub="Reference-manual depth" />
              <StatCard
                label="Completeness"
                value={`${summary.avg_completeness_pct}%`}
                sub="Filled artifacts / total"
              />
              <StatCard
                label="Domains covered"
                value={Object.keys(summary.by_domain).length}
                sub="Generic + domain overlays"
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
              <BarGroup title="By line of business" data={summary.by_lob} />
              <BarGroup title="By status" data={summary.by_status} />
              <BarGroup title="By domain overlay" data={summary.by_domain} />
            </div>
          </>
        )}

        <div className="card mt-6 overflow-hidden">
          <div className="px-5 py-3 border-b border-border flex items-center justify-between">
            <div className="text-sm font-semibold text-ink">Active projects</div>
            <Link href="/projects">
              <a className="text-xs text-accent hover:underline flex items-center gap-1">
                View all <ArrowRight size={12} />
              </a>
            </Link>
          </div>
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-xs text-muted border-b border-border bg-surface2">
                <th className="px-5 py-2 font-medium">Project</th>
                <th className="px-5 py-2 font-medium">LOB</th>
                <th className="px-5 py-2 font-medium">Domain</th>
                <th className="px-5 py-2 font-medium">Status</th>
                <th className="px-5 py-2 font-medium text-right">Actions</th>
              </tr>
            </thead>
            <tbody>
              {projects.map((p) => (
                <tr key={p.id} className="border-b border-border last:border-b-0 hover:bg-surface2" data-testid={`row-project-${p.id}`}>
                  <td className="px-5 py-3">
                    <Link href={`/projects/${p.id}`}>
                      <a className="font-medium text-ink hover:text-accent" data-testid={`link-project-${p.id}`}>
                        {p.name}
                      </a>
                    </Link>
                    <div className="text-xs text-muted">{p.summary}</div>
                  </td>
                  <td className="px-5 py-3 text-ink">{p.lob || '—'}</td>
                  <td className="px-5 py-3 text-muted capitalize">{(p.domain || 'generic').replaceAll('_', ' ')}</td>
                  <td className="px-5 py-3">
                    <span className={`chip ${STATUS_COLORS[p.status] || 'border-border text-muted'}`}>
                      {p.status.replaceAll('_', ' ')}
                    </span>
                  </td>
                  <td className="px-5 py-3 text-right">
                    <a href={api.exportAllUrl(p.id)} className="btn-ghost whitespace-nowrap" data-testid={`button-export-all-${p.id}`}>
                      <Download size={14} /> All DOCX
                    </a>
                  </td>
                </tr>
              ))}
              {projects.length === 0 && (
                <tr>
                  <td colSpan={5} className="px-5 py-8 text-center text-muted">
                    No projects yet — create one to get started.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </main>
    </>
  );
}
