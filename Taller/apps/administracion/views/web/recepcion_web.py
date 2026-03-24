from django.shortcuts import redirect, render
from django.contrib import messages
from django.core.paginator import Paginator
from ...services.recepcion_service import RecepcionService
from ...services.vehiculo_service import VehiculoService
from ...services.usuario_service import UsuarioService
from ...services.evidencia_service import EvidenciaService

def recepcion_lista(request):
    recepciones = RecepcionService.get_all_recepciones()
    paginator = Paginator(recepciones, 10)
    page_number = request.GET.get('page')
    recepciones = paginator.get_page(page_number)

    return render(request, 'recepciones/recepciones_lista.html', {'recepciones': recepciones})

def recepcion_create(request):
    vehiculos = VehiculoService.get_all_vehiculos()
    usuarios = UsuarioService.get_all_usuarios()

    if request.method == 'POST':
        vehiculo_id = request.POST.get('vehiculo_id')
        usuario_id = request.POST.get('usuario_id')
        fecha_ingreso = request.POST.get('fecha_ingreso')
        observaciones = request.POST.get('observaciones')
        kilometraje = request.POST.get('kilometraje')
        nivel_combustible = request.POST.get('nivel_combustible')

        try:
            recepcion = RecepcionService.create_recepcion(
                vehiculo_id,
                usuario_id,
                fecha_ingreso,
                observaciones,
                kilometraje,
                nivel_combustible
            )
        except ValueError as exc:
            messages.error(request, str(exc))
            return render(
                request,
                'recepciones/recepciones_crear.html',
                {'vehiculos': vehiculos, 'usuarios': usuarios}
            )

        return redirect('evidencia_create', recepcion_id=recepcion.id)

    return render(request, 'recepciones/recepciones_crear.html', {'vehiculos': vehiculos, 'usuarios': usuarios})    


def recepciones_editar(request, recepcion_id):
    recepcion = RecepcionService.get_recepcion_by_id(recepcion_id)
    if not recepcion:
        messages.error(request, 'La recepcion no existe.')
        return redirect('recepcion_lista')

    vehiculos = VehiculoService.get_all_vehiculos()
    usuarios = UsuarioService.get_all_usuarios()
    evidencias = EvidenciaService.get_evidencias_by_recepcion(recepcion_id) 

    if request.method == 'POST':
        vehiculo_id = request.POST.get('vehiculo_id')
        usuario_id = request.POST.get('usuario_id')
        fecha_ingreso = request.POST.get('fecha_ingreso')
        observaciones = request.POST.get('observaciones')
        kilometraje = request.POST.get('kilometraje')
        nivel_combustible = request.POST.get('nivel_combustible')

        try:
            RecepcionService.update_recepcion(
                recepcion_id,
                vehiculo_id,
                usuario_id,
                fecha_ingreso,
                observaciones,
                kilometraje,
                nivel_combustible
            )
        except ValueError as exc:
            messages.error(request, str(exc))
            return render(request, 'recepciones/recepciones_editar.html', {
                'recepcion': recepcion,
                'vehiculos': vehiculos,
                'usuarios': usuarios,
                'evidencias': evidencias
            })

        return redirect('recepcion_lista')

    return render(request, 'recepciones/recepciones_editar.html', {
        'recepcion': recepcion,
        'vehiculos': vehiculos,
        'usuarios': usuarios,
        'evidencias': evidencias
    })

def recepcion_eliminar(request, recepcion_id):
    recepcion = RecepcionService.get_recepcion_by_id(recepcion_id)
    if not recepcion:
        messages.error(request, 'La recepcion no existe.')
        return redirect('recepcion_lista')

    if request.method == 'POST':
        try:
            RecepcionService.delete_recepcion(recepcion_id)
            messages.success(request, 'Recepcion eliminada correctamente.')
            return redirect('recepcion_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'recepciones/recepciones_eliminar.html', {'recepcion_id': recepcion_id})

