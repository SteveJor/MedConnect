// src/js/api.js
const API_BASE = '/api'; // ou 'http://127.0.0.1:8000/api'

export function loginUser(credentials) {
  return $.ajax({
    url: `${API_BASE}/login/`,
    method: 'POST',
    data: credentials,
  });
}
