const API_BASE_URL = 'https://xstn-website-fvon.onrender.com';

document.addEventListener('DOMContentLoaded', async () => {
    // 1. Check Authentication & Authorization
    if (!isLoggedIn()) {
        window.location.href = 'login.html';
        return;
    }

    try {
        const response = await authFetch(`${API_BASE_URL}/api/users/me/`);
        if (!response.ok) throw new Error('Not authenticated');
        const user = await response.json();

        // Simple check: Assuming staff/admin status allows viewing. 
        // If not explicit in user model, we rely on backend API 403 blocks.
        document.getElementById('adminName').textContent = user.first_name || user.username || 'Admin';
    } catch (error) {
        console.error("Auth check failed:", error);
        window.location.href = 'login.html';
        return;
    }

    // 2. Tab Switching Logic
    const navLinks = document.querySelectorAll('.nav-links li');
    const tabContents = document.querySelectorAll('.tab-content');
    const pageTitle = document.getElementById('pageTitle');

    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            // Remove active class from all
            navLinks.forEach(l => l.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            // Add active class to clicked
            link.classList.add('active');
            const targetId = link.getAttribute('data-tab');
            document.getElementById(targetId).classList.add('active');
            pageTitle.textContent = link.textContent;

            // Load data for the specific tab
            loadTabData(targetId);
        });
    });

    // 3. Modal Logic
    const modal = document.getElementById('detailsModal');
    document.querySelector('.close-btn').addEventListener('click', () => {
        modal.classList.remove('show');
    });
    window.addEventListener('click', (e) => {
        if (e.target === modal) modal.classList.remove('show');
    });

    // Load initial dashboard data
    loadTabData('dashboard');
});

// Main Data Fetcher
async function loadTabData(tabId) {
    switch (tabId) {
        case 'dashboard':
            await loadDashboardStats();
            break;
        case 'contact':
            await loadContactForms();
            break;
        case 'inquiries':
            await loadInquiries();
            break;
        case 'internships':
            await loadInternships();
            break;
        case 'developers':
            await loadDevelopers();
            break;
        case 'testimonials':
            await loadTestimonials();
            break;
        case 'join':
            await loadJoinApps();
            break;
    }
}

// FORMATTERS
const formatDate = (isoString) => new Date(isoString).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
const getBadgeHTML = (status) => {
    let type = status.toLowerCase();
    if (type === 'false' || type === 'unread') type = 'unread';
    if (type === 'true' || type === 'read') type = 'read';
    return `<span class="badge ${type}">${status}</span>`;
};

// LOADERS
let dashboardChartInstance = null;

async function loadDashboardStats() {
    try {
        const [inq, intern, dev, test] = await Promise.all([
            authFetch(`${API_BASE_URL}/api/forms/inquiry-forms/`).then(r => r.json()),
            authFetch(`${API_BASE_URL}/api/forms/internship-applications/`).then(r => r.json()),
            authFetch(`${API_BASE_URL}/api/forms/developer-applications/`).then(r => r.json()),
            authFetch(`${API_BASE_URL}/api/forms/testimonials/`).then(r => r.json())
        ]);

        const inqCount = Array.isArray(inq) ? inq.length : 0;
        const internCount = Array.isArray(intern) ? intern.filter(i => i.status === 'pending').length : 0;
        const devCount = Array.isArray(dev) ? dev.filter(d => d.status === 'pending').length : 0;
        const testCount = Array.isArray(test) ? test.filter(t => !t.is_approved).length : 0;

        document.getElementById('statInquiries').textContent = inqCount;
        document.getElementById('statInterns').textContent = internCount;
        document.getElementById('statDevelopers').textContent = devCount;
        document.getElementById('statTestimonials').textContent = testCount;

        // Render Chart.js
        renderChart(inqCount, internCount, devCount);

    } catch (e) {
        console.error("Dashboard stats error:", e);
    }
}

function renderChart(inquiries, interns, developers) {
    const ctx = document.getElementById('dashboardChart').getContext('2d');

    if (dashboardChartInstance) {
        dashboardChartInstance.destroy();
    }

    // Gradient for bars
    const gradientBlue = ctx.createLinearGradient(0, 0, 0, 400);
    gradientBlue.addColorStop(0, 'rgba(14, 165, 233, 0.8)');
    gradientBlue.addColorStop(1, 'rgba(14, 165, 233, 0.2)');

    const gradientPurple = ctx.createLinearGradient(0, 0, 0, 400);
    gradientPurple.addColorStop(0, 'rgba(139, 92, 246, 0.8)');
    gradientPurple.addColorStop(1, 'rgba(139, 92, 246, 0.2)');

    dashboardChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Project Inquiries', 'Pending Interns', 'Pending Developers'],
            datasets: [{
                label: 'Active Requests',
                data: [inquiries, interns, developers],
                backgroundColor: [gradientPurple, gradientBlue, gradientBlue],
                borderRadius: 8,
                borderWidth: 0,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.9)',
                    titleColor: '#f8fafc',
                    bodyColor: '#cbd5f5',
                    padding: 12,
                    cornerRadius: 8,
                    displayColors: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)',
                        drawBorder: false
                    },
                    ticks: {
                        color: '#94a3b8',
                        font: { family: "'Inter', sans-serif" }
                    }
                },
                x: {
                    grid: { display: false },
                    ticks: {
                        color: '#94a3b8',
                        font: { family: "'Inter', sans-serif" }
                    }
                }
            }
        }
    });
}

async function loadContactForms() {
    try {
        const res = await authFetch(`${API_BASE_URL}/api/forms/contact-forms/`);
        const data = await res.json();
        const tbody = document.getElementById('contactTableBody');
        tbody.innerHTML = '';

        if (!Array.isArray(data)) return;

        data.forEach(item => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${formatDate(item.created_at)}</td>
                <td>${item.name}</td>
                <td>${item.email}</td>
                <td>${item.subject}</td>
                <td>${getBadgeHTML(item.is_read ? 'Read' : 'Unread')}</td>
                <td>
                    <button class="action-btn" onclick='viewDetails(${JSON.stringify(item)}, "contact")'>View</button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (e) { console.error(e); }
}

async function loadInquiries() {
    try {
        const res = await authFetch(`${API_BASE_URL}/api/forms/inquiry-forms/`);
        const data = await res.json();
        const tbody = document.getElementById('inquiriesTableBody');
        tbody.innerHTML = '';

        if (!Array.isArray(data)) return;

        data.forEach(item => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${formatDate(item.created_at)}</td>
                <td>${item.company || item.name}</td>
                <td>${item.project_type}</td>
                <td>${item.budget_range}</td>
                <td>${getBadgeHTML(item.is_read ? 'Read' : 'Unread')}</td>
                <td><button class="action-btn" onclick='viewDetails(${JSON.stringify(item)}, "inquiry")'>View</button></td>
            `;
            tbody.appendChild(tr);
        });
    } catch (e) { console.error(e); }
}

async function loadInternships() {
    try {
        const res = await authFetch(`${API_BASE_URL}/api/forms/internship-applications/`);
        const data = await res.json();
        const tbody = document.getElementById('internshipsTableBody');
        tbody.innerHTML = '';

        if (!Array.isArray(data)) return;

        data.forEach(item => {
            const linksHtml = `
                ${item.portfolio_url ? `<a href="${item.portfolio_url}" target="_blank">Portfolio</a><br>` : ''}
                ${item.resume_url ? `<a href="${item.resume_url}" target="_blank">Resume</a>` : ''}
            `;
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${formatDate(item.created_at)}</td>
                <td>${item.full_name}</td>
                <td>${item.university}</td>
                <td>${getBadgeHTML(item.status)}</td>
                <td>${linksHtml}</td>
                <td><button class="action-btn" onclick='viewDetails(${JSON.stringify(item)}, "internship")'>View / Action</button></td>
            `;
            tbody.appendChild(tr);
        });
    } catch (e) { console.error(e); }
}

async function loadDevelopers() {
    try {
        const res = await authFetch(`${API_BASE_URL}/api/forms/developer-applications/`);
        const data = await res.json();
        const tbody = document.getElementById('developersTableBody');
        tbody.innerHTML = '';

        if (!Array.isArray(data)) return;

        data.forEach(item => {
            const linksHtml = `
                ${item.portfolio_url ? `<a href="${item.portfolio_url}" target="_blank">Portfolio</a><br>` : ''}
                ${item.github_url ? `<a href="${item.github_url}" target="_blank">GitHub</a><br>` : ''}
                ${item.resume_url ? `<a href="${item.resume_url}" target="_blank">Resume</a>` : ''}
            `;
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${formatDate(item.created_at)}</td>
                <td>${item.full_name}</td>
                <td>${item.role_interested}</td>
                <td>${getBadgeHTML(item.status)}</td>
                <td>${linksHtml}</td>
                <td><button class="action-btn" onclick='viewDetails(${JSON.stringify(item)}, "developer")'>View / Action</button></td>
            `;
            tbody.appendChild(tr);
        });
    } catch (e) { console.error(e); }
}

async function loadTestimonials() {
    try {
        const res = await authFetch(`${API_BASE_URL}/api/forms/testimonials/`);
        const data = await res.json();
        const tbody = document.getElementById('testimonialsTableBody');
        tbody.innerHTML = '';

        if (!Array.isArray(data)) return;

        data.forEach(item => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${formatDate(item.created_at)}</td>
                <td>${item.name}</td>
                <td>${item.rating} ★</td>
                <td>${item.message.substring(0, 50)}...</td>
                <td>${getBadgeHTML(item.is_approved ? 'Approved' : 'Pending')}</td>
                <td><button class="action-btn" onclick='viewDetails(${JSON.stringify(item)}, "testimonial")'>Action</button></td>
            `;
            tbody.appendChild(tr);
        });
    } catch (e) { console.error(e); }
}

async function loadJoinApps() {
    try {
        const res = await authFetch(`${API_BASE_URL}/api/forms/join-applications/`);
        const data = await res.json();
        const tbody = document.getElementById('joinTableBody');
        tbody.innerHTML = '';

        if (!Array.isArray(data)) return;

        data.forEach(item => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${formatDate(item.created_at)}</td>
                <td>${item.full_name}</td>
                <td>${item.role_interested}</td>
                <td>${getBadgeHTML(item.status)}</td>
                <td><button class="action-btn" onclick='viewDetails(${JSON.stringify(item)}, "join")'>View</button></td>
            `;
            tbody.appendChild(tr);
        });
    } catch (e) { console.error(e); }
}

// MODAL VIEW LOGIC
function viewDetails(data, type) {
    const modal = document.getElementById('detailsModal');
    const modalTitle = document.getElementById('modalTitle');
    const modalBody = document.getElementById('modalBody');
    const modalActions = document.getElementById('modalActions');

    modalTitle.textContent = `${type.toUpperCase()} Details`;

    let html = '';
    for (const [key, value] of Object.entries(data)) {
        if (key === 'id') continue;
        let displayVal = value;
        if (typeof value === 'boolean') displayVal = value ? 'Yes' : 'No';
        if (typeof value === 'string' && value.startsWith('http')) {
            displayVal = `<a href="${value}" target="_blank">View Link &rarr;</a>`;
        }

        html += `
            <div class="detail-row">
                <span class="detail-label">${key.replace(/_/g, ' ').toUpperCase()}</span>
                <span class="detail-value">${displayVal || '-'}</span>
            </div>
        `;
    }
    modalBody.innerHTML = html;

    // Actions
    modalActions.innerHTML = '';

    if (type === 'contact' || type === 'inquiry') {
        const endpoint = type === 'contact' ? 'contact-forms' : 'inquiry-forms';
        if (!data.is_read) {
            modalActions.innerHTML = `<button class="action-btn primary" onclick='updateEntity("${endpoint}", ${data.id}, {is_read: true}, "${type}")'>Mark as Read</button>`;
        }
    } else if (type === 'internship' || type === 'developer' || type === 'join') {
        const endpoint = type === 'internship' ? 'internship-applications' : (type === 'developer' ? 'developer-applications' : 'join-applications');
        if (data.status === 'pending' || data.status === 'reviewed') {
            modalActions.innerHTML = `
                <button class="action-btn primary" onclick='updateEntity("${endpoint}", ${data.id}, {status: "reviewed"}, "${type}")'>Mark Reviewed</button>
                <button class="action-btn success" onclick='updateEntity("${endpoint}", ${data.id}, {status: "${type === 'join' ? 'accepted' : 'selected'}"}, "${type}")'>Approve</button>
                <button class="action-btn danger" onclick='updateEntity("${endpoint}", ${data.id}, {status: "rejected"}, "${type}")'>Reject</button>
            `;
        }
    } else if (type === 'testimonial') {
        if (!data.is_approved) {
            modalActions.innerHTML = `<button class="action-btn success" onclick='updateEntity("testimonials", ${data.id}, {is_approved: true}, "testimonial")'>Approve Publish</button>`;
        }
    }

    modal.classList.add('show');
}

// UPDATE LOGIC
async function updateEntity(endpoint, id, payload, type) {
    try {
        const res = await authFetch(`${API_BASE_URL}/api/forms/${endpoint}/${id}/`, {
            method: 'PATCH',
            body: JSON.stringify(payload)
        });

        if (res.ok) {
            document.getElementById('detailsModal').classList.remove('show');
            // Reload the current tab
            loadTabData(type + 's'); // hacky pluralization, handles most cases above or specific tab maps
            if (type === 'contact') loadTabData('contact');
            if (type === 'inquiry') loadTabData('inquiries');
            if (type === 'join') loadTabData('join');
        } else {
            alert('Failed to update.');
        }
    } catch (e) {
        console.error(e);
        alert('Error updating.');
    }
}
