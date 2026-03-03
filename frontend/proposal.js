// Proposal Form Handler
document.addEventListener("DOMContentLoaded", function() {
    const proposalForm = document.querySelector(".proposal-form");
    
    if (proposalForm && !proposalForm.id) {
        // Check if it's actually a proposal form (not developer form on join-developer.html)
        const formHeading = document.querySelector("h2");
        if (formHeading && formHeading.textContent.includes("Proposal")) {
            proposalForm.id = "proposalForm";
            
            proposalForm.addEventListener("submit", function(e) {
                e.preventDefault();
                
                const form = this;
                const formData = {
                    name: form.querySelector('input[type="text"]').value,
                    email: form.querySelector('input[type="email"]').value,
                    phone: form.querySelector('input[type="tel"]')?.value || '',
                    project_type: form.querySelector('select').value,
                    budget_range: form.querySelectorAll('select')[1]?.value || '',
                    message: form.querySelector('textarea').value
                };
                
                console.log("Submitting proposal:", formData);
                
                fetch("http://localhost:8000/api/proposal/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(formData)
                })
                .then(response => {
                    console.log("Response status:", response.status);
                    if(!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    console.log("Success:", data);
                    alert("✅ Proposal submitted successfully! We'll review it and contact you soon.");
                    form.reset();
                })
                .catch(error => {
                    console.error("Error:", error);
                    alert("❌ Error submitting proposal: " + error.message);
                });
            });
        }
    }
});
