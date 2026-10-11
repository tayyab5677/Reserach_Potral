/**
 * app.js — Frontend Logic for Research Opportunity Portal
 * ==========================================================
 * Handles all CRUD operations via fetch(), DOM manipulation,
 * view switching, client-side validation, and user feedback.
 *
 * No data is hard-coded — everything comes from the REST API.
 */

// ============================================================
// Configuration
// ============================================================
const API_BASE = 'http://localhost:5000/api/opportunities';

// ============================================================
// DOM Element References
// ============================================================
const listView       = document.getElementById('list-view');
const detailView     = document.getElementById('detail-view');
const formView       = document.getElementById('form-view');
const oppGrid        = document.getElementById('opportunities-grid');
const detailContent  = document.getElementById('detail-content');
const alertContainer = document.getElementById('alert-container');
const loadingSpinner = document.getElementById('loading-spinner');
const emptyState     = document.getElementById('empty-state');
const oppForm        = document.getElementById('opportunity-form');
const formTitle      = document.getElementById('form-title');
const formSubmitBtn  = document.getElementById('form-submit-btn');
const deleteModal    = new bootstrap.Modal(document.getElementById('deleteModal'));
const statTotal      = document.getElementById('stat-total');
const statOpen       = document.getElementById('stat-open');
const statClosed     = document.getElementById('stat-closed');

// Form field references
const formFields = {
    id:       document.getElementById('form-id'),
    title:    document.getElementById('form-title-input'),
    area:     document.getElementById('form-area'),
    faculty:  document.getElementById('form-faculty'),
    dept:     document.getElementById('form-dept'),
    skills:   document.getElementById('form-skills'),
    desc:     document.getElementById('form-desc'),
    positions: document.getElementById('form-positions'),
    deadline: document.getElementById('form-deadline'),
};

// State
let allOpportunities = [];     // Cached list from API
let currentFilter = 'all';     // Active filter: all | Open | Closed
let deleteTargetId = null;     // ID of opportunity pending deletion
let deleteTargetTitle = '';    // Title of opportunity pending deletion


// ============================================================
// View Management — Show one view, hide the others
// ============================================================
function showView(view) {
    listView.classList.add('d-none');
    detailView.classList.add('d-none');
    formView.classList.add('d-none');
    view.classList.remove('d-none');

    // Scroll to top smoothly
    window.scrollTo({ top: 0, behavior: 'smooth' });
}


// ============================================================
// Alert / Notification System
// ============================================================
function showAlert(message, type = 'success') {
    const icon = type === 'success' ? 'bi-check-circle-fill' : 'bi-exclamation-circle-fill';
    const alertHtml = `
        <div class="alert alert-${type} alert-dismissible fade show d-flex align-items-center" role="alert">
            <i class="bi ${icon} me-2"></i>
            <span>${message}</span>
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
    alertContainer.innerHTML = alertHtml;

    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        const alert = alertContainer.querySelector('.alert');
        if (alert) {
            alert.classList.remove('show');
            setTimeout(() => alert.remove(), 300);
        }
    }, 5000);
}


// ============================================================
// Hero Stats — Update counters
// ============================================================
function updateStats() {
    const total = allOpportunities.length;
    const open = allOpportunities.filter(o => o.status === 'Open').length;
    const closed = allOpportunities.filter(o => o.status === 'Closed').length;

    // Animate the numbers
    animateCounter(statTotal, total);
    animateCounter(statOpen, open);
    animateCounter(statClosed, closed);
}

function animateCounter(element, target) {
    const current = parseInt(element.textContent) || 0;
    if (current === target) return;

    const duration = 400; // ms
    const steps = 20;
    const increment = (target - current) / steps;
    let step = 0;

    const timer = setInterval(() => {
        step++;
        if (step >= steps) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.round(current + increment * step);
        }
    }, duration / steps);
}


// ============================================================
// FETCH ALL OPPORTUNITIES — GET /api/opportunities
// ============================================================
async function fetchOpportunities() {
    loadingSpinner.classList.remove('d-none');
    emptyState.classList.add('d-none');
    oppGrid.innerHTML = '';

    try {
        const response = await fetch(API_BASE);

        if (!response.ok) {
            throw new Error(`Server returned ${response.status}`);
        }

        allOpportunities = await response.json();
        updateStats();
        renderOpportunities();

    } catch (error) {
        console.error('Failed to fetch opportunities:', error);
        showAlert('Failed to load opportunities. Is the backend running?', 'danger');
    } finally {
        loadingSpinner.classList.add('d-none');
    }
}


// ============================================================
// RENDER OPPORTUNITY CARDS — Applies current filter
// ============================================================
function renderOpportunities() {
    oppGrid.innerHTML = '';

    // Apply filter
    const filtered = currentFilter === 'all'
        ? allOpportunities
        : allOpportunities.filter(o => o.status === currentFilter);

    if (filtered.length === 0) {
        emptyState.classList.remove('d-none');
        return;
    }

    emptyState.classList.add('d-none');

    filtered.forEach(opp => {
        const badgeClass = opp.status === 'Open' ? 'badge-open' : 'badge-closed';
        const deadlineFormatted = formatDate(opp.application_deadline);

        const col = document.createElement('div');
        col.className = 'col-md-6 col-lg-4';
        col.innerHTML = `
            <div class="opp-card" data-id="${opp.id}">
                <div class="opp-card-header">
                    <h3 class="opp-card-title">${escapeHtml(opp.title)}</h3>
                    <span class="badge-status ${badgeClass}">${opp.status}</span>
                </div>
                <p class="opp-card-desc">${escapeHtml(opp.description)}</p>
                <div class="opp-card-meta">
                    <span><i class="bi bi-person"></i>${escapeHtml(opp.faculty_name)}</span>
                    <span><i class="bi bi-building"></i>${escapeHtml(opp.department)}</span>
                    <span><i class="bi bi-calendar"></i>${deadlineFormatted}</span>
                    <span><i class="bi bi-people"></i>${opp.positions_available} positions</span>
                </div>
            </div>
        `;

        // Click card → show details
        col.querySelector('.opp-card').addEventListener('click', () => {
            showDetailView(opp.id);
        });

        oppGrid.appendChild(col);
    });
}


// ============================================================
// SHOW DETAIL VIEW — GET /api/opportunities/:id
// ============================================================
async function showDetailView(id) {
    showView(detailView);

    try {
        const response = await fetch(`${API_BASE}/${id}`);

        if (response.status === 404) {
            showAlert('Opportunity not found.', 'danger');
            showView(listView);
            return;
        }

        if (!response.ok) {
            throw new Error(`Server returned ${response.status}`);
        }

        const opp = await response.json();
        renderDetailCard(opp);

    } catch (error) {
        console.error('Failed to fetch opportunity details:', error);
        showAlert('Failed to load opportunity details.', 'danger');
        showView(listView);
    }
}

function renderDetailCard(opp) {
    const badgeClass = opp.status === 'Open' ? 'badge-open' : 'badge-closed';
    const deadlineFormatted = formatDate(opp.application_deadline);

    // Show "Close" button only if status is Open
    const closeButton = opp.status === 'Open'
        ? `<button class="btn-action btn-close-status" onclick="closeOpportunity(${opp.id})">
               <i class="bi bi-lock"></i> Close
           </button>`
        : '';

    detailContent.innerHTML = `
        <div class="detail-card">
            <div class="detail-header">
                <div>
                    <h2 class="detail-title">${escapeHtml(opp.title)}</h2>
                    <span class="badge-status ${badgeClass} mt-2 d-inline-block">${opp.status}</span>
                </div>
                <div class="detail-actions">
                    <button class="btn-action btn-edit" onclick="showEditForm(${opp.id})">
                        <i class="bi bi-pencil"></i> Edit
                    </button>
                    ${closeButton}
                    <button class="btn-action btn-delete" onclick="confirmDelete(${opp.id}, '${escapeHtml(opp.title).replace(/'/g, "\\'")}')">
                        <i class="bi bi-trash"></i> Delete
                    </button>
                </div>
            </div>

            <p class="detail-desc">${escapeHtml(opp.description)}</p>

            <div class="detail-grid">
                <div class="detail-field">
                    <div class="detail-field-label">Research Area</div>
                    <div class="detail-field-value">${escapeHtml(opp.research_area)}</div>
                </div>
                <div class="detail-field">
                    <div class="detail-field-label">Faculty</div>
                    <div class="detail-field-value">${escapeHtml(opp.faculty_name)}</div>
                </div>
                <div class="detail-field">
                    <div class="detail-field-label">Department</div>
                    <div class="detail-field-value">${escapeHtml(opp.department)}</div>
                </div>
                <div class="detail-field">
                    <div class="detail-field-label">Required Skills</div>
                    <div class="detail-field-value">${escapeHtml(opp.required_skills)}</div>
                </div>
                <div class="detail-field">
                    <div class="detail-field-label">Positions Available</div>
                    <div class="detail-field-value">${opp.positions_available}</div>
                </div>
                <div class="detail-field">
                    <div class="detail-field-label">Application Deadline</div>
                    <div class="detail-field-value">${deadlineFormatted}</div>
                </div>
            </div>
        </div>
    `;
}


// ============================================================
// CREATE — Show blank form
// ============================================================
function showCreateForm() {
    showView(formView);
    formTitle.innerHTML = '<i class="bi bi-plus-circle me-2"></i>Create Opportunity';
    formSubmitBtn.innerHTML = '<i class="bi bi-check-lg me-1"></i> Create Opportunity';
    oppForm.reset();
    oppForm.classList.remove('was-validated');
    formFields.id.value = '';  // No ID = create mode
}


// ============================================================
// EDIT — Fetch existing data and populate form
// ============================================================
async function showEditForm(id) {
    try {
        const response = await fetch(`${API_BASE}/${id}`);

        if (!response.ok) {
            throw new Error(`Server returned ${response.status}`);
        }

        const opp = await response.json();

        showView(formView);
        formTitle.innerHTML = '<i class="bi bi-pencil me-2"></i>Edit Opportunity';
        formSubmitBtn.innerHTML = '<i class="bi bi-check-lg me-1"></i> Update Opportunity';
        oppForm.classList.remove('was-validated');

        // Populate form fields
        formFields.id.value       = opp.id;
        formFields.title.value    = opp.title;
        formFields.area.value     = opp.research_area;
        formFields.faculty.value  = opp.faculty_name;
        formFields.dept.value     = opp.department;
        formFields.skills.value   = opp.required_skills;
        formFields.desc.value     = opp.description;
        formFields.positions.value = opp.positions_available;
        formFields.deadline.value = opp.application_deadline;

    } catch (error) {
        console.error('Failed to load opportunity for editing:', error);
        showAlert('Failed to load opportunity data for editing.', 'danger');
    }
}


// ============================================================
// FORM SUBMIT — Create or Update
// ============================================================
oppForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Client-side validation using Bootstrap's built-in classes
    if (!oppForm.checkValidity()) {
        oppForm.classList.add('was-validated');
        return;
    }

    // Additional check: positions must be non-negative
    const positions = parseInt(formFields.positions.value);
    if (isNaN(positions) || positions < 0) {
        formFields.positions.classList.add('is-invalid');
        return;
    }

    // Build the request body
    const body = {
        title:                formFields.title.value.trim(),
        description:          formFields.desc.value.trim(),
        research_area:        formFields.area.value.trim(),
        faculty_name:         formFields.faculty.value.trim(),
        department:           formFields.dept.value.trim(),
        required_skills:      formFields.skills.value.trim(),
        positions_available:  positions,
        application_deadline: formFields.deadline.value,
    };

    const isEdit = formFields.id.value !== '';
    const url    = isEdit ? `${API_BASE}/${formFields.id.value}` : API_BASE;
    const method = isEdit ? 'PUT' : 'POST';

    try {
        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body),
        });

        const data = await response.json();

        if (response.ok) {
            showAlert(
                isEdit
                    ? 'Opportunity updated successfully!'
                    : `Opportunity created successfully! (ID: ${data.id})`,
                'success'
            );
            showView(listView);
            fetchOpportunities();  // Refresh the list
        } else {
            // Server returned a validation error
            showAlert(data.error || 'An error occurred.', 'danger');
        }
    } catch (error) {
        console.error('Form submission failed:', error);
        showAlert('Failed to submit. Is the backend running?', 'danger');
    }
});


// ============================================================
// CLOSE OPPORTUNITY — PUT status to "Closed"
// ============================================================
async function closeOpportunity(id) {
    try {
        const response = await fetch(`${API_BASE}/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status: 'Closed' }),
        });

        const data = await response.json();

        if (response.ok) {
            showAlert('Opportunity status changed to Closed.', 'success');
            showDetailView(id);    // Refresh detail view
            fetchOpportunities();  // Refresh the cached list too
        } else {
            showAlert(data.error || 'Failed to close opportunity.', 'danger');
        }
    } catch (error) {
        console.error('Failed to close opportunity:', error);
        showAlert('Failed to close opportunity.', 'danger');
    }
}


// ============================================================
// DELETE — Confirmation Modal + API call
// ============================================================
function confirmDelete(id, title) {
    deleteTargetId = id;
    deleteTargetTitle = title;
    document.getElementById('delete-opp-title').textContent = title;
    deleteModal.show();
}

document.getElementById('btn-confirm-delete').addEventListener('click', async () => {
    if (!deleteTargetId) return;

    try {
        const response = await fetch(`${API_BASE}/${deleteTargetId}`, {
            method: 'DELETE',
        });

        const data = await response.json();

        deleteModal.hide();

        if (response.ok) {
            showAlert(`"${deleteTargetTitle}" deleted successfully.`, 'success');
            showView(listView);
            fetchOpportunities();
        } else {
            showAlert(data.error || 'Failed to delete opportunity.', 'danger');
        }
    } catch (error) {
        console.error('Failed to delete opportunity:', error);
        deleteModal.hide();
        showAlert('Failed to delete opportunity.', 'danger');
    } finally {
        deleteTargetId = null;
        deleteTargetTitle = '';
    }
});


// ============================================================
// FILTER BUTTONS — All / Open / Closed
// ============================================================
document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        // Update active state
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        // Apply filter
        currentFilter = btn.dataset.filter;
        renderOpportunities();
    });
});


// ============================================================
// NAVIGATION BUTTONS
// ============================================================
document.getElementById('btn-show-create').addEventListener('click', showCreateForm);
document.getElementById('btn-back-list').addEventListener('click', () => {
    showView(listView);
});
document.getElementById('btn-back-from-form').addEventListener('click', () => {
    showView(listView);
});
document.getElementById('btn-cancel-form').addEventListener('click', () => {
    showView(listView);
});
document.getElementById('nav-brand').addEventListener('click', (e) => {
    e.preventDefault();
    showView(listView);
});


// ============================================================
// UTILITY FUNCTIONS
// ============================================================

/**
 * Format a date string (YYYY-MM-DD) to a more readable format.
 * e.g., "2026-12-15" → "Dec 15, 2026"
 */
function formatDate(dateStr) {
    if (!dateStr) return 'N/A';
    const date = new Date(dateStr + 'T00:00:00');  // Prevent timezone shift
    return date.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
    });
}

/**
 * Escape HTML to prevent XSS attacks.
 */
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}


// ============================================================
// INITIALIZATION — Load all opportunities on page load
// ============================================================
document.addEventListener('DOMContentLoaded', () => {
    showView(listView);
    fetchOpportunities();
});
