import { useEffect, useState } from 'react';
import { Link, useRoute } from 'wouter';
import { api } from '../api.js';
import { TopBar } from '../App.jsx';
import { ArrowLeft, Download, BookOpen, Info, AlertTriangle, Compass, Globe, GitBranch, ListTree } from 'lucide-react';

const DOMAIN_LABELS = {
  generic: 'Generic (enterprise baseline)',
  banking: 'Banking & financial services',
  retail: 'Retail & e-commerce',
  energy_oil_gas: 'Energy, oil & gas',
  aerospace: 'Aerospace & defense',
  public_sector: 'Public sector',
  telecom: 'Telecommunications',
  entertainment: 'Media & entertainment',
};

function List({ items }) {
  return <ul className="list-disc ml-5 space-y-1 text-sm">{items.map((x, i) => <li key={i}>{x}</li>)}</ul>;
}

function ArtifactList({ artifacts, selectedId }) {
  return (
    <aside className="w-72 border-r border-border bg-white shrink-0 overflow-auto">
      <div className="px-4 py-3 border-b border-border">
        <div className="text-sm font-semibold text-ink">All 21 artifacts</div>
        <div className="text-xs text-muted">Reference-manual depth</div>
      </div>
      <div>
        {artifacts.map((a) => {
          const active = a.id === selectedId;
          return (
            <Link key={a.id} href={`/reference/${a.id}`}>
              <a
                className={`block px-4 py-2.5 border-b border-border text-sm hover:bg-surface2 transition-colors ${active ? 'bg-accent/10 text-accent' : 'text-ink'}`}
                data-testid={`link-ref-${a.id}`}
              >
                <div className="flex items-center gap-2">
                  <span className="text-[11px] font-mono opacity-70">{a.id}</span>
                  <span className="text-xs font-medium truncate">{a.short_title || a.title}</span>
                </div>
              </a>
            </Link>
          );
        })}
      </div>
    </aside>
  );
}

export default function ArtifactReference() {
  const [, params] = useRoute('/reference/:aid');
  const [, base] = useRoute('/reference');
  const [artifacts, setArtifacts] = useState([]);
  const [current, setCurrent] = useState(null);
  const aid = params?.aid;

  useEffect(() => {
    api.listArtifacts().then((list) => {
      setArtifacts(list);
      if (!aid && list.length > 0) {
        // no-op; UI shows empty state
      }
    });
  }, []);

  useEffect(() => {
    if (!aid) { setCurrent(null); return; }
    api.getArtifact(aid).then(setCurrent).catch(() => setCurrent(null));
  }, [aid]);

  return (
    <>
      <TopBar>
        <div className="flex items-center gap-3 min-w-0">
          {current && (
            <>
              <Link href="/reference"><a className="btn-ghost" data-testid="button-back-reference"><ArrowLeft size={14} /></a></Link>
              <div className="min-w-0">
                <div className="text-[11px] font-mono text-muted">{current.id}</div>
                <div className="text-sm font-semibold text-ink truncate">{current.title}</div>
              </div>
            </>
          )}
          {!current && (
            <div>
              <div className="text-sm font-semibold text-ink">Artifact reference</div>
              <div className="text-xs text-muted">Learn each artifact end-to-end — concepts, examples, pitfalls, domain overlays</div>
            </div>
          )}
        </div>
        {current && (
          <a href={api.blankOneUrl(current.id)} className="btn" data-testid="button-download-blank">
            <Download size={14} /> Blank DOCX
          </a>
        )}
      </TopBar>
      <div className="flex flex-1 min-h-0">
        <ArtifactList artifacts={artifacts} selectedId={aid} />
        <main className="flex-1 overflow-auto p-6">
          {!current && (
            <div className="max-w-2xl">
              <div className="card p-6">
                <BookOpen size={22} className="text-accent" />
                <div className="text-base font-semibold text-ink mt-2">Choose an artifact to open its reference</div>
                <div className="text-sm text-muted mt-1">
                  Each entry is written as a mini reference-manual for someone with no prior AI cost management or AI background:
                  key concepts, step-by-step how-to, a fully worked example, common pitfalls, decision tree, and eight
                  domain overlays (banking, retail, energy, aerospace, public sector, telecom, entertainment, generic).
                </div>
              </div>
            </div>
          )}
          {current && (
            <div className="max-w-4xl mx-auto space-y-4">
              <div className="card p-5">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-3">
                  <div>
                    <div className="text-xs uppercase tracking-wider text-muted">Purpose</div>
                    <div className="text-sm text-ink mt-1">{current.purpose}</div>
                  </div>
                  <div>
                    <div className="text-xs uppercase tracking-wider text-muted">When to use</div>
                    <div className="text-sm text-ink mt-1">{current.when_to_use || '—'}</div>
                  </div>
                  <div>
                    <div className="text-xs uppercase tracking-wider text-muted">Role context</div>
                    <div className="text-sm text-ink mt-1">{current.role_context || '—'}</div>
                  </div>
                  <div>
                    <div className="text-xs uppercase tracking-wider text-muted">Inputs needed</div>
                    <div className="text-sm text-ink mt-1">{Array.isArray(current.inputs_needed) ? current.inputs_needed.join(', ') : (current.inputs_needed || '—')}</div>
                  </div>
                </div>
              </div>

              {current.learning?.concepts && (
                <div className="card p-5">
                  <div className="flex items-center gap-2 mb-2"><BookOpen size={14} className="text-accent" /><h3 className="text-sm font-semibold text-ink">Key concepts</h3></div>
                  <div className="space-y-2">
                    {current.learning.concepts.map((c, i) => (
                      <div key={i}>
                        <div className="text-sm font-medium text-ink">{c.term}</div>
                        <div className="text-sm text-muted">{c.definition}</div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {current.learning?.how_to_use && (
                <div className="card p-5">
                  <div className="flex items-center gap-2 mb-2"><Compass size={14} className="text-accent" /><h3 className="text-sm font-semibold text-ink">How to use this artifact</h3></div>
                  <ol className="list-decimal ml-5 space-y-1.5 text-sm text-ink">
                    {current.learning.how_to_use.map((s, i) => <li key={i}>{s}</li>)}
                  </ol>
                </div>
              )}

              {current.learning?.worked_example && (
                <div className="card p-5">
                  <div className="flex items-center gap-2 mb-2"><Info size={14} className="text-accent" /><h3 className="text-sm font-semibold text-ink">Worked example</h3></div>
                  <div className="text-sm text-ink whitespace-pre-wrap">{current.learning.worked_example}</div>
                </div>
              )}

              {current.learning?.pitfalls && (
                <div className="card p-5">
                  <div className="flex items-center gap-2 mb-2"><AlertTriangle size={14} className="text-warn" /><h3 className="text-sm font-semibold text-ink">Common pitfalls</h3></div>
                  <List items={current.learning.pitfalls} />
                </div>
              )}

              {current.learning?.decision_tree && (
                <div className="card p-5">
                  <div className="flex items-center gap-2 mb-2"><GitBranch size={14} className="text-accent" /><h3 className="text-sm font-semibold text-ink">Decision tree</h3></div>
                  <div className="text-sm text-ink whitespace-pre-wrap font-mono bg-surface2 p-3 rounded-md">{current.learning.decision_tree}</div>
                </div>
              )}

              {current.learning?.domain_overlays && (
                <div className="card p-5">
                  <div className="flex items-center gap-2 mb-3"><Globe size={14} className="text-accent" /><h3 className="text-sm font-semibold text-ink">Domain overlays</h3></div>
                  <div className="space-y-4">
                    {Object.entries(current.learning.domain_overlays).map(([k, v]) => (
                      <div key={k}>
                        <div className="text-xs font-semibold uppercase tracking-wider text-accent">{DOMAIN_LABELS[k] || k}</div>
                        <div className="text-sm text-ink mt-1 whitespace-pre-wrap">{v}</div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {(current.fields?.length || current.tables?.length) && (
                <div className="card p-5">
                  <div className="flex items-center gap-2 mb-3"><ListTree size={14} className="text-accent" /><h3 className="text-sm font-semibold text-ink">Structure</h3></div>
                  {current.fields?.length > 0 && (
                    <>
                      <div className="text-xs uppercase tracking-wider text-muted">Fields ({current.fields.length})</div>
                      <ul className="mt-1 mb-3 grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-1 text-sm">
                        {current.fields.map((f) => (
                          <li key={f.key} className="text-ink"><span className="text-muted">{f.type}</span> · {f.label}</li>
                        ))}
                      </ul>
                    </>
                  )}
                  {current.tables?.length > 0 && (
                    <>
                      <div className="text-xs uppercase tracking-wider text-muted">Tables ({current.tables.length})</div>
                      <ul className="mt-1 space-y-1 text-sm text-ink">
                        {current.tables.map((t) => (
                          <li key={t.key}>
                            <span className="font-medium">{t.label}</span>
                            <span className="text-muted"> · {(t.columns || []).map((c) => c.label).join(', ')}</span>
                          </li>
                        ))}
                      </ul>
                    </>
                  )}
                </div>
              )}
            </div>
          )}
        </main>
      </div>
    </>
  );
}
