// AI Cost Architect — shared UI (sidebar, mobile toggle, picker)

(function () {
  // Detect base path so links work at /ai-cost-architect/ (project pages) and at root
  const scriptEl = document.currentScript || document.querySelector('script[src*="app.js"]');
  const scriptSrc = scriptEl ? scriptEl.getAttribute('src') : '';
  // scriptSrc looks like "../assets/app.js" or "assets/app.js" etc.
  // Base is the URL of "site/" — compute by resolving scriptSrc back to its "assets/" parent
  const scriptUrl = new URL(scriptEl.src, window.location.href);
  const baseUrl = new URL('../', scriptUrl); // one level up from /assets/
  window.ACA.base = baseUrl.pathname;
  window.ACA.url = (p) => baseUrl.pathname + p.replace(/^\//, '');

  // Render sidebar
  function renderSidebar(activeKey) {
    const B = window.ACA.url;
    const phaseLinks = window.ACA.phases
      .filter(p => p.num >= 1 && p.num <= 7)
      .map(p => `<li><a href="${B('phases/' + p.key + '.html')}" data-key="phase-${p.key}">
          Phase ${p.num} · ${p.name}
        </a></li>`).join('');
    return `
      <a class="brand" href="${B('index.html')}">
        <span class="brand-mark">A</span>
        <span>
          <span class="brand-name">AI Cost Architect</span><br>
          <span class="brand-sub">Cost architecture for enterprise AI</span>
        </span>
      </a>
      <div class="nav-group">
        <div class="nav-label">Get Started</div>
        <ul class="nav-list">
          <li><a href="${B('index.html')}" data-key="home">Overview</a></li>
          <li><a href="${B('methodology.html')}" data-key="methodology">Methodology</a></li>
          <li><a href="${B('roles.html')}" data-key="roles">Roles &amp; RACI</a></li>
        </ul>
      </div>
      <div class="nav-group">
        <div class="nav-label">Phases <span class="nav-count">7</span></div>
        <ul class="nav-list">${phaseLinks}</ul>
      </div>
      <div class="nav-group">
        <div class="nav-label">Reference</div>
        <ul class="nav-list">
          <li><a href="${B('artifacts/index.html')}" data-key="artifacts">All 21 Artifacts</a></li>
          <li><a href="${B('domains.html')}" data-key="domains">Domain Overlays</a></li>
          <li><a href="${B('governance.html')}" data-key="governance">Governance Cadence</a></li>
          <li><a href="${B('failure-modes.html')}" data-key="failures">Failure Modes</a></li>
        </ul>
      </div>
      <div class="nav-group">
        <div class="nav-label">Project</div>
        <ul class="nav-list">
          <li><a href="https://github.com/zestor/ai-cost-architect">GitHub Repository</a></li>
          <li><a href="${B('index.html')}#app">Portfolio App</a></li>
        </ul>
      </div>
    `;
  }

  function mountLayout(activeKey) {
    const sidebar = document.getElementById('sidebar');
    if (sidebar) sidebar.innerHTML = renderSidebar(activeKey);
    if (activeKey) {
      const target = document.querySelector(`[data-key="${activeKey}"]`);
      if (target) target.classList.add('active');
    }

    // Mobile menu toggle
    const toggle = document.getElementById('menu-toggle');
    const sidebarEl = document.querySelector('.sidebar');
    if (toggle && sidebarEl) {
      toggle.addEventListener('click', () => sidebarEl.classList.toggle('open'));
      document.addEventListener('click', (e) => {
        if (window.innerWidth <= 900 && !sidebarEl.contains(e.target) && !toggle.contains(e.target)) {
          sidebarEl.classList.remove('open');
        }
      });
    }

    // Auto-set year in footer
    document.querySelectorAll('[data-year]').forEach(el => el.textContent = new Date().getFullYear());
  }

  // Picker on home page
  function mountPicker() {
    const phaseSel = document.getElementById('picker-phase');
    const tierSel  = document.getElementById('picker-tier');
    const list     = document.getElementById('picker-artifacts');
    const summary  = document.getElementById('picker-summary');
    if (!phaseSel || !tierSel || !list) return;

    // Populate phase select
    window.ACA.phases.filter(p => p.num >= 1 && p.num <= 7).forEach(p => {
      const opt = document.createElement('option');
      opt.value = p.num;
      opt.textContent = `Phase ${p.num} — ${p.name} (${p.weeks})`;
      phaseSel.appendChild(opt);
    });

    function render() {
      const phase = Number(phaseSel.value);
      const tier  = tierSel.value;
      const items = window.ACA.artifacts.filter(a => a.phase === phase);
      const requiredIds = window.ACA.tiers[tier];
      const phaseData = window.ACA.phases.find(p => p.num === phase);

      list.innerHTML = '';
      items.forEach(a => {
        const isReq = requiredIds.includes(a.id);
        const li = document.createElement('li');
        li.innerHTML = `
          <a href="${window.ACA.url('artifacts/' + a.slug + '.html')}">
            <span>
              <span class="item-num mono">${a.id}</span>
              ${a.title}
            </span>
            <span class="item-req ${isReq ? '' : 'item-opt'}">${isReq ? 'Required' : 'Optional at ' + tier}</span>
          </a>
        `;
        list.appendChild(li);
      });
      if (summary) {
        const requiredCount = items.filter(a => requiredIds.includes(a.id)).length;
        summary.innerHTML = `<strong>Phase ${phase} · ${phaseData.name}</strong> — ${phaseData.purpose}
          <br><span class="text-muted text-small">Exit criteria: ${phaseData.exit}</span>
          <br><span class="text-small mono" style="color:var(--primary)">${requiredCount} required at ${tier}, ${items.length - requiredCount} optional</span>`;
      }
    }

    phaseSel.addEventListener('change', render);
    tierSel.addEventListener('change', render);
    phaseSel.value = 1;
    render();
  }

  window.ACA.mountLayout = mountLayout;
  window.ACA.mountPicker = mountPicker;
})();
