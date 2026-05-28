// Simple micro-interaction for rows
document.querySelectorAll('tr').forEach((row) => {
  row.addEventListener('mouseenter', () => {
    row.style.transition = 'background-color 0.2s ease';
  });
});

document.querySelectorAll('[data-fuel-level]').forEach((bar) => {
  const value = Number.parseFloat(bar.dataset.fuelLevel);
  const clamped = Number.isFinite(value)
    ? Math.min(Math.max(value, 0), 100)
    : 0;
  bar.style.width = `${clamped}%`;
});

// Atmospheric fade-in
window.addEventListener('load', () => {
  document.body.classList.add('opacity-0');
  setTimeout(() => {
    document.body.classList.remove('opacity-0');
    document.body.classList.add('transition-opacity', 'duration-700', 'opacity-100');
  }, 50);
});
