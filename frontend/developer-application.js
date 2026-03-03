// Developer Application Form Handler
document.addEventListener("DOMContentLoaded", function () {
    const devForm = document.querySelector(".proposal-form");

    if (devForm) {
        const formHeading = document.querySelector("h2");
        if (formHeading && formHeading.textContent.includes("Developer")) {
            devForm.id = "developerForm";

            devForm.addEventListener("submit", function (e) {
                e.preventDefault();

                const form = this;
                const submitBtn = form.querySelector('.submit-btn');
                submitBtn.disabled = true;
                submitBtn.textContent = 'Submitting...';

                const inputs = form.querySelectorAll('input[type="text"]');
                const selects = form.querySelectorAll('select');

                const formData = {
                    full_name: inputs[0]?.value || '',
                    email: form.querySelector('input[type="email"]').value,
                    phone: form.querySelector('input[type="tel"]')?.value || '',
                    role_interested: selects[0]?.value || '',
                    skills: inputs[1]?.value || '',
                    experience_level: selects[1]?.value?.toLowerCase() || 'beginner',
                    portfolio_url: form.querySelector('input[type="url"]')?.value || '',
                    message: form.querySelector('textarea').value
                };

                fetch("http://localhost:8000/api/developer-application/", {
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
                        showSuccessPopup("Your developer application has been submitted! Our team will review it and contact you soon.", form);
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
        }
    }
});
