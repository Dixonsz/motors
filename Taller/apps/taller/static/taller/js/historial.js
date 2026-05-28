// Simple micro-interactions for table rows
document.querySelectorAll('tbody tr').forEach((row) => {
  row.addEventListener('click', () => {
    const link = row.querySelector('a');
    if (link) {
      window.location.href = link.getAttribute('href');
    }
  });
  row.style.cursor = 'pointer';
});
