document.getElementById("contactForm").addEventListener("submit", function(e){
  e.preventDefault();
  
  const form = this;
  const formData = {
    full_name: form.querySelector('input[name="full_name"]').value,
    email: form.querySelector('input[name="email"]').value,
    subject: form.querySelector('input[name="subject"]').value,
    message: form.querySelector('textarea[name="message"]').value,
    phone: ""
  };
  
  fetch("http://localhost:8000/api/contact/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(formData)
  })
  .then(response => {
    if(!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  })
  .then(data => {
    if(data.id) {
      // Show success message and hide form
      form.style.display = "none";
      form.reset();
      const successMsg = document.getElementById("contactSuccess");
      successMsg.style.display = "block";
      successMsg.scrollIntoView({ behavior: 'smooth' });
    } else {
      alert("Error: " + JSON.stringify(data));
    }
  })
  .catch(error => {
    console.error("Error:", error);
    alert("Error submitting form: " + error);
  });
});
