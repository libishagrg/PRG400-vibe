const BASE = '/api';

function getToken() { return localStorage.getItem('access_token'); }

async function request(path, options = {}) {
  const headers = { 'Content-Type': 'application/json', ...options.headers };
  const token = getToken();
  if (token) headers['Authorization'] = `Bearer ${token}`;
  const res = await fetch(BASE + path, { ...options, headers });
  if (res.status === 401) { auth.logout(); return null; }
  return res;
}

const api = {
  async getFeaturedDestinations() {
    const r = await request('/destinations/featured/');
    return r.ok ? r.json() : [];
  },
  async getDestinations(params = '') {
    const r = await request(`/destinations/?${params}`);
    return r.ok ? r.json() : { results: [] };
  },
  async getDestination(id) {
    const r = await request(`/destinations/${id}/`);
    return r.ok ? r.json() : null;
  },
  async getFeaturedTours() {
    const r = await request('/tours/featured/');
    return r.ok ? r.json() : [];
  },
  async getTours(params = '') {
    const r = await request(`/tours/?${params}`);
    return r.ok ? r.json() : { results: [] };
  },
  async getTour(id) {
    const r = await request(`/tours/${id}/`);
    return r.ok ? r.json() : null;
  },
  async getTourDates(id) {
    const r = await request(`/tours/${id}/dates/`);
    return r.ok ? r.json() : [];
  },
  async getReviews(tourId) {
    const r = await request(`/reviews/?tour=${tourId}`);
    return r.ok ? r.json() : { results: [] };
  },
  async createReview(data) {
    return request('/reviews/', { method: 'POST', body: JSON.stringify(data) });
  },
  async getMyBookings() {
    const r = await request('/bookings/my_bookings/');
    return r && r.ok ? r.json() : [];
  },
  async createBooking(data) {
    return request('/bookings/', { method: 'POST', body: JSON.stringify(data) });
  },
  async cancelBooking(id) {
    return request(`/bookings/${id}/cancel/`, { method: 'POST' });
  },
  async login(email, password) {
    const r = await fetch(`${BASE}/auth/login/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });
    return r.json().then(d => ({ ok: r.ok, data: d }));
  },
  async register(data) {
    const r = await fetch(`${BASE}/auth/register/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return r.json().then(d => ({ ok: r.ok, data: d }));
  },
  async logout(refresh) {
    await request('/auth/logout/', { method: 'POST', body: JSON.stringify({ refresh }) });
  },
  async getProfile() {
    const r = await request('/auth/profile/');
    return r && r.ok ? r.json() : null;
  },
};
