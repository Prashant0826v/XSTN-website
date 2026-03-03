/**
 * XSTN Authentication System
 * Handles signup, login, OTP verification, JWT token management, and auth state.
 */

const API_BASE = 'https://xstn-website-fvon.onrender.com';

// ==================== TOKEN MANAGEMENT ====================

function saveTokens(access, refresh) {
    localStorage.setItem('xstn_access_token', access);
    localStorage.setItem('xstn_refresh_token', refresh);
}

function getAccessToken() {
    return localStorage.getItem('xstn_access_token');
}

function getRefreshToken() {
    return localStorage.getItem('xstn_refresh_token');
}

function clearTokens() {
    localStorage.removeItem('xstn_access_token');
    localStorage.removeItem('xstn_refresh_token');
    localStorage.removeItem('xstn_user');
}

function saveUser(user) {
    localStorage.setItem('xstn_user', JSON.stringify(user));
}

function getUser() {
    const u = localStorage.getItem('xstn_user');
    return u ? JSON.parse(u) : null;
}

function isLoggedIn() {
    return !!getAccessToken();
}

function logout() {
    // Show confirmation popup
    const overlay = document.createElement('div');
    overlay.className = 'xstn-popup-overlay';
    overlay.innerHTML = `
        <div class="xstn-popup-box">
            <div class="xstn-popup-icon">
                <svg viewBox="0 0 52 52" class="popup-checkmark">
                    <circle cx="26" cy="26" r="25" fill="none" stroke="#f59e0b" stroke-width="2"/>
                    <text x="26" y="33" text-anchor="middle" fill="#f59e0b" font-size="24" font-weight="bold">?</text>
                </svg>
            </div>
            <h3 class="xstn-popup-title">Logout Confirmation</h3>
            <p class="xstn-popup-message">Are you sure you want to log out?</p>
            <div style="display:flex;gap:12px;justify-content:center;margin-top:10px;">
                <button id="confirmLogoutBtn" style="padding:10px 28px;border-radius:8px;border:none;background:linear-gradient(135deg,#ef4444,#dc2626);color:white;font-weight:600;cursor:pointer;font-size:14px;transition:all 0.3s;">Yes, Logout</button>
                <button id="cancelLogoutBtn" style="padding:10px 28px;border-radius:8px;border:1.5px solid rgba(255,255,255,0.2);background:transparent;color:white;font-weight:600;cursor:pointer;font-size:14px;transition:all 0.3s;">Cancel</button>
            </div>
        </div>
    `;
    document.body.appendChild(overlay);
    requestAnimationFrame(() => overlay.classList.add('active'));

    document.getElementById('confirmLogoutBtn').addEventListener('click', () => {
        overlay.classList.remove('active');
        setTimeout(() => overlay.remove(), 300);
        clearTokens();
        window.location.href = 'index.html';
    });

    document.getElementById('cancelLogoutBtn').addEventListener('click', () => {
        overlay.classList.remove('active');
        setTimeout(() => overlay.remove(), 300);
    });

    overlay.addEventListener('click', (e) => {
        if (e.target === overlay) {
            overlay.classList.remove('active');
            setTimeout(() => overlay.remove(), 300);
        }
    });
}

// Authenticated fetch helper
async function authFetch(url, options = {}) {
    const token = getAccessToken();
    if (!token) {
        window.location.href = 'login.html';
        return;
    }

    options.headers = {
        ...options.headers,
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    };

    let response = await fetch(url, options);

    // If 401, try refreshing the token
    if (response.status === 401) {
        const refreshed = await refreshAccessToken();
        if (refreshed) {
            options.headers['Authorization'] = `Bearer ${getAccessToken()}`;
            response = await fetch(url, options);
        } else {
            logout();
            return;
        }
    }

    return response;
}

async function refreshAccessToken() {
    const refresh = getRefreshToken();
    if (!refresh) return false;

    try {
        const response = await fetch(`${API_BASE}/api/token/refresh/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ refresh })
        });

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('xstn_access_token', data.access);
            return true;
        }
        return false;
    } catch {
        return false;
    }
}

// ==================== NAVBAR AUTH STATE ====================

function updateNavbar() {
    const navAuth = document.querySelector('.nav-auth');
    if (!navAuth) return;

    if (isLoggedIn()) {
        const user = getUser();
        const displayName = user ? (user.first_name || user.username || 'User') : 'User';
        navAuth.innerHTML = `
      <a href="dashboard.html" class="nav-profile-btn" title="My Profile">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
          <circle cx="12" cy="7" r="4"></circle>
        </svg>
        <span>${displayName}</span>
      </a>
      <a href="#" class="nav-logout-btn" onclick="logout(); return false;">Logout</a>
    `;
    }
}

// Run navbar update — call immediately since script is at end of body
try {
    updateNavbar();
} catch (e) {
    console.error('updateNavbar error:', e);
}

// ==================== PASSWORD HELPERS ====================

function togglePassword(fieldId) {
    const field = document.getElementById(fieldId);
    const btn = event.target;
    if (field.type === 'password') {
        field.type = 'text';
        btn.textContent = 'hide';
    } else {
        field.type = 'password';
        btn.textContent = 'show';
    }
}

function checkPasswordStrength() {
    const password = document.getElementById('signupPassword')?.value || '';
    const strengthFill = document.getElementById('strengthFill');
    const strengthText = document.getElementById('strengthText');
    if (!strengthFill || !strengthText) return;

    let strength = 0;
    const checks = {
        'req-length': password.length >= 8,
        'req-upper': /[A-Z]/.test(password),
        'req-number': /[0-9]/.test(password),
        'req-special': /[!@#$%^&*(),.?":{}|<>]/.test(password)
    };

    Object.entries(checks).forEach(([id, passed]) => {
        const el = document.getElementById(id);
        if (el) el.classList.toggle('active', passed);
        if (passed) strength += 25;
    });

    strengthFill.style.width = strength + '%';
    const levels = [
        { max: 25, text: 'Weak', color: '#ef4444' },
        { max: 50, text: 'Fair', color: '#f97316' },
        { max: 75, text: 'Good', color: '#eab308' },
        { max: 101, text: 'Strong', color: '#22c55e' }
    ];
    const level = levels.find(l => strength < l.max);
    strengthText.textContent = level.text;
    strengthFill.style.backgroundColor = level.color;
}

// ==================== SIGNUP ====================

const signupForm = document.getElementById('signupForm');
if (signupForm) {
    signupForm.addEventListener('submit', async function (e) {
        e.preventDefault();
        const form = this;
        const submitBtn = form.querySelector('.submit-btn');
        const errorDiv = document.getElementById('authError');

        // Clear previous errors
        if (errorDiv) errorDiv.style.display = 'none';

        const username = form.querySelector('input[name="username"]')?.value;
        const email = form.querySelector('input[name="email"]').value;
        const firstName = form.querySelector('input[name="first_name"]')?.value || '';
        const lastName = form.querySelector('input[name="last_name"]')?.value || '';
        const password = form.querySelector('input[name="password"]').value;
        const confirmPassword = form.querySelector('input[name="confirmPassword"]').value;

        // Client-side validation
        if (!username || !email || !password || !confirmPassword) {
            showErrorPopup('Please fill all required fields.');
            return;
        }
        if (password !== confirmPassword) {
            showErrorPopup('Passwords do not match.');
            return;
        }
        if (password.length < 8) {
            showErrorPopup('Password must be at least 8 characters.');
            return;
        }

        submitBtn.disabled = true;
        submitBtn.textContent = 'Creating Account...';

        try {
            const response = await fetch(`${API_BASE}/api/users/register/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    username,
                    email,
                    first_name: firstName,
                    last_name: lastName,
                    password,
                    confirm_password: confirmPassword
                })
            });

            const data = await response.json();

            if (response.ok) {
                // Store email for verification page
                localStorage.setItem('xstn_verify_email', email);
                showSuccessPopup(
                    'Account created! A verification code has been sent to your email.',
                    form
                );
                // Redirect to verify page after popup closes
                setTimeout(() => {
                    window.location.href = `verify.html?email=${encodeURIComponent(email)}`;
                }, 2500);
            } else {
                const errors = Object.values(data).flat().join('. ');
                showErrorPopup(errors || 'Registration failed. Please try again.');
            }
        } catch (error) {
            console.error('Signup error:', error);
            showErrorPopup('Network error. Please check your connection.');
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'JOIN XSTN →';
        }
    });
}

// ==================== LOGIN ====================

const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async function (e) {
        e.preventDefault();
        const form = this;
        const submitBtn = form.querySelector('.submit-btn');

        const email = form.querySelector('input[name="email"]').value;
        const password = form.querySelector('input[name="password"]').value;

        if (!email || !password) {
            showErrorPopup('Please enter email and password.');
            return;
        }

        submitBtn.disabled = true;
        submitBtn.textContent = 'Signing in...';

        try {
            // Get JWT tokens
            const response = await fetch(`${API_BASE}/api/token/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });

            if (response.ok) {
                const tokens = await response.json();
                saveTokens(tokens.access, tokens.refresh);

                // Fetch user profile
                const profileRes = await fetch(`${API_BASE}/api/users/me/`, {
                    headers: { 'Authorization': `Bearer ${tokens.access}` }
                });

                if (profileRes.ok) {
                    const user = await profileRes.json();
                    saveUser(user);
                }

                showSuccessPopup('Login successful! Redirecting to dashboard...', form);
                setTimeout(() => {
                    window.location.href = 'dashboard.html';
                }, 1500);
            } else {
                const data = await response.json();
                showErrorPopup(data.detail || 'Invalid email or password.');
            }
        } catch (error) {
            console.error('Login error:', error);
            showErrorPopup('Network error. Please check your connection.');
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'SIGN IN';
        }
    });
}

// ==================== EMAIL VALIDATION ====================

const emailInput = document.getElementById('signupEmail');
if (emailInput) {
    emailInput.addEventListener('input', function () {
        const emailCheck = document.getElementById('emailCheck');
        if (!emailCheck) return;
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (emailRegex.test(this.value)) {
            emailCheck.textContent = '✓';
            emailCheck.style.color = '#22c55e';
        } else {
            emailCheck.textContent = '';
        }
    });
}

// ==================== ERROR DISPLAY ====================

function showAuthError(message) {
    let errorDiv = document.getElementById('authError');
    if (!errorDiv) {
        errorDiv = document.createElement('div');
        errorDiv.id = 'authError';
        errorDiv.className = 'auth-error';
        const form = document.querySelector('.auth-form');
        if (form) form.parentNode.insertBefore(errorDiv, form);
    }
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';

    // Auto-hide after 5s
    setTimeout(() => {
        errorDiv.style.display = 'none';
    }, 5000);
}
