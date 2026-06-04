// JS para autocompletar datos del cliente al seleccionar en el formulario de crear vehículo
$(document).ready(function () {
    // Inicializa select2 si está presente
    if ($.fn.select2) {
        $('#cliente_id').select2({
            width: '100%',
            placeholder: 'Seleccione el propietario del vehiculo',
            allowClear: true
        });
    }

    // Obtiene la URL base para el detalle del cliente
    var scriptTag = document.querySelector('script[src*="vehiculos.js"]');
    var baseUrl = scriptTag ? scriptTag.getAttribute('data-cliente-detalle-url') : null;
    if (!baseUrl) return;

    $('#cliente_id').on('change', function () {
        var clienteId = $(this).val();
        if (!clienteId) {
            limpiarCamposCliente();
            return;
        }
        // Reemplaza el marcador de id en rutas como /clientes/0/detalle-json/
        var url = baseUrl.replace('/0/', '/' + clienteId + '/');
        $.get(url, function (data) {
            if (data && data.id) {
                $('#cliente_cedula').val(data.cedula || '');
                $('#cliente_telefono').val(data.telefono || '');
                $('#cliente_correo').val(data.correo || '');
                $('#cliente_direccion').val(data.direccion || '');
            } else {
                limpiarCamposCliente();
            }
        }).fail(function () {
            limpiarCamposCliente();
        });
    });

    if ($('#cliente_id').val()) {
        $('#cliente_id').trigger('change');
    }

    function limpiarCamposCliente() {
        $('#cliente_cedula').val('');
        $('#cliente_telefono').val('');
        $('#cliente_correo').val('');
        $('#cliente_direccion').val('');
    }
});
