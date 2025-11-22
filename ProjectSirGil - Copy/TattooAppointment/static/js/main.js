/**
 * Main JavaScript File
 * Tattoo Appointment Application
 */

// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('Tattoo Appointment App Loaded');

    // Initialize mobile menu toggle
    initMobileMenu();

    // Initialize form validation
    initFormValidation();

    // Initialize search functionality
    initSearch();

    // Auto-dismiss messages
    autoDismissMessages();
});

/**
 * Mobile Menu Toggle
 */
function initMobileMenu() {
    const toggle = document.querySelector('.navbar__toggle');
    const menu = document.querySelector('.navbar__menu');

    if (toggle && menu) {
        toggle.addEventListener('click', function() {
            const isExpanded = this.getAttribute('aria-expanded') === 'true';
            this.setAttribute('aria-expanded', !isExpanded);
            menu.classList.toggle('is-open');
        });
    }
}

/**
 * Form Validation
 */
function initFormValidation() {
    const forms = document.querySelectorAll('form[data-validate]');

    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
            }
        });
    });
}

function validateForm(form) {
    let isValid = true;
    const inputs = form.querySelectorAll('input[required], textarea[required]');

    inputs.forEach(input => {
        if (!input.value.trim()) {
            showError(input, 'This field is required');
            isValid = false;
        } else {
            clearError(input);
        }
    });

    return isValid;
}

function showError(input, message) {
    const formField = input.closest('.form-field');
    if (formField) {
        let errorElement = formField.querySelector('.form-field__error');
        if (!errorElement) {
            errorElement = document.createElement('span');
            errorElement.className = 'form-field__error';
            formField.appendChild(errorElement);
        }
        errorElement.textContent = message;
        input.classList.add('has-error');
    }
}

function clearError(input) {
    const formField = input.closest('.form-field');
    if (formField) {
        const errorElement = formField.querySelector('.form-field__error');
        if (errorElement) {
            errorElement.remove();
        }
        input.classList.remove('has-error');
    }
}

/**
 * Search Functionality
 */
function initSearch() {
    const searchInputs = document.querySelectorAll('.search-bar__input');

    searchInputs.forEach(input => {
        // Debounce search for better performance
        let timeout;
        input.addEventListener('input', function() {
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                const query = this.value.trim();
                if (query.length >= 3) {
                    console.log('Searching for:', query);
                    // Implement search logic here
                }
            }, 300);
        });
    });
}

/**
 * Auto-dismiss messages after 5 seconds
 */
function autoDismissMessages() {
    const messages = document.querySelectorAll('.alert');

    messages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 300);
        }, 5000);
    });
}

/**
 * Utility: Show loading state
 */
function showLoading(element) {
    element.classList.add('is-loading');
    element.disabled = true;
}

function hideLoading(element) {
    element.classList.remove('is-loading');
    element.disabled = false;
}

/**
 * Utility: Format date
 */
function formatDate(date) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(date).toLocaleDateString('en-US', options);
}

// Export utilities for use in other modules
window.TattooApp = {
    showLoading,
    hideLoading,
    formatDate,
    showError,
    clearError
};
