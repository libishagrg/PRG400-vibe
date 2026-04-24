// Shared modal HTML injected into every page
function injectAuthModal() {
  const el = document.createElement('div');
  el.innerHTML = `
  <div id="auth-modal" class="fixed inset-0 z-50 hidden items-center justify-center bg-black/60 backdrop-blur-sm">
    <div class="bg-white rounded-2xl shadow-2xl w-full max-w-md mx-4 overflow-hidden">
      <div class="flex border-b">
        <button id="tab-login" onclick="switchTab('login')" class="flex-1 py-4 font-semibold text-emerald-600 border-b-2 border-emerald-600 transition">Login</button>
        <button id="tab-register" onclick="switchTab('register')" class="flex-1 py-4 font-semibold text-gray-400 hover:text-gray-600 transition">Sign Up</button>
      </div>

      <!-- Login Form -->
      <div id="form-login" class="p-8">
        <h2 class="text-2xl font-bold text-gray-800 mb-6">Welcome back</h2>
        <form onsubmit="handleLogin(event)">
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input id="login-email" type="email" required class="w-full border border-gray-300 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-emerald-400" placeholder="you@example.com">
          </div>
          <div class="mb-6">
            <label class="block text-sm font-medium text-gray-700 mb-1">Password</label>
            <input id="login-password" type="password" required class="w-full border border-gray-300 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-emerald-400" placeholder="••••••••">
          </div>
          <div id="login-error" class="text-red-500 text-sm mb-3 hidden"></div>
          <button type="submit" class="w-full bg-emerald-500 hover:bg-emerald-600 text-white py-3 rounded-xl font-semibold transition">Login</button>
        </form>
        <p class="text-center text-sm text-gray-500 mt-4">No account? <button onclick="switchTab('register')" class="text-emerald-600 font-semibold">Sign up free</button></p>
      </div>

      <!-- Register Form -->
      <div id="form-register" class="p-8 hidden">
        <h2 class="text-2xl font-bold text-gray-800 mb-6">Create account</h2>
        <form onsubmit="handleRegister(event)">
          <div class="grid grid-cols-2 gap-3 mb-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">First name</label>
              <input id="reg-first" type="text" class="w-full border border-gray-300 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-emerald-400" placeholder="Jane">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Last name</label>
              <input id="reg-last" type="text" class="w-full border border-gray-300 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-emerald-400" placeholder="Doe">
            </div>
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">Username</label>
            <input id="reg-username" type="text" required class="w-full border border-gray-300 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-emerald-400" placeholder="janedoe">
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input id="reg-email" type="email" required class="w-full border border-gray-300 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-emerald-400" placeholder="you@example.com">
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">Password</label>
            <input id="reg-password" type="password" required class="w-full border border-gray-300 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-emerald-400" placeholder="••••••••">
          </div>
          <div class="mb-6">
            <label class="block text-sm font-medium text-gray-700 mb-1">Confirm password</label>
            <input id="reg-password2" type="password" required class="w-full border border-gray-300 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-emerald-400" placeholder="••••••••">
          </div>
          <div id="reg-error" class="text-red-500 text-sm mb-3 hidden"></div>
          <button type="submit" class="w-full bg-emerald-500 hover:bg-emerald-600 text-white py-3 rounded-xl font-semibold transition">Create Account</button>
        </form>
        <p class="text-center text-sm text-gray-500 mt-4">Already have an account? <button onclick="switchTab('login')" class="text-emerald-600 font-semibold">Login</button></p>
      </div>

      <button onclick="closeModal()" class="absolute top-4 right-4 text-gray-400 hover:text-gray-600 text-2xl leading-none">&times;</button>
    </div>
  </div>`;
  document.body.appendChild(el);
}

function openModal(tab = 'login') {
  const modal = document.getElementById('auth-modal');
  modal.classList.remove('hidden');
  modal.classList.add('flex');
  switchTab(tab);
}
function closeModal() {
  const modal = document.getElementById('auth-modal');
  modal.classList.add('hidden');
  modal.classList.remove('flex');
}
function switchTab(tab) {
  document.getElementById('form-login').classList.toggle('hidden', tab !== 'login');
  document.getElementById('form-register').classList.toggle('hidden', tab !== 'register');
  document.getElementById('tab-login').className = tab === 'login'
    ? 'flex-1 py-4 font-semibold text-emerald-600 border-b-2 border-emerald-600 transition'
    : 'flex-1 py-4 font-semibold text-gray-400 hover:text-gray-600 transition';
  document.getElementById('tab-register').className = tab === 'register'
    ? 'flex-1 py-4 font-semibold text-emerald-600 border-b-2 border-emerald-600 transition'
    : 'flex-1 py-4 font-semibold text-gray-400 hover:text-gray-600 transition';
}

async function handleLogin(e) {
  e.preventDefault();
  const btn = e.target.querySelector('button[type=submit]');
  btn.disabled = true; btn.textContent = 'Logging in…';
  const errEl = document.getElementById('login-error');
  errEl.classList.add('hidden');
  const res = await api.login(
    document.getElementById('login-email').value,
    document.getElementById('login-password').value,
  );
  if (res.ok) {
    auth.save(res.data);
    closeModal();
    updateNav();
    if (typeof onLoginSuccess === 'function') onLoginSuccess();
  } else {
    errEl.textContent = res.data.detail || 'Invalid credentials.';
    errEl.classList.remove('hidden');
  }
  btn.disabled = false; btn.textContent = 'Login';
}

async function handleRegister(e) {
  e.preventDefault();
  const btn = e.target.querySelector('button[type=submit]');
  btn.disabled = true; btn.textContent = 'Creating…';
  const errEl = document.getElementById('reg-error');
  errEl.classList.add('hidden');
  const res = await api.register({
    username: document.getElementById('reg-username').value,
    email: document.getElementById('reg-email').value,
    password: document.getElementById('reg-password').value,
    password2: document.getElementById('reg-password2').value,
    first_name: document.getElementById('reg-first').value,
    last_name: document.getElementById('reg-last').value,
  });
  if (res.ok) {
    switchTab('login');
    document.getElementById('login-email').value = document.getElementById('reg-email').value;
    errEl.classList.add('hidden');
    document.getElementById('login-error').textContent = '';
    alert('Account created! Please log in.');
  } else {
    const msgs = Object.values(res.data).flat().join(' ');
    errEl.textContent = msgs || 'Registration failed.';
    errEl.classList.remove('hidden');
  }
  btn.disabled = false; btn.textContent = 'Create Account';
}

// Shared nav HTML
function injectNav(activePage) {
  const pages = [
    { href: '/', label: 'Home' },
    { href: '/destinations.html', label: 'Destinations' },
    { href: '/tours.html', label: 'Tours' },
  ];
  const links = pages.map(p => {
    const active = p.href === activePage;
    return `<a href="${p.href}" class="${active ? 'text-white font-semibold' : 'text-white/70 hover:text-white'} transition">${p.label}</a>`;
  }).join('');
  return `
  <nav class="fixed top-0 left-0 right-0 z-40 bg-emerald-700/95 backdrop-blur-sm shadow-lg">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between h-16">
      <a href="/" class="text-white font-bold text-xl flex items-center gap-2">
        <span class="text-2xl">✈️</span> WanderLust
      </a>
      <div class="hidden md:flex items-center gap-8">${links}</div>
      <div class="flex items-center gap-4" id="nav-auth-links"></div>
    </div>
  </nav>`;
}

// Render star rating
function stars(rating) {
  const r = parseFloat(rating) || 0;
  const full = Math.floor(r);
  const half = r % 1 >= 0.5;
  let s = '';
  for (let i = 0; i < 5; i++) {
    if (i < full) s += '<span class="text-yellow-400">★</span>';
    else if (i === full && half) s += '<span class="text-yellow-300">★</span>';
    else s += '<span class="text-gray-300">★</span>';
  }
  return s;
}

function difficultyBadge(d) {
  const colors = { easy: 'bg-green-100 text-green-700', moderate: 'bg-yellow-100 text-yellow-700', challenging: 'bg-orange-100 text-orange-700', extreme: 'bg-red-100 text-red-700' };
  return `<span class="px-2 py-0.5 rounded-full text-xs font-semibold ${colors[d] || 'bg-gray-100 text-gray-600'}">${d}</span>`;
}

function categoryIcon(c) {
  const icons = { adventure: '🧗', cultural: '🏛️', wildlife: '🦁', beach: '🏖️', city: '🏙️', food: '🍜', photography: '📷', wellness: '🧘' };
  return icons[c] || '🗺️';
}

function formatPrice(p) {
  return '$' + parseFloat(p).toLocaleString('en-US', { minimumFractionDigits: 0 });
}

function tourCard(t) {
  return `
  <a href="/tour.html?id=${t.id}" class="bg-white rounded-2xl shadow-md hover:shadow-xl transition-all duration-300 overflow-hidden group block">
    <div class="relative overflow-hidden h-52">
      <img src="${t.image_url || 'https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=600'}"
           alt="${t.title}" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
      ${t.discount_percent ? `<span class="absolute top-3 left-3 bg-red-500 text-white text-xs font-bold px-2 py-1 rounded-full">${t.discount_percent}% OFF</span>` : ''}
      <span class="absolute top-3 right-3 bg-black/50 text-white text-xs px-2 py-1 rounded-full">${t.duration_days} days</span>
    </div>
    <div class="p-5">
      <div class="flex items-center gap-2 text-sm text-gray-500 mb-2">
        <span>${categoryIcon(t.category)} ${t.category_display || t.category}</span>
        <span>·</span>
        <span>📍 ${t.destination_name}, ${t.destination_country}</span>
      </div>
      <h3 class="font-bold text-gray-800 text-lg leading-tight mb-3 group-hover:text-emerald-600 transition">${t.title}</h3>
      <div class="flex items-center justify-between">
        <div>
          ${t.discount_percent
            ? `<span class="text-gray-400 line-through text-sm">${formatPrice(t.price_per_person)}</span>
               <span class="text-emerald-600 font-bold text-lg ml-1">${formatPrice(t.discounted_price)}</span>`
            : `<span class="text-emerald-600 font-bold text-lg">${formatPrice(t.price_per_person)}</span>`
          }
          <span class="text-gray-400 text-sm">/person</span>
        </div>
        <div class="flex items-center gap-1 text-sm">${stars(t.rating)}<span class="text-gray-500 ml-1">(${t.total_reviews})</span></div>
      </div>
    </div>
  </a>`;
}

function destinationCard(d) {
  return `
  <a href="/tours.html?destination=${d.id}" class="relative overflow-hidden rounded-2xl group h-64 block shadow-md hover:shadow-xl transition">
    <img src="${d.image_url || 'https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=600'}"
         alt="${d.name}" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500">
    <div class="absolute inset-0 bg-gradient-to-t from-black/70 via-black/20 to-transparent"></div>
    <div class="absolute bottom-0 left-0 p-5 text-white">
      <h3 class="text-xl font-bold">${d.name}</h3>
      <p class="text-white/80 text-sm">📍 ${d.country}</p>
    </div>
  </a>`;
}

function showToast(msg, type = 'success') {
  const t = document.createElement('div');
  t.className = `fixed bottom-6 right-6 z-50 px-6 py-3 rounded-xl shadow-lg text-white font-medium transition-all ${type === 'success' ? 'bg-emerald-500' : 'bg-red-500'}`;
  t.textContent = msg;
  document.body.appendChild(t);
  setTimeout(() => t.remove(), 3500);
}
