document.getElementById("internshipForm").addEventListener("submit", function (e) {
    e.preventDefault();

    const form = this;
    const submitBtn = form.querySelector('.submit-btn');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Submitting...';

    const formData = {
        full_name: form.querySelector('input[name="full_name"]').value,
        email: form.querySelector('input[name="email"]').value,
        phone: form.querySelector('input[name="phone"]').value,
        position: form.querySelector('select[name="position"]').value,
        experience: form.querySelector('textarea[name="experience"]').value,
        cover_letter: form.querySelector('textarea[name="cover_letter"]').value,
        resume: null
    };

    const isLocal = window.location.hostname === "127.0.0.1" || window.location.hostname === "localhost";
    const apiUrl = isLocal 
        ? "http://127.0.0.1:8000/api/internship/" 
        : "https://xstn-backend.onrender.com/api/internship/";

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
            showSuccessPopup("Your internship application has been submitted successfully! We'll review it and contact you soon.", form);
        })
        .catch(error => {
            console.error("Error:", error);
            showErrorPopup("Something went wrong. Please try again later.");
        })
        .finally(() => {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Submit Application';
        });
});
