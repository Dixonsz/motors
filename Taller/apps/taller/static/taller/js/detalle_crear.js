const servicioSelect = document.getElementById('servicio_id');
const precioInput = document.getElementById('precio');

if (servicioSelect && precioInput) {
  const setPrecioDesdeServicio = () => {
    const option = servicioSelect.options[servicioSelect.selectedIndex];
    if (!option) {
      return;
    }
    const precioBase = option.getAttribute('data-precio');
    if (precioBase && !precioInput.value) {
      precioInput.value = precioBase;
    }
  };

  servicioSelect.addEventListener('change', () => {
    precioInput.value = '';
    setPrecioDesdeServicio();
  });

  setPrecioDesdeServicio();
}
