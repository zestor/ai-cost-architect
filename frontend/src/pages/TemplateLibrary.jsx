import { useEffect, useState } from 'react';
import { Link } from 'wouter';
import { api } from '../api.js';
import { TopBar } from '../App.jsx';
import { Download, FileText, Package } from 'lucide-react';

const STAGE_GROUPS = [
  { title: 'Foundations', ids: ['A01', 'A02', 'A03'], desc: 'Discovery, opportunity, governance intake' },
  { title: 'Design & Build', ids: ['A04', 'A05', 'A06', 'A07'], desc: 'Requirements, architecture, evaluation' },
  { title: 'Cost & Unit Economics', ids: ['A08', 'A09', 'A10', 'A11'], desc: 'TCO, unit cost, showback, forecasting' },
  { title: 'Operate & Govern', ids: ['A12', 'A13', 'A14', 'A15', 'A16'], desc: 'Runbook, incident, risk, MRM, drift' },
  { title: 'Scale & Executive', ids: ['A17', 'A18', 'A19', 'A20', 'A21'], desc: 'Portfolio, exec brief, RACI, playbook, close-out' },
];

export default function TemplateLibrary() {
  const [artifacts, setArtifacts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.listArtifacts().then(setArtifacts).finally(() => setLoading(false));
  }, []);

  const idx = Object.fromEntries(artifacts.map((a) => [a.id, a]));

  return (
    <>
      <TopBar>
        <div>
          <div className="text-sm font-semibold text-ink">Template library</div>
          <div className="text-xs text-muted">21 blank reference-manual artifacts, ready to download</div>
        </div>
        <div className="flex items-center gap-2">
          <a href={api.blankAllUrl()} className="btn-primary" data-testid="button-download-all-blank">
            <Package size={14} /> Download all 21 (zip)
          </a>
        </div>
      </TopBar>
      <main className="p-6 flex-1 overflow-auto">
        {loading && <div className="text-muted">Loading…</div>}
        {!loading && (
          <>
            <div className="card p-4 mb-6 flex items-start gap-3">
              <FileText size={20} className="text-accent shrink-0 mt-0.5" />
              <div className="text-sm text-ink">
                <div className="font-medium">Blank templates</div>
                <div className="text-muted text-xs mt-1">
                  Each artifact is a self-contained reference manual — concepts, worked example, pitfalls, decision tree,
                  and eight domain overlays (generic, banking, retail, energy & oil-and-gas, aerospace, public sector,
                  telecom, entertainment). To generate a filled version tied to a project's specific data, open the
                  project detail and export from there.
                </div>
              </div>
            </div>

            {STAGE_GROUPS.map((group) => (
              <section key={group.title} className="mb-8">
                <div className="flex items-baseline gap-3 mb-3">
                  <h2 className="text-sm font-semibold text-ink">{group.title}</h2>
                  <div className="text-xs text-muted">{group.desc}</div>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                  {group.ids.map((aid) => {
                    const a = idx[aid];
                    if (!a) return null;
                    return (
                      <div key={aid} className="card p-4" data-testid={`template-card-${aid}`}>
                        <div className="text-[11px] font-mono text-muted">{aid}</div>
                        <div className="text-sm font-medium text-ink mt-0.5 leading-snug">{a.title}</div>
                        <div className="text-xs text-muted mt-1.5 line-clamp-3">{a.purpose}</div>
                        <div className="flex items-center gap-1 mt-3">
                          <a href={api.blankOneUrl(aid)} className="btn text-xs flex-1 justify-center" data-testid={`button-blank-docx-${aid}`}>
                            <Download size={12} /> Blank DOCX
                          </a>
                          <Link href={`/reference/${aid}`}>
                            <a className="btn-ghost text-xs" data-testid={`button-preview-${aid}`}>Preview</a>
                          </Link>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </section>
            ))}
          </>
        )}
      </main>
    </>
  );
}
