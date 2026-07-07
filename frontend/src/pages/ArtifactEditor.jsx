import { useEffect, useMemo, useState } from 'react';
import { Link, useRoute } from 'wouter';
import { api } from '../api.js';
import { TopBar } from '../App.jsx';
import { ArrowLeft, Download, Save, Plus, Trash2, BookOpen, Info, AlertTriangle, Compass, Globe } from 'lucide-react';

function Section({ title, icon: Icon, children, defaultOpen = false }) {
  const [open, setOpen] = useState(defaultOpen);
  return (
    <div className="card overflow-hidden">
      <button onClick={() => setOpen(!open)}
        className="w-full flex items-center justify-between px-4 py-3 text-left hover:bg-surface2 transition-colors"
        data-testid={`toggle-${title.toLowerCase().replace(/\s+/g, '-')}`}>
        <div className="flex items-center gap-2">
          {Icon && <Icon size={14} className="text-accent" />}
          <div className="text-sm font-semibold text-ink">{title}</div>
        </div>
        <div className="text-xs text-muted">{open ? 'Hide' : 'Show'}</div>
      </button>
      {open && <div className="px-4 pb-4 pt-1 border-t border-border text-sm text-ink">{children}</div>}
    </div>
  );
}

function Field({ field, value, onChange }) {
  const common = { className: 'input', value: value ?? '', onChange: (e) => onChange(e.target.value), 'data-testid': `field-${field.key}` };
  if (field.type === 'textarea') return <textarea rows={field.rows || 4} {...common} placeholder={field.placeholder || ''} />;
  if (field.type === 'select') {
    return (
      <select {...common}>
        <option value="">— select —</option>
        {(field.options || []).map((o) => <option key={o} value={o}>{o}</option>)}
      </select>
    );
  }
  if (field.type === 'multiselect') {
    const arr = Array.isArray(value) ? value : (value ? String(value).split(',').map((s) => s.trim()).filter(Boolean) : []);
    return (
      <div className="flex flex-wrap gap-1.5">
        {(field.options || []).map((o) => {
          const selected = arr.includes(o);
          return (
            <button
              key={o} type="button"
              onClick={() => onChange(selected ? arr.filter((v) => v !== o) : [...arr, o])}
              className={`chip cursor-pointer ${selected ? 'bg-accent text-white border-accent' : 'border-border text-ink bg-white'}`}
              data-testid={`option-${field.key}-${o}`}>
              {o}
            </button>
          );
        })}
      </div>
    );
  }
  if (field.type === 'date') return <input type="date" {...common} />;
  if (field.type === 'number') return <input type="number" step="any" {...common} placeholder={field.placeholder || ''} />;
  return <input type="text" {...common} placeholder={field.placeholder || ''} />;
}

function TableEditor({ table, rows, onChange }) {
  const cols = table.columns || [];
  const addRow = () => onChange([...(rows || []), Object.fromEntries(cols.map((c) => [c.key, '']))]);
  const removeRow = (i) => onChange(rows.filter((_, idx) => idx !== i));
  const updateCell = (i, k, v) => onChange(rows.map((r, idx) => (idx === i ? { ...r, [k]: v } : r)));
  return (
    <div className="mt-3">
      <div className="flex items-center justify-between mb-1.5">
        <div className="text-xs font-semibold text-ink">{table.label}</div>
        <button onClick={addRow} className="btn-ghost text-xs" data-testid={`button-add-row-${table.key}`}>
          <Plus size={12} /> Add row
        </button>
      </div>
      <div className="overflow-x-auto border border-border rounded-md">
        <table className="w-full text-xs">
          <thead>
            <tr className="bg-surface2 text-muted">
              {cols.map((c) => <th key={c.key} className="text-left px-2 py-1.5 font-medium">{c.label}</th>)}
              <th className="w-8" />
            </tr>
          </thead>
          <tbody>
            {(rows || []).map((row, i) => (
              <tr key={i} className="border-t border-border">
                {cols.map((c) => (
                  <td key={c.key} className="px-1 py-1">
                    <input
                      className="w-full px-1.5 py-1 rounded border border-transparent bg-transparent focus:border-accent focus:bg-white focus:outline-none"
                      value={row[c.key] ?? ''}
                      onChange={(e) => updateCell(i, c.key, e.target.value)}
                      data-testid={`cell-${table.key}-${i}-${c.key}`}
                    />
                  </td>
                ))}
                <td className="px-1 text-right">
                  <button onClick={() => removeRow(i)} className="text-muted hover:text-err" data-testid={`button-remove-row-${table.key}-${i}`}>
                    <Trash2 size={12} />
                  </button>
                </td>
              </tr>
            ))}
            {(!rows || rows.length === 0) && (
              <tr>
                <td colSpan={cols.length + 1} className="px-3 py-4 text-center text-muted">No rows yet.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default function ArtifactEditor() {
  const [, params] = useRoute('/projects/:pid/artifacts/:aid');
  const pid = params?.pid; const aid = params?.aid;
  const [project, setProject] = useState(null);
  const [artifact, setArtifact] = useState(null);
  const [values, setValues] = useState({});
  const [tables, setTables] = useState({});
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [savedAt, setSavedAt] = useState(null);

  useEffect(() => {
    if (!pid || !aid) return;
    setLoading(true);
    Promise.all([api.getProject(pid), api.getArtifact(aid), api.getEntry(pid, aid).catch(() => null)])
      .then(([proj, art, entry]) => {
        setProject(proj); setArtifact(art);
        setValues(entry?.fields || {});
        setTables(entry?.tables || {});
      })
      .finally(() => setLoading(false));
  }, [pid, aid]);

  const save = async () => {
    setSaving(true);
    try {
      await api.upsertEntry(pid, aid, { fields: values, tables });
      setSavedAt(new Date());
    } finally { setSaving(false); }
  };

  const domain = project?.domain || 'generic';
  const activeOverlay = artifact?.learning?.domain_overlays?.[domain];

  if (loading) return <><TopBar><div className="text-sm text-muted">Loading…</div></TopBar></>;
  if (!artifact || !project) return <><TopBar><div className="text-sm text-err">Not found</div></TopBar></>;

  return (
    <>
      <TopBar>
        <div className="flex items-center gap-3 min-w-0">
          <Link href={`/projects/${pid}`}><a className="btn-ghost" data-testid="button-back-project"><ArrowLeft size={14} /></a></Link>
          <div className="min-w-0">
            <div className="text-[11px] font-mono text-muted">{artifact.id} · {project.name}</div>
            <div className="text-sm font-semibold text-ink truncate">{artifact.title}</div>
          </div>
        </div>
        <div className="flex items-center gap-2 shrink-0">
          {savedAt && <div className="text-xs text-muted">Saved {savedAt.toLocaleTimeString()}</div>}
          <button onClick={save} disabled={saving} className="btn-primary" data-testid="button-save-artifact">
            <Save size={14} /> {saving ? 'Saving…' : 'Save'}
          </button>
          <a href={api.exportOneUrl(pid, aid)} className="btn" data-testid="button-download-docx">
            <Download size={14} /> DOCX
          </a>
        </div>
      </TopBar>
      <main className="p-6 flex-1 overflow-auto">
        <div className="max-w-4xl mx-auto space-y-4">
          {/* Purpose + when-to-use */}
          <div className="card p-4">
            <div className="text-xs uppercase tracking-wider text-muted mb-1">Purpose</div>
            <div className="text-sm text-ink">{artifact.purpose}</div>
            {artifact.when_to_use && (
              <>
                <div className="text-xs uppercase tracking-wider text-muted mt-3 mb-1">When to use</div>
                <div className="text-sm text-ink">{artifact.when_to_use}</div>
              </>
            )}
          </div>

          {/* Learning content */}
          {artifact.learning && (
            <div className="space-y-2">
              {artifact.learning.concepts && (
                <Section title="Key concepts" icon={BookOpen}>
                  {artifact.learning.concepts.map((c, i) => (
                    <div key={i} className="mb-2 last:mb-0">
                      <div className="text-sm font-medium text-ink">{c.term}</div>
                      <div className="text-sm text-muted">{c.definition}</div>
                    </div>
                  ))}
                </Section>
              )}
              {artifact.learning.how_to_use && (
                <Section title="How to use this artifact" icon={Compass}>
                  <ol className="list-decimal ml-5 space-y-1.5 text-sm">
                    {artifact.learning.how_to_use.map((step, i) => <li key={i}>{step}</li>)}
                  </ol>
                </Section>
              )}
              {artifact.learning.worked_example && (
                <Section title="Worked example" icon={Info}>
                  <div className="text-sm whitespace-pre-wrap">{artifact.learning.worked_example}</div>
                </Section>
              )}
              {artifact.learning.pitfalls && (
                <Section title="Common pitfalls" icon={AlertTriangle}>
                  <ul className="list-disc ml-5 space-y-1 text-sm">
                    {artifact.learning.pitfalls.map((p, i) => <li key={i}>{p}</li>)}
                  </ul>
                </Section>
              )}
              {activeOverlay && (
                <div className="card p-4 border-l-4 border-l-accent">
                  <div className="flex items-center gap-2 text-xs uppercase tracking-wider text-accent mb-1">
                    <Globe size={12} /> Domain overlay · {domain.replaceAll('_', ' ')}
                  </div>
                  <div className="text-sm whitespace-pre-wrap">{activeOverlay}</div>
                </div>
              )}
            </div>
          )}

          {/* Form fields */}
          <div className="card p-5">
            <div className="text-sm font-semibold text-ink mb-4">Fill-in fields</div>
            <div className="space-y-4">
              {(artifact.fields || []).map((f) => (
                <div key={f.key}>
                  <label className="text-xs font-medium text-ink block mb-1">
                    {f.label}
                    {f.help && <span className="text-muted font-normal ml-1">— {f.help}</span>}
                  </label>
                  <Field field={f} value={values[f.key]} onChange={(v) => setValues({ ...values, [f.key]: v })} />
                </div>
              ))}
              {(!artifact.fields || artifact.fields.length === 0) && (
                <div className="text-sm text-muted">This artifact has no fillable fields — only tables.</div>
              )}
            </div>
          </div>

          {/* Tables */}
          {(artifact.tables || []).map((t) => (
            <div key={t.key} className="card p-5">
              <TableEditor table={t} rows={tables[t.key] || []} onChange={(rows) => setTables({ ...tables, [t.key]: rows })} />
            </div>
          ))}

          <div className="flex items-center justify-end pt-2">
            <button onClick={save} disabled={saving} className="btn-primary" data-testid="button-save-bottom">
              <Save size={14} /> {saving ? 'Saving…' : 'Save changes'}
            </button>
          </div>
        </div>
      </main>
    </>
  );
}
