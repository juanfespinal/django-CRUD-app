// CleanRecruit - Main JavaScript

document.addEventListener('DOMContentLoaded', function () {
    // Initialize HTMX
    initHTMX();

    // Initialize modals
    initModals();

    // Initialize delete confirmations
    initDeleteConfirmations();

    // Initialize filters
    initFilters();
});

// HTMX Configuration
function initHTMX() {
    // Add CSRF token to all requests
    document.body.addEventListener('htmx:configRequest', function (event) {
        const csrfToken = getCookie('csrftoken');
        if (csrfToken) {
            event.detail.headers['X-CSRFToken'] = csrfToken;
        }
    });

    // Handle form responses
    document.body.addEventListener('htmx:afterSwap', function (event) {
        // Reinitialize components after content swap
        initModals();
        initDeleteConfirmations();
    });

    // Show toast on response
    document.body.addEventListener('htmx:afterRequest', function (event) {
        const response = event.detail.xhr;
        if (response.status >= 200 && response.status < 300) {
            // Check if there's a toast in the response
            const toast = event.detail.serverResponse;
            if (toast && toast.includes('toast')) {
                // Toast will be rendered by Django messages framework
            }
        }
    });
}

// Modal Functions
function initModals() {
    const modalTriggers = document.querySelectorAll('[data-modal]');
    const modalClose = document.querySelectorAll('[data-close]');

    modalTriggers.forEach(trigger => {
        trigger.addEventListener('click', function (e) {
            e.preventDefault();
            const modalId = this.getAttribute('data-modal');
            openModal(modalId);
        });
    });

    modalClose.forEach(close => {
        close.addEventListener('click', function () {
            const modal = this.closest('.modal-backdrop');
            if (modal) {
                closeModal(modal);
            }
        });
    });

    // Close on backdrop click
    document.querySelectorAll('.modal-backdrop').forEach(backdrop => {
        backdrop.addEventListener('click', function (e) {
            if (e.target === this) {
                closeModal(this);
            }
        });
    });

    // Close on escape
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') {
            document.querySelectorAll('.modal-backdrop.open').forEach(modal => {
                closeModal(modal);
            });
        }
    });
}

function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('open');
        document.body.style.overflow = 'hidden';

        // Focus first input
        const firstInput = modal.querySelector('input, select, textarea');
        if (firstInput) {
            setTimeout(() => firstInput.focus(), 100);
        }
    }
}

function closeModal(modal) {
    modal.classList.remove('open');
    document.body.style.overflow = '';
}

// Delete Confirmation
function initDeleteConfirmations() {
    const deleteButtons = document.querySelectorAll('[data-delete]');

    deleteButtons.forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();
            const url = this.getAttribute('href') || this.getAttribute('data-url');
            const itemName = this.getAttribute('data-item') || 'item';

            if (confirm(`Are you sure you want to delete "${itemName}"?`)) {
                htmx.ajax('DELETE', url, {
                    swap: 'afterend',
                    target: document.body
                }).then(() => {
                    // Reload the page to show updated list
                    window.location.reload();
                });
            }
        });
    });
}

// Filter Functions
function initFilters() {
    // Auto-submit form on filter change
    const filterSelects = document.querySelectorAll('[data-filter]');

    filterSelects.forEach(select => {
        select.addEventListener('change', function () {
            const form = this.closest('form');
            if (form) {
                form.submit();
            }
        });
    });

    // Debounced search
    const searchInput = document.querySelector('[data-search]');
    if (searchInput) {
        let timeout;
        searchInput.addEventListener('input', function () {
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                const form = this.closest('form');
                if (form) {
                    form.submit();
                }
            }, 300);
        });
    }
}

// Utility Functions
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Mobile Menu Toggle
function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    if (sidebar) {
        sidebar.classList.toggle('open');
    }
}

// Export for global use
window.openModal = openModal;
window.closeModal = closeModal;
window.toggleSidebar = toggleSidebar;
