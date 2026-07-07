import { useEffect, useState } from 'react';
import { Link } from 'wouter';
import { api } from '../api.js';
import { TopBar } from '../App.jsx';
import { PlusCircle, Download, ArrowRight, X, Trash2 } from 'lucide-react';

const STATUS_OPTIONS = ['discovery', 'business_case', 'pilot', 'scale', 'operate', 'retired'];
const DOMAIN_OPTIONS = ['generic', 'banking', 'retail', 'energy_oil_gas', 'aerospace', 'public_sector', 'telecom', 'entertainment'];
const STATUS_COLORS = {
  discovery: 'border-muted/40 text-muted bg-surface2',
  business_case: 'border-warn/40 text-warn bg-warn/5',
  pilot: 'border-accent/40 text-accent bg-accent/5',
  scale: 'border-ok/40 text-ok bg-ok/5',
  operate: 'border-ok/40 text-ok bg-ok/5',
  retired: 'border-muted/40 text-muted bg-surface2',
};

function NewProjectModal({ open, onClose, onCreated }) {
  const [form, setForm] = useState({
    name: '',
    summary: '',
    lob: '',
    owner: 'Chris Clark (Principal AI Solutions Consultant)',
    domain: 'generic',
    status: 'discovery',
  });
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  if (!open) return null;

  const submit = async (e) => {
    e.preventDefault();
    setError('');
    setSubmitting(true);
    try {
      const created = await api.createProject(form);
      onCreated(created);
      onClose();
      setForm({ name: '', summary: '', lob: '', owner: form.owner, domain: 'generic', status: 'discovery' });
    } catch (err) {
      setError(String(err.message || err));
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-ink/40 backdrop-blur-sm" onClick={onClose}>
      <div className="card w-full max-w-lg bg-white" onClick={(e) => e.stopPropagation()}>
        <div className="flex items-center justify-between px-5 py-3 border-b border-border">
          <div className="text-sm font-semibold text-ink">New AI project</div>
          <button onClick={onClose} className="text-muted hover:text-ink" data-testid="button-close-new-project">
            <X size={16} />
          </button>
        </div>
        <form onSubmit={submit} className="p-5 space-y-3">
          <div>
            <label className="text-xs text-muted block mb-1">Project name</label>
            <input required className="input" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })}
              placeholder="e.g. Contact center RAG assistant" data-testid="input-project-name" />
          </div>
          <div>
            <label className="text-xs text-muted block mb-1">One-line summary</label>
            <input className="input" value={form.summary} onChange={(e) => setForm({ ...form, summary: e.target.value })}
              placeholder="What the AI does and who it serves" data-testid="input-project-summary" />
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-xs text-muted block mb-1">Line of business</label>
              <input className="input" value={form.lob} onChange={(e) => setForm({ ...form, lob: e.target.value })}
                placeholder="e.g. Consumer Banking" data-testid="input-project-lob" />
            </div>
            <div>
              <label className="text-xs text-muted block mb-1">Owner</label>
              <input className="input" value={form.owner} onChange={(e) => setForm({ ...form, owner: e.target.value })}
                data-testid="input-project-owner" />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-xs text-muted block mb-1">Domain overlay</label>
              <select className="input" value={form.domain} onChange={(e) => setForm({ ...form, domain: e.target.value })}
                data-testid="select-project-domain">
                {DOMAIN_OPTIONS.map((d) => (
                  <option key={d} value={d}>{d.replaceAll('_', ' ')}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="text-xs text-muted block mb-1">Status</label>
              <select className="input" value={form.status} onChange={(e) => setForm({ ...form, status: e.target.value })}
                data-testid="select-project-status">
                {STATUS_OPTIONS.map((s) => (
                  <option key={s} value={s}>{s.replaceAll('_', ' ')}</option>
                ))}
              </select>
            </div>
          </div>
          {error && <div className="text-xs text-err bg-err/5 border border-err/30 rounded-md p-2">{error}</div>}
          <div className="pt-2 flex items-center justify-end gap-2">
            <button type="button" onClick={onClose} className="btn" data-testid="button-cancel-new-project">Cancel</button>
            <button type="submit" disabled={submitting} className="btn-primary" data-testid="button-submit-new-project">
              {submitting ? 'Creating…' : 'Create project'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default function Projects() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const [query, setQuery] = useState('');

  const load = () => {
    setLoading(true);
    api.listProjects()
      .then(setProjects)
      .finally(() => setLoading(false));
  };
  useEffect(load, []);

  const filtered = projects.filter((p) =>
    !query || [p.name, p.summary, p.lob, p.owner, p.domain, p.status].some((v) => (v || '').toLowerCase().includes(query.toLowerCase()))
  );

  const remove = async (id) => {
    if (!confirm('Delete this project and all its artifact entries? This cannot be undone.')) return;
    await api.deleteProject(id);
    load();
  };

  return (
    <>
      <TopBar>
        <div>
          <div className="text-sm font-semibold text-ink">Projects</div>
          <div className="text-xs text-muted">Manage the portfolio of AI use cases</div>
        </div>
        <div className="flex items-center gap-2">
          <input value={query} onChange={(e) => setQuery(e.target.value)}
            placeholder="Search projects…"
            className="input w-64 h-9 py-1"
            data-testid="input-search-projects" />
          <button onClick={() => setModalOpen(true)} className="btn-primary whitespace-nowrap" data-testid="button-new-project">
            <PlusCircle size={14} /> New project
          </button>
        </div>
      </TopBar>
      <main className="p-6 flex-1 overflow-auto">
        {loading && <div className="text-muted">Loading…</div>}
        {!loading && (
          <div className="card overflow-hidden">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-xs text-muted border-b border-border bg-surface2">
                  <th className="px-5 py-2 font-medium">Project</th>
                  <th className="px-5 py-2 font-medium">LOB</th>
                  <th className="px-5 py-2 font-medium">Domain</th>
                  <th className="px-5 py-2 font-medium">Status</th>
                  <th className="px-5 py-2 font-medium">Owner</th>
                  <th className="px-5 py-2 font-medium text-right">Actions</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((p) => (
                  <tr key={p.id} className="border-b border-border last:border-b-0 hover:bg-surface2" data-testid={`row-project-${p.id}`}>
                    <td className="px-5 py-3">
                      <Link href={`/projects/${p.id}`}>
                        <a className="font-medium text-ink hover:text-accent" data-testid={`link-project-${p.id}`}>
                          {p.name}
                        </a>
                      </Link>
                      {p.summary && <div className="text-xs text-muted mt-0.5 max-w-md">{p.summary}</div>}
                    </td>
                    <td className="px-5 py-3 text-ink">{p.lob || '—'}</td>
                    <td className="px-5 py-3 text-muted capitalize">{(p.domain || 'generic').replaceAll('_', ' ')}</td>
                    <td className="px-5 py-3">
                      <span className={`chip ${STATUS_COLORS[p.status] || 'border-border text-muted'}`}>
                        {p.status.replaceAll('_', ' ')}
                      </span>
                    </td>
                    <td className="px-5 py-3 text-xs text-muted">{p.owner || '—'}</td>
                    <td className="px-5 py-3">
                      <div className="flex items-center justify-end gap-1">
                        <a href={api.exportAllUrl(p.id)} className="btn-ghost" data-testid={`button-export-${p.id}`}>
                          <Download size={13} /> DOCX
                        </a>
                        <Link href={`/projects/${p.id}`}>
                          <a className="btn-ghost" data-testid={`button-open-${p.id}`}>
                            Open <ArrowRight size={12} />
                          </a>
                        </Link>
                        <button onClick={() => remove(p.id)} className="btn-ghost text-err/70 hover:text-err" data-testid={`button-delete-${p.id}`}>
                          <Trash2 size={13} />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
                {filtered.length === 0 && (
                  <tr>
                    <td colSpan={6} className="px-5 py-10 text-center text-muted">
                      {query ? 'No projects match your search.' : 'No projects yet. Create one to begin.'}
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </main>
      <NewProjectModal open={modalOpen} onClose={() => setModalOpen(false)} onCreated={load} />
    </>
  );
}
