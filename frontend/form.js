document.getElementById("contactForm").addEventListener("submit", function (e) {
  e.preventDefault();

  const form = this;
  const submitBtn = form.querySelector('.submit-btn');
  submitBtn.disabled = true;
  submitBtn.textContent = 'Sending...';

  const formData = {
    full_name: form.querySelector('input[name="full_name"]').value,
    email: form.querySelector('input[name="email"]').value,
    subject: form.querySelector('input[name="subject"]').value,
    message: form.querySelector('textarea[name="message"]').value,
    phone: ""
  };

  fetch("http://localhost:8000/api/contact/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(formData)
  })
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      showSuccessPopup("Your message has been sent successfully! We'll get back to you soon.", form);
    })
    .catch(error => {
      console.error("Error:", error);
      showErrorPopup("Something went wrong. Please try again later.");
    })
    .finally(() => {
      submitBtn.disabled = false;
      submitBtn.textContent = 'Send Message';
    });
});
