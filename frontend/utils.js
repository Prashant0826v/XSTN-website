// Utility functions for XSTN frontend

/**
 * Validate email format
 */
function isValidEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

/**
 * Validate phone number (basic validation)
 */
function isValidPhone(phone) {
  if (!phone) return true; // Phone is optional
  const phoneRegex = /^[\d\s\-\+\(\)]{7,}$/;
  return phoneRegex.test(phone);
}

/**
 * Trim all form input values
 */
function trimFormValues(form) {
  const inputs = form.querySelectorAll('input[type="text"], input[type="email"], input[type="tel"], input[type="url"], textarea');
  inputs.forEach(input => {
    input.value = input.value.trim();
  });
}

/**
 * Show loading state on button
 */
function setButtonLoading(button, isLoading, text = null) {
  if (isLoading) {
    button.disabled = true;
    button.dataset.originalText = button.textContent;
    if (text) button.textContent = text;
  } else {
    button.disabled = false;
    button.textContent = button.dataset.originalText || 'Submit';
  }
}

/**
 * Display toast notification
 */
function showNotification(message, type = 'success', duration = 3000) {
  const toast = document.createElement('div');
  toast.className = `notification notification-${type}`;
  toast.textContent = message;
  toast.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 16px 24px;
    background-color: ${type === 'success' ? '#28a745' : type === 'error' ? '#dc3545' : '#17a2b8'};
    color: white;
    border-radius: 4px;
    z-index: 9999;
    font-size: 14px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    animation: slideIn 0.3s ease-out;
  `;
  
  document.body.appendChild(toast);
  
  setTimeout(() => {
    toast.style.animation = 'slideOut 0.3s ease-out';
    setTimeout(() => toast.remove(), 300);
  }, duration);
}

/**
 * Handle API errors
 */
function handleApiError(error, defaultMessage = 'An error occurred. Please try again.') {
  console.error('API Error:', error);
  
  let message = defaultMessage;
  
  if (error.response) {
    message = error.response.data?.detail || error.response.data?.message || defaultMessage;
  } else if (error.message) {
    message = error.message;
  }
  
  return message;
}

/**
 * Disable form during submission
 */
function disableForm(form, disable = true) {
  const elements = form.querySelectorAll('input, textarea, select, button');
  elements.forEach(el => {
    el.disabled = disable;
  });
}

/**
 * Format date for display
 */
function formatDate(date) {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
}

/**
 * Scroll to element smoothly
 */
function smoothScroll(element) {
  element.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * Get form data as object
 */
function getFormData(form) {
  const formData = new FormData(form);
  const data = {};
  
  for (let [key, value] of formData.entries()) {
    if (value) {
      data[key] = value.trim();
    }
  }
  
  return data;
}

/**
 * Clear form errors
 */
function clearFormErrors(form) {
  const errors = form.querySelectorAll('.error-message');
  errors.forEach(error => error.remove());
  
  const errorFields = form.querySelectorAll('.error');
  errorFields.forEach(field => field.classList.remove('error'));
}

/**
 * Show form errors
 */
function showFormErrors(form, errors) {
  clearFormErrors(form);
  
  for (let [fieldName, errorMessage] of Object.entries(errors)) {
    const field = form.querySelector(`[name="${fieldName}"]`);
    if (field) {
      field.classList.add('error');
      const errorEl = document.createElement('div');
      errorEl.className = 'error-message';
      errorEl.textContent = errorMessage;
      field.parentNode.appendChild(errorEl);
    }
  }
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    isValidEmail,
    isValidPhone,
    trimFormValues,
    setButtonLoading,
    showNotification,
    handleApiError,
    disableForm,
    formatDate,
    smoothScroll,
    getFormData,
    clearFormErrors,
    showFormErrors
  };
}
