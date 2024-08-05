document.addEventListener('DOMContentLoaded', function() {
  // Function to update button state based on localStorage
  function updateButtonState(button) {
      const id = button.dataset.id;
      const applied = localStorage.getItem(`applied_${id}`) === 'true';

      if (applied) {
          button.textContent = 'Applied';
          button.classList.remove('btn-primary');
          button.classList.add('btn-applied');
          button.disabled = true;
      } else {
          button.textContent = 'Apply';
          button.classList.remove('btn-applied');
          button.classList.add('btn-primary');
          button.disabled = false;
      }
  }

  // Attach event listeners to all "Apply" buttons
  document.querySelectorAll('.apply-btn').forEach(button => {
      // Initialize button state
      updateButtonState(button);

      button.addEventListener('click', function() {
          const id = this.dataset.id;
          // Change the button text to "Applied"
          this.textContent = 'Applied';
          // Change the button style
          this.classList.remove('btn-primary');
          this.classList.add('btn-applied');
          // Disable the button
          this.disabled = true;
          // Store the applied state in localStorage
          localStorage.setItem(`applied_${id}`, 'true');
      });
  });

  // Handle showing the modal
  document.addEventListener('show.bs.modal', function(event) {
      const button = event.relatedTarget; // Button that triggered the modal
      const modal = document.getElementById('detailsModal'); // The modal

      // Find the "Apply" button within the modal
      const applyButton = modal.querySelector('.apply-btn');
      const id = button.dataset.id; // Get the unique ID from the related button
      applyButton.dataset.id = id; // Set the ID on the modal button
      // Initialize button state based on localStorage
      updateButtonState(applyButton);
  });
});
