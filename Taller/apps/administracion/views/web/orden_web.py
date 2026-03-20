from django.shortcuts import redirect, render
from django.contrib import messages
from ...services.orden_service import OrdenService
from ...services.orden_servicio_service import OrdenServicioService
from ...services.usuario_service import UsuarioService
from ...services.servicio_service import ServicioService
from ...services.estado_service import EstadoService


def _get_orden_gestion_context(orden=None):
    detalle_items = []
    total = 0
    recepciones_disponibles = OrdenService.get_recepciones_disponibles(
        orden_id_excluir=orden.id if orden else None
    )

    if orden:
        detalles = OrdenServicioService.get_detalles_by_orden(orden.id)
        total = OrdenServicioService.get_total_by_orden(orden.id)
        detalle_items = [
            {
                'detalle': detalle,
                'subtotal': detalle.precio * detalle.cantidad,
            }
            for detalle in detalles
        ]

    return {
        'orden': orden,
        'usuarios': UsuarioService.get_all_usuarios(),
        'recepciones': recepciones_disponibles,
        'servicios': ServicioService.get_all_servicios(),
        'detalle_items': detalle_items,
        'total_orden': total,
        'estados': EstadoService.get_all_estados().filter(is_active=True),
    }


def _procesar_accion_orden(request, orden):
    accion = request.POST.get('action', 'guardar_orden')

    if accion == 'guardar_orden':
        recepcion_id = request.POST.get('recepcion_id')
        usuario_id = request.POST.get('usuario_id')
        diagnostico = request.POST.get('diagnostico')
        estado_id = request.POST.get('estado_id') or request.POST.get('estado')

        if orden:
            OrdenService.update_orden(
                orden.id,
                recepcion_id=recepcion_id,
                usuario_id=usuario_id,
                diagnostico=diagnostico,
                estado_id=estado_id,
            )
            messages.success(request, 'Orden actualizada correctamente.')
            return orden

        orden = OrdenService.create_orden(
            recepcion_id=recepcion_id,
            usuario_id=usuario_id,
            diagnostico=diagnostico,
            estado_id=estado_id,
        )
        messages.success(request, 'Orden creada. Ahora puedes gestionar sus servicios en esta misma vista.')
        return orden

    if not orden:
        raise ValueError('Primero debes guardar la orden para gestionar sus servicios.')

    if accion == 'agregar_detalle':
        OrdenServicioService.create_detalle(
            orden_id=orden.id,
            servicio_id=request.POST.get('servicio_id'),
            cantidad=request.POST.get('cantidad'),
            precio=request.POST.get('precio'),
            observaciones=request.POST.get('observaciones'),
        )
        messages.success(request, 'Servicio agregado a la orden correctamente.')
        return orden

    if accion == 'actualizar_detalle':
        OrdenServicioService.update_detalle(
            detalle_id=request.POST.get('detalle_id'),
            cantidad=request.POST.get('cantidad'),
            precio=request.POST.get('precio'),
            observaciones=request.POST.get('observaciones'),
        )
        messages.success(request, 'Detalle de servicio actualizado correctamente.')
        return orden

    if accion == 'eliminar_detalle':
        OrdenServicioService.delete_detalle(
            detalle_id=request.POST.get('detalle_id'),
            orden_id=orden.id,
        )
        messages.success(request, 'Detalle de servicio eliminado correctamente.')
        return orden

    raise ValueError('Accion no valida para la orden.')

def orden_lista(request):
    ordenes = OrdenService.get_all_ordenes()

    orden_items = [
        {
            'orden': orden,
            'total': OrdenServicioService.get_total_by_orden(orden.id),
        }
        for orden in ordenes
    ]

    return render(request, 'ordenes/ordenes_lista.html', {'orden_items': orden_items})

def orden_gestion(request, orden_id=None):
    orden = None
    if orden_id is not None:
        orden = OrdenService.get_orden_by_id(orden_id)
        if not orden:
            messages.error(request, 'La orden solicitada no existe.')
            return redirect('ordenes_lista')

    if request.method == 'POST':
        try:
            orden = _procesar_accion_orden(request, orden)
        except ValueError as exc:
            messages.error(request, str(exc))

        if orden:
            return redirect('ordenes_editar', orden_id=orden.id)
        return redirect('ordenes_crear')

    return render(request, 'ordenes/ordenes_editar.html', _get_orden_gestion_context(orden))


def orden_create(request):
    return orden_gestion(request)


def orden_editar(request, orden_id):
    return orden_gestion(request, orden_id=orden_id)


def orden_detalle_agregar(request, orden_id):
    orden = OrdenService.get_orden_by_id(orden_id)
    if not orden:
        messages.error(request, 'La orden solicitada no existe.')
        return redirect('ordenes_lista')

    if request.method != 'POST':
        return redirect('ordenes_editar', orden_id=orden_id)

    servicio_id = request.POST.get('servicio_id')
    cantidad = request.POST.get('cantidad')
    precio = request.POST.get('precio')
    observaciones = request.POST.get('observaciones')

    try:
        OrdenServicioService.create_detalle(
            orden_id=orden_id,
            servicio_id=servicio_id,
            cantidad=cantidad,
            precio=precio,
            observaciones=observaciones,
        )
        messages.success(request, 'Servicio agregado a la orden correctamente.')
    except ValueError as exc:
        messages.error(request, str(exc))

    return redirect('ordenes_editar', orden_id=orden_id)


def orden_detalle_eliminar(request, orden_id, detalle_id):
    orden = OrdenService.get_orden_by_id(orden_id)
    if not orden:
        messages.error(request, 'La orden solicitada no existe.')
        return redirect('ordenes_lista')

    if request.method != 'POST':
        return redirect('ordenes_editar', orden_id=orden_id)

    try:
        OrdenServicioService.delete_detalle(detalle_id=detalle_id, orden_id=orden_id)
        messages.success(request, 'Detalle de servicio eliminado correctamente.')
    except ValueError as exc:
        messages.error(request, str(exc))

    return redirect('ordenes_editar', orden_id=orden_id)


def orden_detalle_actualizar(request, orden_id, detalle_id):
    orden = OrdenService.get_orden_by_id(orden_id)
    if not orden:
        messages.error(request, 'La orden solicitada no existe.')
        return redirect('ordenes_lista')

    if request.method != 'POST':
        return redirect('ordenes_editar', orden_id=orden_id)

    cantidad = request.POST.get('cantidad')
    precio = request.POST.get('precio')
    observaciones = request.POST.get('observaciones')

    try:
        OrdenServicioService.update_detalle(
            detalle_id=detalle_id,
            cantidad=cantidad,
            precio=precio,
            observaciones=observaciones,
        )
        messages.success(request, 'Detalle de servicio actualizado correctamente.')
    except ValueError as exc:
        messages.error(request, str(exc))

    return redirect('ordenes_editar', orden_id=orden_id)

def orden_eliminar(request, orden_id):
    orden = OrdenService.get_orden_by_id(orden_id)
    if not orden:
        messages.error(request, 'La orden solicitada no existe.')
        return redirect('ordenes_lista')

    if request.method == 'POST':
        try:
            OrdenService.delete_orden(orden_id)
            return redirect('ordenes_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'ordenes/ordenes_eliminar.html', {'orden': orden})

