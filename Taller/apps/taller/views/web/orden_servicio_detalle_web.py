from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from ...services.orden_servicio_detalle_service import OrdenServicioDetalleService
from ...services.orden_servicio_service import OrdenServicioService
from ....agenda.services.servicio_service import ServicioService
from config.security import access_required, protected_error_to_message

ORDEN_CLOSED_ERROR = "La orden de servicio está cerrada y no se puede modificar."


@access_required("Ordenes", "crear")
def detalle_create(request, orden_id):
    orden = OrdenServicioService.get_orden_servicio_by_id(orden_id)
    if not orden:
        messages.error(request, 'La orden no existe.')
        return redirect('ordenes_lista')

    if OrdenServicioService.is_orden_cerrada(orden):
        messages.error(request, ORDEN_CLOSED_ERROR)
        return redirect('orden_detalle', orden_id=orden_id)

    if request.method == 'POST':
        servicio_id = request.POST.get('servicio_id')
        precio_raw = (request.POST.get('precio') or '').strip()
        servicio = ServicioService.get_servicio_by_id(servicio_id)

        if not servicio:
            messages.error(request, 'El servicio no existe.')
            return redirect('orden_detalle', orden_id=orden_id)

        try:
            precio = Decimal(precio_raw) if precio_raw else servicio.precio_base
        except (InvalidOperation, TypeError):
            messages.error(request, 'El precio ingresado no es valido.')
            return redirect('detalle_crear', orden_id=orden_id)

        try:
            OrdenServicioDetalleService.create_detalle(
                orden_id=orden_id,
                servicio_id=servicio_id,
                precio=precio,
                cantidad=int(request.POST.get('cantidad', 1)),
                observaciones=request.POST.get('observaciones')
            )
            messages.success(request, 'Servicio agregado correctamente.')
            return redirect('orden_detalle', orden_id=orden_id)
        except ValueError as exc:
            messages.error(request, str(exc))

    servicios = ServicioService.get_all_servicios()
    return render(request, 'ordenes/detalle_crear.html', {
        'orden': orden,
        'servicios': servicios
    })


@access_required("Ordenes", "editar")
def detalle_editar(request, detalle_id):
    detalle = OrdenServicioDetalleService.get_detalle_by_id(detalle_id)
    if not detalle:
        messages.error(request, 'El detalle no existe.')
        return redirect('ordenes_lista')

    if OrdenServicioService.is_orden_cerrada(detalle.orden):
        messages.error(request, ORDEN_CLOSED_ERROR)
        return redirect('orden_detalle', orden_id=detalle.orden_id)

    if request.method == 'POST':
        try:
            OrdenServicioDetalleService.update_detalle(
                detalle_id,
                precio=int(request.POST.get('precio')),
                cantidad=int(request.POST.get('cantidad')),
                observaciones=request.POST.get('observaciones')
            )
            messages.success(request, 'Detalle actualizado correctamente.')
            return redirect('orden_detalle', orden_id=detalle.orden_id)
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'ordenes/detalle_editar.html', {'detalle': detalle})


@access_required("Ordenes", "eliminar")
@protected_error_to_message
def detalle_eliminar(request, detalle_id):
    detalle = OrdenServicioDetalleService.get_detalle_by_id(detalle_id)
    if not detalle:
        messages.error(request, 'El detalle no existe.')
        return redirect('ordenes_lista')

    if OrdenServicioService.is_orden_cerrada(detalle.orden):
        messages.error(request, ORDEN_CLOSED_ERROR)
        return redirect('orden_detalle', orden_id=detalle.orden_id)

    orden_id = detalle.orden_id

    if request.method == 'POST':
        try:
            OrdenServicioDetalleService.delete_detalle(detalle_id)
            messages.success(request, 'Servicio eliminado correctamente.')
            return redirect('orden_detalle', orden_id=orden_id)
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'confirmar_eliminacion.html', {'object': detalle, 'cancel_url': reverse('orden_detalle', kwargs={'orden_id': orden_id})})
