const auth = {
  isLoggedIn() { return !!localStorage.getItem('access_token'); },
  getUser() {
    try { return JSON.parse(localStorage.getItem('user')); } catch { return null; }
  },
  save(data) {
    localStorage.setItem('access_token', data.access);
    localStorage.setItem('refresh_token', data.refresh);
    if (data.user) localStorage.setItem('user', JSON.stringify(data.user));
  },
  logout() {
    const refresh = localStorage.getItem('refresh_token');
    if (refresh) api.logout(refresh).catch(() => {});
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    updateNav();
    if (window.location.pathname.includes('bookings')) window.location.href = '/';
  },
};

function updateNav() {
  const links = document.getElementById('nav-auth-links');
  if (!links) return;
  if (auth.isLoggedIn()) {
    const user = auth.getUser();
    const name = user ? (user.first_name || user.username || user.email) : 'Account';
    links.innerHTML = `
      <a href="/bookings.html" class="text-white/80 hover:text-white transition">My Trips</a>
      <span class="text-white/60">|</span>
      <span class="text-white font-medium">${name}</span>
      <button onclick="auth.logout()" class="bg-white/20 hover:bg-white/30 text-white px-4 py-1.5 rounded-full text-sm transition">Logout</button>
    `;
  } else {
    links.innerHTML = `
      <button onclick="openModal('login')" class="text-white/80 hover:text-white transition">Login</button>
      <button onclick="openModal('register')" class="bg-white text-emerald-600 px-4 py-1.5 rounded-full text-sm font-semibold hover:bg-emerald-50 transition">Sign Up</button>
    `;
  }
}

function requireAuth(cb) {
  if (auth.isLoggedIn()) { cb(); return; }
  openModal('login');
}
