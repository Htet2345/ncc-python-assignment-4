document.querySelectorAll('.delete-form').forEach((form) => {
  form.addEventListener('submit', (event) => {
    if (!window.confirm('Are you sure?')) event.preventDefault();
  });
});
