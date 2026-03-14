document.getElementById("joinForm").addEventListener("submit", function (e) {
  e.preventDefault();

  const form = this;
  const formData = {
    full_name: form.querySelector('input[name="full_name"]').value,
    email: form.querySelector('input[name="email"]').value,
    role: form.querySelector('select[name="role"]').value,
    message: form.querySelector('textarea[name="message"]').value
  };

  const isLocal = window.location.hostname === "127.0.0.1" || window.location.hostname === "localhost";
  const apiUrl = isLocal 
    ? "http://127.0.0.1:8000/api/forms/join-applications/" 
    : "https://xstn-website-production.up.railway.app/api/forms/join-applications/";

  fetch(apiUrl, {
    method: "POST",
    mode: "cors",
    headers: {
      "Content-Type": "application/json",
      "Accept": "application/json"
    },
    body: JSON.stringify(formData),
    credentials: "omit"
  })
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      if (data.id) {
        showSuccessPopup("Your application has been received successfully. We will review it shortly.", form);
      } else {
        showErrorPopup("Error: " + (data.detail || JSON.stringify(data)));
      }
    })
    .catch(error => {
      console.error("Error:", error);
      showErrorPopup("Error submitting form: " + error.message);
    });
});
