    (function () {
        const clienteSelect = document.getElementById('cliente_id');
        const currentScript = document.currentScript;
        const detalleUrlTemplate = currentScript ? currentScript.dataset.clienteDetalleUrl : '';
        const cedulaInput = document.getElementById('cliente_cedula');
        const telefonoInput = document.getElementById('cliente_telefono');
        const correoInput = document.getElementById('cliente_correo');
        const direccionInput = document.getElementById('cliente_direccion');

        if (!clienteSelect || !detalleUrlTemplate || !cedulaInput || !telefonoInput || !correoInput || !direccionInput) {
            return;
        }

        const limpiarCliente = () => {
            cedulaInput.value = '';
            telefonoInput.value = '';
            correoInput.value = '';
            direccionInput.value = '';
        };

        const cargarClienteSeleccionado = async () => {
            const clienteId = clienteSelect.value;

            if (!clienteId) {
                limpiarCliente();
                return;
            }

            const detalleUrl = detalleUrlTemplate.replace('/0/', '/' + clienteId + '/');

            try {
                const respuesta = await fetch(detalleUrl, {
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });

                if (!respuesta.ok) {
                    throw new Error('No se pudo obtener el cliente.');
                }

                const cliente = await respuesta.json();
                cedulaInput.value = cliente.cedula || '';
                telefonoInput.value = cliente.telefono || '';
                correoInput.value = cliente.correo || '';
                direccionInput.value = cliente.direccion || '';
            } catch (error) {
                limpiarCliente();
                console.error(error);
            }
        };

        clienteSelect.addEventListener('change', cargarClienteSeleccionado);
        cargarClienteSeleccionado();

        if (window.jQuery && window.jQuery.fn && window.jQuery.fn.select2) {
            window.jQuery(clienteSelect).select2({
                placeholder: 'Buscar cliente...',
                allowClear: true,
                width: '100%',
                minimumResultsForSearch: 0
            });
            window.jQuery(clienteSelect).on('change', cargarClienteSeleccionado);
        }
    })();