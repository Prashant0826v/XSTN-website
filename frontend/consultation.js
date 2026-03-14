// Consultation Form Handler
document.addEventListener("DOMContentLoaded", function () {
    const consultForm = document.querySelector(".consult-form");

    if (consultForm) {
        consultForm.id = "consultationForm";

        consultForm.addEventListener("submit", function (e) {
            e.preventDefault();

            const form = this;
            const selects = form.querySelectorAll('select');

            const formData = {
                full_name: form.querySelector('input[type="text"]').value,
                email: form.querySelector('input[type="email"]').value,
                phone: form.querySelector('input[type="tel"]')?.value || '',
                consultation_type: selects[0]?.value || '',
                preferred_date: form.querySelector('input[type="date"]')?.value || '',
                requirement: form.querySelector('textarea').value
            };

            console.log("Submitting consultation:", formData);

            const isLocal = window.location.hostname === "127.0.0.1" || window.location.hostname === "localhost";
            const apiUrl = isLocal 
                ? "http://127.0.0.1:8000/api/consultation/" 
                : "https://xstn-website-production.up.railway.app/api/consultation/";

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
                    console.log("Response status:", response.status);
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    console.log("Success:", data);
                    showSuccessPopup("Consultation request submitted! We'll contact you to schedule a time.", form);
                })
                .catch(error => {
                    console.error("Error:", error);
                    showErrorPopup("Error submitting request. Please try again later.");
                });
        });
    }
});
