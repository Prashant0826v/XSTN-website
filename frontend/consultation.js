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

            fetch("https://xstn-website-1.onrender.com/api/consultation/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(formData)
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
                    alert("✅ Consultation request submitted! We'll contact you to schedule a time.");
                    form.reset();
                })
                .catch(error => {
                    console.error("Error:", error);
                    alert("❌ Error submitting request: " + error.message);
                });
        });
    }
});
