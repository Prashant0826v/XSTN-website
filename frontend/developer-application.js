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
                const inputs = form.querySelectorAll('input[type="text"]');
                const selects = form.querySelectorAll('select');

                const formData = {
                    full_name: inputs[0]?.value || '',
                    email: form.querySelector('input[type="email"]').value,
                    phone: form.querySelector('input[type="tel"]')?.value || '',
                    role_interested: selects[0]?.value || '',
                    skills: inputs[1]?.value || '',  // Skills input
                    experience_level: selects[1]?.value?.toLowerCase() || 'beginner',
                    portfolio_url: form.querySelector('input[name="portfolio_url"]')?.value || '',
                    github_url: form.querySelector('input[name="github_url"]')?.value || '',
                    resume_url: form.querySelector('input[name="resume_url"]')?.value || '',
                    message: form.querySelector('textarea').value
                };

                console.log("Submitting developer application:", formData);

                const isLocal = window.location.hostname === "127.0.0.1" || window.location.hostname === "localhost";
                const apiUrl = isLocal 
                    ? "http://127.0.0.1:8000/api/forms/developer-applications/" 
                    : "https://xstn-website-production.up.railway.app/api/forms/developer-applications/";

                fetch(apiUrl, {
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
                        showSuccessPopup("Application submitted! Our team will review it and contact you soon.", form);
                    })
                    .catch(error => {
                        console.error("Error:", error);
                        showErrorPopup("Error submitting application. Please try again later.");
                    });
            });
        }
    }
});
