from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.urls import reverse
from ...services.recepcion_service import RecepcionService
from ....vehiculos.services.vehiculo_service import VehiculoService
from ....autenticacion.services.usuario_service import UsuarioService
from config.security import access_required


@access_required("Recepciones", "ver")
def recepcion_lista(request):
    recepciones = RecepcionService.get_all_recepciones()
    paginator = Paginator(recepciones, 10)
    page_number = request.GET.get('page')
    recepciones = paginator.get_page(page_number)
    return render(request, 'recepciones/recepciones_lista.html', {'recepciones': recepciones})


@access_required("Recepciones", "crear")
def recepcion_create(request):
    if request.method == 'POST':
        try:
            RecepcionService.create_recepcion(
                vehiculo_id=request.POST.get('vehiculo_id'),
                usuario_id=request.POST.get('usuario_id'),
                observaciones=request.POST.get('observaciones', ''),
                kilometraje=int(request.POST.get('kilometraje')),
                nivel_combustible=int(request.POST.get('nivel_combustible'))
            )
            messages.success(request, 'Recepción registrada correctamente.')
            return redirect('recepciones_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    vehiculos = VehiculoService.get_all_vehiculos()
    usuarios  = UsuarioService.get_all_usuarios()

    return render(request, 'recepciones/recepciones_crear.html', {
        'vehiculos': vehiculos,
        'usuarios': usuarios
    })


@access_required("Recepciones", "ver")
def recepcion_detalle(request, recepcion_id):
    recepcion = RecepcionService.get_recepcion_by_id(recepcion_id)
    if not recepcion:
        messages.error(request, 'La recepción no existe.')
        return redirect('recepciones_lista')

    return render(request, 'recepciones/recepciones_detalle.html', {'recepcion': recepcion})


@access_required("Recepciones", "eliminar")
def recepcion_eliminar(request, recepcion_id):
    recepcion = RecepcionService.get_recepcion_by_id(recepcion_id)
    if not recepcion:
        messages.error(request, 'La recepción no existe.')
        return redirect('recepciones_lista')

    if request.method == 'POST':
        try:
            RecepcionService.delete_recepcion(recepcion_id)
            messages.success(request, 'Recepción eliminada correctamente.')
            return redirect('recepciones_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'confirmar_eliminacion.html', {'object': recepcion, 'cancel_url': reverse('recepciones_lista')})
