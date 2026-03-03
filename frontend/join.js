document.getElementById("joinForm").addEventListener("submit", function (e) {
  e.preventDefault();

  const form = this;
  const submitBtn = form.querySelector('.submit-btn');
  submitBtn.disabled = true;
  submitBtn.textContent = 'Submitting...';

  const formData = {
    full_name: form.querySelector('input[name="full_name"]').value,
    email: form.querySelector('input[name="email"]').value,
    role: form.querySelector('select[name="role"]').value,
    message: form.querySelector('textarea[name="message"]').value
  };

  fetch("http://localhost:8000/api/join/", {
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
      showSuccessPopup("Your application has been submitted successfully! We'll review it and get back to you.", form);
    })
    .catch(error => {
      console.error("Error:", error);
      showErrorPopup("Something went wrong. Please try again later.");
    })
    .finally(() => {
      submitBtn.disabled = false;
      submitBtn.textContent = 'Apply Now';
    });
});
