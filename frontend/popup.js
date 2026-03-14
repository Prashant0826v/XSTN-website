/**
 * XSTN Success/Error Popup System
 * Premium animated modal popup for form submissions.
 */

function showPopup(type, title, message, formElement, onCloseCallback) {
  // Remove existing popup if any
  const existing = document.querySelector('.xstn-popup-overlay');
  if (existing) existing.remove();

  const isSuccess = type === 'success';
  const iconSVG = isSuccess
    ? `<svg viewBox="0 0 52 52" class="popup-checkmark">
        <circle cx="26" cy="26" r="25" fill="none" stroke="#00e676" stroke-width="2"/>
        <path fill="none" stroke="#00e676" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" d="M14 27l7 7 16-16"/>
      </svg>`
    : `<svg viewBox="0 0 52 52" class="popup-checkmark">
        <circle cx="26" cy="26" r="25" fill="none" stroke="#ff5252" stroke-width="2"/>
        <path fill="none" stroke="#ff5252" stroke-width="3" stroke-linecap="round" d="M18 18l16 16M34 18l-16 16"/>
      </svg>`;

  const overlay = document.createElement('div');
  overlay.className = 'xstn-popup-overlay';
  overlay.innerHTML = `
    <div class="xstn-popup-box">
      <div class="xstn-popup-icon">${iconSVG}</div>
      <h3 class="xstn-popup-title">${title}</h3>
      <p class="xstn-popup-message">${message}</p>
      <button class="xstn-popup-btn ${isSuccess ? 'success' : 'error'}" id="popupOkBtn">OK</button>
    </div>
  `;

  document.body.appendChild(overlay);

  // Trigger animation
  requestAnimationFrame(() => {
    overlay.classList.add('active');
  });

  // Close handler
  const closePopup = () => {
    overlay.classList.remove('active');
    setTimeout(() => {
      overlay.remove();
      if (isSuccess && formElement) {
        formElement.reset();
        formElement.style.display = '';
      }
      if (typeof onCloseCallback === 'function') {
        onCloseCallback();
      }
    }, 300);
  };

  document.getElementById('popupOkBtn').addEventListener('click', closePopup);
  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) closePopup();
  });
}

function showSuccessPopup(message, formElement, onCloseCallback) {
  showPopup('success', 'Successfully Submitted!', message, formElement, onCloseCallback);
}

function showErrorPopup(message) {
  showPopup('error', 'Submission Failed', message, null);
}
