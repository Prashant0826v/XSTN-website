/**
 * XSTN API Client for Frontend Form Submissions
 * 
 * This module provides functions to submit form data to the XSTN Django backend API.
 * All functions are async and return a result object with { success: boolean, data: any, error: string }
 * 
 * Usage:
 * import { submitContactForm, subscribeNewsletter } from './api-client.js';
 * 
 * const result = await submitContactForm({ name, email, phone, subject, message });
 * if (result.success) {
 *     console.log('Form submitted:', result.data);
 * } else {
 *     console.error('Error:', result.error);
 * }
 */

const API_BASE_URL = 'https://xstn-website-fvon.onrender.com';

// For production, update to:
// const API_BASE_URL = 'https://api.xstn.com';

/**
 * Utility function to get the appropriate API URL based on environment
 * @returns {string} API base URL
 */
function getAPIBaseUrl() {
    const hostname = window.location.hostname;
    if (hostname === 'localhost' || hostname === '127.0.0.1') {
        return 'http://127.0.0.1:8000';
    }
    // Automatically use your Railway backend URL
    // REPLACE this with your actual Railway URL once deployed
    return 'https://your-backend-name.railway.app';
}

/**
 * Generic function to submit form data to API
 * @param {string} endpoint - API endpoint (e.g., 'api/contact')
 * @param {object} data - Form data to submit
 * @returns {Promise} Result object with { success, data, error }
 */
async function submitForm(endpoint, data) {
    try {
        const url = `${getAPIBaseUrl()}/${endpoint}`;
        console.log(`Submitting to: ${url}`, data);

        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(data),
            credentials: 'include' // Include cookies for CORS
        });

        const contentType = response.headers.get('content-type');
        let responseData;

        if (contentType && contentType.includes('application/json')) {
            responseData = await response.json();
        } else {
            const text = await response.text();
            responseData = { error: text || 'Unknown error' };
        }

        if (!response.ok) {
            const errorMessage = responseData.error || responseData.detail || `HTTP ${response.status}`;
            throw new Error(errorMessage);
        }

        return {
            success: true,
            data: responseData
        };

    } catch (error) {
        console.error(`API Error (${endpoint}):`, error);
        return {
            success: false,
            error: error.message || 'Form submission failed. Please try again.'
        };
    }
}

/**
 * Submit contact form
 * @param {object} formData - { full_name, email, phone, subject, message }
 * @returns {Promise} Result object
 */
async function submitContactForm(formData) {
    return submitForm('api/contact/', {
        full_name: formData.full_name || formData.name || '',
        email: formData.email || '',
        phone: formData.phone || '',
        subject: formData.subject || '',
        message: formData.message || ''
    });
}

/**
 * Submit proposal form
 * @param {object} formData - { name, email, company, project_type, budget_range, timeline, message }
 * @returns {Promise} Result object
 */
async function submitProposalForm(formData) {
    return submitForm('api/proposal/', {
        name: formData.name || '',
        email: formData.email || '',
        company: formData.company || '',
        project_type: formData.project_type || '',
        budget_range: formData.budget_range || '',
        timeline: formData.timeline || '',
        message: formData.message || ''
    });
}

/**
 * Submit internship application
 * @param {object} formData - { full_name, email, phone, position, experience, cover_letter, resume }
 * @returns {Promise} Result object
 */
async function submitInternshipApplication(formData) {
    return submitForm('api/internship/', {
        full_name: formData.full_name || formData.fullName || '',
        email: formData.email || '',
        phone: formData.phone || '',
        position: formData.position || '',
        experience: formData.experience || '',
        cover_letter: formData.cover_letter || formData.coverLetter || '',
        resume: formData.resume || ''
    });
}

/**
 * Submit developer application
 * @param {object} formData - { full_name, email, phone, role_interested, experience_level, skills, portfolio_url, github_url, message }
 * @returns {Promise} Result object
 */
async function submitDeveloperApplication(formData) {
    return submitForm('api/developer-application/', {
        full_name: formData.full_name || formData.fullName || '',
        email: formData.email || '',
        phone: formData.phone || '',
        role_interested: formData.role_interested || formData.roleInterested || '',
        experience_level: formData.experience_level || formData.experienceLevel || 'intermediate',
        skills: formData.skills || '',
        portfolio_url: formData.portfolio_url || formData.portfolioUrl || '',
        github_url: formData.github_url || formData.githubUrl || '',
        message: formData.message || ''
    });
}

/**
 * Submit join community
 * @param {object} formData - { full_name, email, role, message }
 * @returns {Promise} Result object
 */
async function submitJoinCommunity(formData) {
    return submitForm('api/join/', {
        full_name: formData.full_name || formData.fullName || '',
        email: formData.email || '',
        role: formData.role || formData.role_interested || '',
        message: formData.message || ''
    });
}

/**
 * Submit consultation request
 * @param {object} formData - { full_name, email, phone, consultation_type, preferred_date, requirement }
 * @returns {Promise} Result object
 */
async function submitConsultationRequest(formData) {
    return submitForm('api/consultation/', {
        full_name: formData.full_name || formData.fullName || '',
        email: formData.email || '',
        phone: formData.phone || '',
        consultation_type: formData.consultation_type || formData.consultationType || '',
        preferred_date: formData.preferred_date || formData.preferredDate || '',
        requirement: formData.requirement || ''
    });
}

/**
 * Subscribe to newsletter
 * @param {string} email - Email address to subscribe
 * @returns {Promise} Result object
 */
async function subscribeNewsletter(email) {
    return submitForm('api/newsletter/', {
        email: email || ''
    });
}

/**
 * Submit testimonial
 * @param {object} formData - { name, company, email, rating, message }
 * @returns {Promise} Result object
 */
async function submitTestimonial(formData) {
    return submitForm('api/testimonial/', {
        name: formData.name || '',
        company: formData.company || '',
        email: formData.email || '',
        rating: parseInt(formData.rating) || 5,
        message: formData.message || ''
    });
}

/**
 * Form validation utility functions
 */

function isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function isValidPhone(phone) {
    // Simple validation - at least 10 digits
    const digits = phone.replace(/\D/g, '');
    return digits.length >= 10;
}

function isValidUrl(url) {
    try {
        new URL(url);
        return true;
    } catch {
        return false;
    }
}

/**
 * Validate contact form data
 * @param {object} data - Form data to validate
 * @returns {object} { isValid: boolean, errors: string[] }
 */
function validateContactForm(data) {
    const errors = [];

    if (!data.name || data.name.trim().length === 0) {
        errors.push('Name is required');
    }

    if (!data.email || !isValidEmail(data.email)) {
        errors.push('Valid email is required');
    }

    if (data.phone && data.phone.trim().length > 0 && !isValidPhone(data.phone)) {
        errors.push('Phone number must have at least 10 digits');
    }

    if (!data.subject || data.subject.trim().length === 0) {
        errors.push('Subject is required');
    }

    if (!data.message || data.message.trim().length < 10) {
        errors.push('Message must be at least 10 characters');
    }

    return {
        isValid: errors.length === 0,
        errors: errors
    };
}

/**
 * Validate inquiry form data
 * @param {object} data - Form data to validate
 * @returns {object} { isValid: boolean, errors: string[] }
 */
function validateInquiryForm(data) {
    const errors = [];

    if (!data.name || data.name.trim().length === 0) {
        errors.push('Name is required');
    }

    if (!data.email || !isValidEmail(data.email)) {
        errors.push('Valid email is required');
    }

    if (!data.projectType || data.projectType.trim().length === 0) {
        errors.push('Project type is required');
    }

    if (!data.message || data.message.trim().length < 10) {
        errors.push('Message must be at least 10 characters');
    }

    return {
        isValid: errors.length === 0,
        errors: errors
    };
}

/**
 * Show form loading state
 * @param {HTMLElement} button - Submit button element
 */
function showLoadingState(button) {
    button.disabled = true;
    const originalText = button.textContent;
    button.setAttribute('data-original-text', originalText);
    button.textContent = '⏳ Loading...';
}

/**
 * Hide form loading state
 * @param {HTMLElement} button - Submit button element
 */
function hideLoadingState(button) {
    button.disabled = false;
    const originalText = button.getAttribute('data-original-text') || 'Submit';
    button.textContent = originalText;
}

/**
 * Show success message
 * @param {string} message - Success message to display
 * @param {string} containerId - ID of container element (optional)
 */
function showSuccessMessage(message, containerId = null) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'api-success-message';
    messageDiv.innerHTML = `
        <div style="
            background-color: #10b981;
            color: white;
            padding: 16px;
            border-radius: 8px;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        ">
            <span style="font-size: 20px;">✓</span>
            <span>${message}</span>
        </div>
    `;

    if (containerId) {
        const container = document.getElementById(containerId);
        if (container) {
            container.insertBefore(messageDiv, container.firstChild);
        }
    } else {
        document.body.insertBefore(messageDiv, document.body.firstChild);
    }

    // Auto-remove after 5 seconds
    setTimeout(() => messageDiv.remove(), 5000);
}

/**
 * Show error message
 * @param {string} message - Error message to display
 * @param {string} containerId - ID of container element (optional)
 */
function showErrorMessage(message, containerId = null) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'api-error-message';
    messageDiv.innerHTML = `
        <div style="
            background-color: #ef4444;
            color: white;
            padding: 16px;
            border-radius: 8px;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        ">
            <span style="font-size: 20px;">✗</span>
            <span>${message}</span>
        </div>
    `;

    if (containerId) {
        const container = document.getElementById(containerId);
        if (container) {
            container.insertBefore(messageDiv, container.firstChild);
        }
    } else {
        document.body.insertBefore(messageDiv, document.body.firstChild);
    }

    // Auto-remove after 5 seconds
    setTimeout(() => messageDiv.remove(), 5000);
}

// Export all functions
export {
    // Form submission functions
    submitContactForm,
    submitInquiryForm,
    submitInternshipApplication,
    submitDeveloperApplication,
    submitJoinApplication,
    submitConsultationRequest,
    subscribeNewsletter,
    submitTestimonial,

    // Validation functions
    isValidEmail,
    isValidPhone,
    isValidUrl,
    validateContactForm,
    validateInquiryForm,

    // UI helper functions
    showLoadingState,
    hideLoadingState,
    showSuccessMessage,
    showErrorMessage,

    // Utility
    getAPIBaseUrl,
    submitForm
};
