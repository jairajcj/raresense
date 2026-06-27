/**
 * RareSense.AI — API Client
 * Centralized API calls to the FastAPI backend
 */
const API_BASE = 'http://localhost:8000/api';

function getHeaders() {
  const token = localStorage.getItem('raresense_token');
  const headers = { 'Content-Type': 'application/json' };
  if (token) headers['Authorization'] = `Bearer ${token}`;
  return headers;
}

async function request(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;
  const res = await fetch(url, {
    headers: getHeaders(),
    ...options,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || 'API Error');
  }
  return res.json();
}

// Auth
export const api = {
  login: (data) => request('/auth/login', { method: 'POST', body: JSON.stringify(data) }),
  register: (data) => request('/auth/register', { method: 'POST', body: JSON.stringify(data) }),
  me: () => request('/auth/me'),

  // Patients
  getPatients: (params = '') => request(`/patients${params}`),
  getPatient: (id) => request(`/patients/${id}`),
  createPatient: (data) => request('/patients', { method: 'POST', body: JSON.stringify(data) }),
  updatePatient: (id, data) => request(`/patients/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  deletePatient: (id) => request(`/patients/${id}`, { method: 'DELETE' }),

  // Patient Portal
  getMyPatientProfile: () => request('/patients/me'),
  uploadPrescription: (formData) => {
    const token = localStorage.getItem('raresense_token');
    return fetch(`${API_BASE}/patients/me/upload-prescription`, {
      method: 'POST',
      headers: { ...(token ? { 'Authorization': `Bearer ${token}` } : {}) },
      body: formData
    }).then(res => {
      if (!res.ok) throw new Error('Upload failed');
      return res.json();
    });
  },
  updateClinicalNote: (id, data) => request(`/patients/notes/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  deleteClinicalNote: (id) => request(`/patients/notes/${id}`, { method: 'DELETE' }),

  // Clinical Notes
  getPatientNotes: (id) => request(`/patients/${id}/notes`),
  addNote: (patientId, data) => request(`/patients/${patientId}/notes`, { method: 'POST', body: JSON.stringify(data) }),
  getTimeline: (id) => request(`/patients/${id}/timeline`),

  // Diseases
  getDiseases: (params = '') => request(`/diseases${params}`),
  getDisease: (id) => request(`/diseases/${id}`),
  getCategories: () => request('/diseases/categories'),

  // Analytics
  getDashboard: () => request('/analytics/dashboard'),
  getSymptomFrequency: () => request('/analytics/symptom-frequency'),
  getDiseaseDistribution: () => request('/analytics/disease-distribution'),
  getTimelineDensity: () => request('/analytics/timeline-density'),
  getMatchAccuracy: () => request('/analytics/match-accuracy'),
  getRecentActivity: (limit = 20) => request(`/analytics/recent-activity?limit=${limit}`),
  getEntityBreakdown: () => request('/analytics/entity-breakdown'),

  // Search
  search: (q, page = 1) => request(`/search?q=${encodeURIComponent(q)}&page=${page}`),
  filterNotes: (params) => request(`/search/filter?${params}`),
  analyzeText: (text) => request('/search/analyze', { method: 'POST', body: JSON.stringify({ text }) }),
  getSpecialties: () => request('/search/specialties'),

  // Matching
  runMatching: (patientId, topK = 10) => request(`/match/${patientId}?top_k=${topK}`, { method: 'POST' }),
  getMatchResults: (patientId) => request(`/match/${patientId}/results`),
  updateMatchStatus: (matchId, status, notes = '') => request(`/match/${matchId}/status`, { method: 'PUT', body: JSON.stringify({ status, notes }) }),
  analyzeNote: (text) => request('/match/analyze-note', { method: 'POST', body: JSON.stringify({ text }) }),

  // Health
  health: () => request('/health'),
};
