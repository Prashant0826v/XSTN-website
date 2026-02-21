document.getElementById("joinForm").addEventListener("submit", function(e){
  e.preventDefault();
  
  const formData = {
    full_name: this.querySelector('input[name="full_name"]').value,
    email: this.querySelector('input[name="email"]').value,
    role: this.querySelector('select[name="role"]').value,
    message: this.querySelector('textarea[name="message"]').value
  };
  
  fetch("http://127.0.0.1:8000/api/api/join/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(formData)
  })
  .then(response => response.json())
  .then(data => {
    if(data.id) {
      // Show success message and hide form
      this.style.display = "none";
      const successMsg = document.getElementById("successMsg");
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
