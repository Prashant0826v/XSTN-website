// Consultation Form Handler
document.addEventListener("DOMContentLoaded", function () {
    const consultForm = document.querySelector(".consult-form");

    if (consultForm) {
        consultForm.id = "consultationForm";

        consultForm.addEventListener("submit", function (e) {
            e.preventDefault();

            const form = this;
            const submitBtn = form.querySelector('.submit-btn');
            submitBtn.disabled = true;
            submitBtn.textContent = 'Submitting...';

            const selects = form.querySelectorAll('select');

            const formData = {
                full_name: form.querySelector('input[type="text"]').value,
                email: form.querySelector('input[type="email"]').value,
                phone: form.querySelector('input[type="tel"]')?.value || '',
                consultation_type: selects[0]?.value || '',
                preferred_date: form.querySelector('input[type="date"]')?.value || '',
                requirement: form.querySelector('textarea').value
            };

            fetch("http://localhost:8000/api/consultation/", {
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
                    showSuccessPopup("Your consultation request has been submitted! We'll contact you to schedule a time.", form);
                })
                .catch(error => {
                    console.error("Error:", error);
                    showErrorPopup("Something went wrong. Please try again later.");
                })
                .finally(() => {
                    submitBtn.disabled = false;
                    submitBtn.textContent = 'Submit Request';
                });
        });
    }
});
