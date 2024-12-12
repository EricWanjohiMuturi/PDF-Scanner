const loginButton = document.getElementById('loginButton');

    loginButton.addEventListener('click', () => {
      // Add the loading state
      loginButton.classList.add('btn-loading');
      loginButton.disabled = true;

      // Simulate a validation process (e.g., 3 seconds)
      setTimeout(() => {
        // Remove the loading state
        loginButton.classList.remove('btn-loading');
        loginButton.disabled = false;

        alert('Validation process complete!');
      }, 3000); // 3-second delay
    });