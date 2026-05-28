from datetime import datetime
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.urls import reverse
from ...services.recepcion_service import RecepcionService
from ....vehiculos.services.vehiculo_service import VehiculoService
from ....autenticacion.services.usuario_service import UsuarioService
from ...services.evidencia_service import EvidenciaService
from config.security import access_required, protected_error_to_message


@access_required("Recepciones", "ver")
def recepcion_lista(request):
    vehiculo = request.GET.get('vehiculo', '').strip()
    cliente = request.GET.get('cliente', '').strip()
    fecha_str = request.GET.get('fecha_ingreso', '').strip()
    usuario_id = request.GET.get('usuario_id', '').strip()

    fecha_ingreso = None
    if fecha_str:
        try:
            fecha_ingreso = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, 'La fecha no tiene el formato correcto (YYYY-MM-DD).')

    recepciones = RecepcionService.get_recepciones_filtradas(
        vehiculo=vehiculo or None,
        cliente=cliente or None,
        usuario=usuario_id or None,
        fecha_ingreso=fecha_ingreso
    )
    paginator = Paginator(recepciones, 10)
    page_number = request.GET.get('page')
    recepciones = paginator.get_page(page_number)
    usuarios = UsuarioService.get_all_usuarios()
    filtros_query = request.GET.copy()
    filtros_query.pop('page', None)

    return render(request, 'recepciones/recepciones_lista.html', {
        'recepciones': recepciones,
        'usuarios': usuarios,
        'filtros': {
            'vehiculo': vehiculo,
            'cliente': cliente,
            'fecha_ingreso': fecha_str,
            'usuario_id': usuario_id
        },
        'filtros_query': filtros_query.urlencode()
    })


@access_required("Recepciones", "crear")
def recepcion_create(request):
    if request.method == 'POST':
        try:
            recepcion = RecepcionService.create_recepcion(
                vehiculo_id=request.POST.get('vehiculo_id'),
                usuario_id=request.POST.get('usuario_id'),
                observaciones=request.POST.get('observaciones', ''),
                kilometraje=int(request.POST.get('kilometraje')),
                nivel_combustible=int(request.POST.get('nivel_combustible'))
            )

            archivos = request.FILES.getlist('evidencias')
            if archivos:
                EvidenciaService.create_multiple_evidencias(
                    recepcion_id=recepcion.id,
                    archivos=archivos,
                    tipo='foto',
                    descripcion='Evidencia fotográfica de ingreso'
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

    bloqueada = RecepcionService.is_recepcion_cerrada(recepcion)
    return render(request, 'recepciones/recepciones_detalle.html', {'recepcion': recepcion, 'bloqueada': bloqueada})


@access_required("Recepciones", "eliminar")
@protected_error_to_message
def recepcion_eliminar(request, recepcion_id):
    recepcion = RecepcionService.get_recepcion_by_id(recepcion_id)
    if not recepcion:
        messages.error(request, 'La recepción no existe.')
        return redirect('recepciones_lista')

    if RecepcionService.is_recepcion_cerrada(recepcion):
        messages.error(request, 'La recepción tiene una orden de servicio cerrada y no se puede modificar.')
        return redirect('recepciones_detalle', recepcion_id=recepcion.id)

    if request.method == 'POST':
        try:
            RecepcionService.delete_recepcion(recepcion_id)
            messages.success(request, 'Recepción eliminada correctamente.')
            return redirect('recepciones_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'confirmar_eliminacion.html', {'object': recepcion, 'cancel_url': reverse('recepciones_lista')})
