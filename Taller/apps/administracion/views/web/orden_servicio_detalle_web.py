from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from ...services.orden_servicio_detalle_service import OrdenServicioDetalleService
from ...services.orden_servicio_service import OrdenServicioService
from ...services.servicio_service import ServicioService
from ...security import access_required


@access_required("Ordenes", "crear")
def detalle_create(request, orden_id):
    orden = OrdenServicioService.get_orden_servicio_by_id(orden_id)
    if not orden:
        messages.error(request, 'La orden no existe.')
        return redirect('ordenes_lista')

    if request.method == 'POST':
        try:
            OrdenServicioDetalleService.create_detalle(
                orden_id=orden_id,
                servicio_id=request.POST.get('servicio_id'),
                precio=int(request.POST.get('precio')),
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
def detalle_eliminar(request, detalle_id):
    detalle = OrdenServicioDetalleService.get_detalle_by_id(detalle_id)
    if not detalle:
        messages.error(request, 'El detalle no existe.')
        return redirect('ordenes_lista')

    orden_id = detalle.orden_id

    if request.method == 'POST':
        try:
            OrdenServicioDetalleService.delete_detalle(detalle_id)
            messages.success(request, 'Servicio eliminado correctamente.')
            return redirect('orden_detalle', orden_id=orden_id)
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'confirmar_eliminacion.html', {'object': detalle, 'cancel_url': reverse('orden_detalle', kwargs={'orden_id': orden_id})})