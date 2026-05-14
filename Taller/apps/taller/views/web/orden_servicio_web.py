from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.urls import reverse
from ...services.orden_servicio_service import OrdenServicioService
from ...services.recepcion_service import RecepcionService
from ....autenticacion.services.usuario_service import UsuarioService
from ....vehiculos.services.estado_service import EstadoService
from config.security import access_required

ORDEN_ERROR="La orden de servicio no existe o no se puede procesar la solicitud."


@access_required("Ordenes", "ver")
def orden_lista(request):
    ordenes = OrdenServicioService.get_all_ordenes_servicio()
    paginator = Paginator(ordenes, 10)
    page_number = request.GET.get('page')
    ordenes = paginator.get_page(page_number)
    return render(request, 'ordenes/ordenes_lista.html', {'ordenes': ordenes})


@access_required("Ordenes", "ver")
def orden_detalle(request, orden_id):
    orden = OrdenServicioService.get_orden_servicio_by_id(orden_id)
    if not orden:
        messages.error(request, ORDEN_ERROR)
        return redirect('ordenes_lista')

    detalles = orden.ordenes_detalle.all()
    return render(request, 'ordenes/ordenes_detalle.html', {
        'orden': orden,
        'detalles': detalles
    })


@access_required("Ordenes", "crear")
def orden_create(request):
    if request.method == 'POST':
        try:
            OrdenServicioService.create_orden_servicio(
                recepcion_id=request.POST.get('recepcion_id'),
                usuario_id=request.POST.get('usuario_id'),
                estado_id=request.POST.get('estado_id'),
                diagnostico=request.POST.get('diagnostico'),
                observaciones=request.POST.get('observaciones')
            )
            messages.success(request, 'Orden de servicio creada correctamente.')
            return redirect('ordenes_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    recepciones = RecepcionService.get_all_recepciones()
    usuarios    = UsuarioService.get_all_usuarios()
    estados     = EstadoService.get_all_estados()

    return render(request, 'ordenes/ordenes_crear.html', {
        'recepciones': recepciones,
        'usuarios': usuarios,
        'estados': estados
    })


@access_required("Ordenes", "editar")
def orden_editar(request, orden_id):
    orden = OrdenServicioService.get_orden_servicio_by_id(orden_id)
    if not orden:
        messages.error(request, ORDEN_ERROR)
        return redirect('ordenes_lista')

    if request.method == 'POST':
        try:
            OrdenServicioService.update_orden_servicio(
                orden_id,
                usuario_id=request.POST.get('usuario_id'),
                estado_id=request.POST.get('estado_id'),
                diagnostico=request.POST.get('diagnostico'),
                observaciones=request.POST.get('observaciones')
            )
            messages.success(request, 'Orden actualizada correctamente.')
            return redirect('orden_detalle', orden_id=orden_id)
        except ValueError as exc:
            messages.error(request, str(exc))

    usuarios = UsuarioService.get_all_usuarios()
    estados  = EstadoService.get_all_estados()

    return render(request, 'ordenes/ordenes_editar.html', {
        'orden': orden,
        'usuarios': usuarios,
        'estados': estados
    })


@access_required("Ordenes", "editar")
def orden_cerrar(request, orden_id):
    orden = OrdenServicioService.get_orden_servicio_by_id(orden_id)
    if not orden:
        messages.error(request, ORDEN_ERROR)
        return redirect('ordenes_lista')

    if request.method == 'POST':
        try:
            OrdenServicioService.cerrar_orden_servicio(orden_id)
            messages.success(request, 'Orden cerrada correctamente.')
            return redirect('orden_detalle', orden_id=orden_id)
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'ordenes/ordenes_cerrar.html', {'orden': orden})


@access_required("Ordenes", "eliminar")
def orden_eliminar(request, orden_id):
    orden = OrdenServicioService.get_orden_servicio_by_id(orden_id)
    if not orden:
        messages.error(request, ORDEN_ERROR)
        return redirect('ordenes_lista')

    if request.method == 'POST':
        try:
            OrdenServicioService.delete_orden_servicio(orden_id)
            messages.success(request, 'Orden eliminada correctamente.')
            return redirect('ordenes_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'confirmar_eliminacion.html', {'object': orden, 'cancel_url': reverse('ordenes_lista')})
