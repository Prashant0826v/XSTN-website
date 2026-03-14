document.addEventListener("DOMContentLoaded", function () {
    const newsletterForm = document.getElementById("newsletterForm");
    
    if (newsletterForm) {
        newsletterForm.addEventListener("submit", async function (e) {
            e.preventDefault();
            
            const emailInput = document.getElementById("newsletterEmail");
            const email = emailInput ? emailInput.value : "";
            
            if (!email) {
                if (typeof showErrorPopup === "function") {
                    showErrorPopup("Please enter a valid email address.");
                } else {
                    alert("Please enter a valid email address.");
                }
                return;
            }

            const submitBtn = newsletterForm.querySelector('.submit-btn');
            const originalBtnText = submitBtn ? submitBtn.textContent : "Subscribe";
            
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.textContent = "Subscribing...";
            }

            try {
                // Determine API BASE URL from global scope or default to 127.0.0.1:8000
                const baseUrl = typeof API_BASE !== 'undefined' ? API_BASE : 'http://127.0.0.1:8000';
                
                const response = await fetch(`${baseUrl}/api/newsletter/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email: email })
                });

                if (response.ok) {
                    if (typeof showSuccessPopup === "function") {
                        showSuccessPopup("You have successfully subscribed to our newsletter!", newsletterForm);
                    } else {
                        alert("You have successfully subscribed to our newsletter!");
                        newsletterForm.reset();
                    }
                } else {
                    const data = await response.json();
                    const errors = data ? Object.values(data).flat().join('. ') : 'Subscription failed.';
                    if (typeof showErrorPopup === "function") {
                        showErrorPopup(errors);
                    } else {
                        alert("Error: " + errors);
                    }
                }
            } catch (error) {
                console.error("Newsletter subscription error:", error);
                if (typeof showErrorPopup === "function") {
                    showErrorPopup("Network error. Please check your connection.");
                } else {
                    alert("Network error. Please try again later.");
                }
            } finally {
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.textContent = originalBtnText;
                }
            }
        });
    }
});
