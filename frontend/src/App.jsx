import { useEffect, useState } from 'react';
import { Router, Route, Switch, Link, useLocation } from 'wouter';
import { useHashLocation } from 'wouter/use-hash-location';
import { LayoutDashboard, FolderKanban, FileText, Library, Download } from 'lucide-react';
import Dashboard from './pages/Dashboard.jsx';
import Projects from './pages/Projects.jsx';
import ProjectDetail from './pages/ProjectDetail.jsx';
import ArtifactEditor from './pages/ArtifactEditor.jsx';
import TemplateLibrary from './pages/TemplateLibrary.jsx';
import ArtifactReference from './pages/ArtifactReference.jsx';

function Logo() {
  return (
    <div className="flex items-center gap-2">
      <svg viewBox="0 0 32 32" width="26" height="26" aria-label="FinOps AI logo">
        <rect x="2" y="2" width="28" height="28" rx="6" fill="#01696F" />
        <path d="M9 22 L14 12 L18 18 L23 10" stroke="white" strokeWidth="2.4" fill="none" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
      <div className="leading-tight">
        <div className="text-[13px] font-semibold text-ink">FinOps AI</div>
        <div className="text-[11px] text-muted -mt-0.5">Portfolio Manager</div>
      </div>
    </div>
  );
}

function Sidebar() {
  const [location] = useLocation();
  const nav = [
    { href: '/', label: 'Dashboard', icon: LayoutDashboard },
    { href: '/projects', label: 'Projects', icon: FolderKanban },
    { href: '/templates', label: 'Template library', icon: Library },
    { href: '/reference', label: 'Artifact reference', icon: FileText },
  ];
  const isActive = (h) => (h === '/' ? location === '/' : location.startsWith(h));
  return (
    <aside className="w-60 border-r border-border bg-surface2 flex flex-col shrink-0">
      <div className="px-4 py-4 border-b border-border">
        <Logo />
      </div>
      <nav className="flex-1 p-2 space-y-0.5">
        {nav.map((n) => {
          const Icon = n.icon;
          const active = isActive(n.href);
          return (
            <Link key={n.href} href={n.href}>
              <a
                className={
                  'flex items-center gap-2 px-3 py-2 rounded-md text-sm transition-colors ' +
                  (active ? 'bg-accent/10 text-accent font-medium' : 'text-ink/80 hover:bg-white')
                }
                data-testid={`nav-${n.label.toLowerCase().replace(/\s+/g, '-')}`}
              >
                <Icon size={16} />
                {n.label}
              </a>
            </Link>
          );
        })}
      </nav>
      <div className="p-3 border-t border-border">
        <div className="text-[11px] text-muted leading-relaxed">
          FinOps AI framework
          <br />
          21 reference artifacts · exportable to DOCX
        </div>
      </div>
    </aside>
  );
}

function TopBar({ children }) {
  return (
    <header className="h-14 border-b border-border bg-white/70 backdrop-blur px-6 flex items-center justify-between sticky top-0 z-10">
      {children}
    </header>
  );
}

export default function App() {
  const [ready, setReady] = useState(false);
  useEffect(() => setReady(true), []);
  return (
    <Router hook={useHashLocation}>
      <div className="min-h-screen flex bg-surface">
        <Sidebar />
        <div className="flex-1 flex flex-col min-w-0">
          {ready && (
            <Switch>
              <Route path="/" component={Dashboard} />
              <Route path="/projects" component={Projects} />
              <Route path="/projects/:pid" component={ProjectDetail} />
              <Route path="/projects/:pid/artifacts/:aid" component={ArtifactEditor} />
              <Route path="/templates" component={TemplateLibrary} />
              <Route path="/reference" component={ArtifactReference} />
              <Route path="/reference/:aid" component={ArtifactReference} />
              <Route>
                <div className="p-8 text-muted">Not found.</div>
              </Route>
            </Switch>
          )}
        </div>
      </div>
    </Router>
  );
}

export { TopBar };
