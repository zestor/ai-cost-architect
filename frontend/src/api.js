// Thin API client
// __PORT_8765__ is replaced by deploy_website with the proxy path at deploy time.
// In dev we hit the vite proxy at /api.
const PROXY = '__PORT_8765__';
const API = PROXY.startsWith('__') ? '/api' : `${PROXY}/api`;

async function request(path, opts = {}) {
  const res = await fetch(`${API}${path}`, {
    ...opts,
    headers: { 'Content-Type': 'application/json', ...(opts.headers || {}) },
  });
  if (!res.ok) {
    const txt = await res.text();
    throw new Error(`${res.status} ${res.statusText}: ${txt}`);
  }
  if (res.status === 204) return null;
  const ct = res.headers.get('content-type') || '';
  if (ct.includes('application/json')) return res.json();
  return res;
}

export const api = {
  listArtifacts: () => request('/artifacts'),
  getArtifact: (id) => request(`/artifacts/${id}`),
  listDomains: () => request('/domains'),
  listProjects: () => request('/projects'),
  createProject: (body) => request('/projects', { method: 'POST', body: JSON.stringify(body) }),
  getProject: (id) => request(`/projects/${id}`),
  updateProject: (id, body) => request(`/projects/${id}`, { method: 'PUT', body: JSON.stringify(body) }),
  deleteProject: (id) => request(`/projects/${id}`, { method: 'DELETE' }),
  getEntry: (pid, aid) => request(`/projects/${pid}/entries/${aid}`),
  upsertEntry: (pid, aid, body) => request(`/projects/${pid}/entries/${aid}`, { method: 'PUT', body: JSON.stringify(body) }),
  portfolioSummary: () => request('/portfolio/summary'),
  exportOneUrl: (pid, aid) => `${API}/projects/${pid}/export/${aid}`,
  exportAllUrl: (pid) => `${API}/projects/${pid}/export_all`,
  blankOneUrl: (aid) => `${API}/templates/blank/${aid}`,
  blankAllUrl: () => `${API}/templates/blank_all`,
};

export function downloadFile(url, filename) {
  const a = document.createElement('a');
  a.href = url;
  if (filename) a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
}
