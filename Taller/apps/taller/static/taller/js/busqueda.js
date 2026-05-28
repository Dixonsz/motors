// Dynamic placeholder update logic
function updatePlaceholder(type) {
  const input = document.getElementById('valor');
  if (!input) {
    return;
  }
  if (type === 'Placa') {
    input.placeholder = 'Placa: ABC123';
  } else {
    input.placeholder = 'Cédula: 123456789';
  }
}

// Add subtle animation on form submit
const searchForm = document.getElementById('searchForm');
if (searchForm) {
  searchForm.addEventListener('submit', function () {
    const btn = this.querySelector('button[type="submit"]');
    if (!btn) {
      return;
    }
    btn.innerHTML =
      '<span class="material-symbols-outlined animate-spin">sync</span> Consultando...';
    btn.classList.add('opacity-80');
  });
}

// Initialize with default state
document.addEventListener('DOMContentLoaded', () => {
  const checkedRadio = document.querySelector('input[name="tipo"]:checked');
  if (checkedRadio) {
    updatePlaceholder(checkedRadio.value);
  }
});
