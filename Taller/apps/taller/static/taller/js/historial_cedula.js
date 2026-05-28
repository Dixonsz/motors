// Micro-interaction for hover states on data rows
document.querySelectorAll('tbody tr').forEach((row) => {
  row.addEventListener('mouseenter', () => {
    row
      .querySelector('.material-symbols-outlined')
      ?.classList.add('translate-x-1');
  });
  row.addEventListener('mouseleave', () => {
    row
      .querySelector('.material-symbols-outlined')
      ?.classList.remove('translate-x-1');
  });
});
