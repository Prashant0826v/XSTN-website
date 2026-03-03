// Proposal Form Handler
document.addEventListener("DOMContentLoaded", function () {
    const proposalForm = document.querySelector(".proposal-form");

    if (proposalForm && !proposalForm.id) {
        const formHeading = document.querySelector("h2");
        if (formHeading && formHeading.textContent.includes("Proposal")) {
            proposalForm.id = "proposalForm";

            proposalForm.addEventListener("submit", function (e) {
                e.preventDefault();

                const form = this;
                const submitBtn = form.querySelector('.submit-btn');
                submitBtn.disabled = true;
                submitBtn.textContent = 'Submitting...';

                const formData = {
                    name: form.querySelector('input[type="text"]').value,
                    email: form.querySelector('input[type="email"]').value,
                    phone: form.querySelector('input[type="tel"]')?.value || '',
                    project_type: form.querySelector('select').value,
                    budget_range: form.querySelectorAll('select')[1]?.value || '',
                    message: form.querySelector('textarea').value
                };

                fetch("http://localhost:8000/api/proposal/", {
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
                        showSuccessPopup("Your proposal request has been submitted! We'll review it and contact you soon.", form);
                    })
                    .catch(error => {
                        console.error("Error:", error);
                        showErrorPopup("Something went wrong. Please try again later.");
                    })
                    .finally(() => {
                        submitBtn.disabled = false;
                        submitBtn.textContent = 'Request Proposal';
                    });
            });
        }
    }
});
