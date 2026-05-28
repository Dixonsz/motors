from datetime import datetime

from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.urls import reverse
from apps.agenda.services.cita_service import CitaService
from apps.taller.services.cliente_service import ClienteService
from apps.vehiculos.services.vehiculo_service import VehiculoService
from apps.agenda.services.servicio_service import ServicioService
from apps.autenticacion.services.usuario_service import UsuarioService
from apps.vehiculos.services.estado_service import EstadoService
from config.security import access_required, protected_error_to_message


@access_required("Citas", "ver")

def cita_lista(request):

    vehiculo = request.GET.get('vehiculo', '').strip()
    cliente = request.GET.get('cliente', '').strip()
    fecha_str = request.GET.get('fecha', '').strip()

    fecha = None
    if fecha_str:
        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, 'La fecha no tiene el formato correcto (YYYY-MM-DD).')
    
    citas = CitaService.get_citas_filtradas(cliente=cliente or None, vehiculo=vehiculo or None, fecha=fecha)

    paginator = Paginator(citas, 10)
    page_number = request.GET.get('page')
    citas = paginator.get_page(page_number)
    filtros_query = request.GET.copy()
    filtros_query.pop('page', None)
    return render(request, 'citas/citas_lista.html', {
        'citas': citas,
        'filtros': {
            'vehiculo': vehiculo,
            'cliente': cliente,
            'fecha': fecha_str
        },
        'filtros_query': filtros_query.urlencode()
    })


@access_required("Citas", "crear")
def cita_create(request):
    if request.method == 'POST':
        try:
            servicios_id = request.POST.getlist('servicios_id')  
            CitaService.create_cita(
                vehiculo_id=request.POST.get('vehiculo_id') or None,
                cliente_id=request.POST.get('cliente_id') or None,
                servicios_id=servicios_id,
                usuario_id=request.POST.get('usuario_id'),
                fecha=request.POST.get('fecha'),
                hora_inicio=request.POST.get('hora_inicio'),
                estado_id=request.POST.get('estado_id'),
                anotaciones=request.POST.get('anotaciones')
            )
            messages.success(request, 'Cita creada correctamente.')
            return redirect('citas_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    clientes  = ClienteService.get_all_clientes()
    vehiculos = VehiculoService.get_all_vehiculos()
    servicios = ServicioService.get_all_servicios()
    usuarios  = UsuarioService.get_all_usuarios()
    estados   = EstadoService.get_all_estados()

    return render(request, 'citas/citas_crear.html', {
        'clientes': clientes,
        'vehiculos': vehiculos,
        'servicios': servicios,
        'usuarios': usuarios,
        'estados': estados
    })


@access_required("Citas", "editar")
def cita_editar(request, cita_id):
    cita = CitaService.get_cita_by_id(cita_id)
    if not cita:
        messages.error(request, 'La cita no existe.')
        return redirect('citas_lista')

    if request.method == 'POST':
        try:
            servicios_id = request.POST.getlist('servicios_id')
            CitaService.update_cita(
                cita_id,
                vehiculo_id=request.POST.get('vehiculo_id') or None,
                cliente_id=request.POST.get('cliente_id') or None,
                servicios_id=servicios_id or None,
                usuario_id=request.POST.get('usuario_id'),
                fecha=request.POST.get('fecha'),
                hora_inicio=request.POST.get('hora_inicio'),
                estado_id=request.POST.get('estado_id'),
                anotaciones=request.POST.get('anotaciones')
            )
            messages.success(request, 'Cita actualizada correctamente.')
            return redirect('citas_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    clientes  = ClienteService.get_all_clientes()
    vehiculos = VehiculoService.get_all_vehiculos()
    servicios = ServicioService.get_all_servicios()
    usuarios  = UsuarioService.get_all_usuarios()
    estados   = EstadoService.get_all_estados()

    return render(request, 'citas/citas_editar.html', {
        'cita': cita,
        'clientes': clientes,
        'vehiculos': vehiculos,
        'servicios': servicios,
        'usuarios': usuarios,
        'estados': estados
    })


@access_required("Citas", "eliminar")
@protected_error_to_message
def cita_eliminar(request, cita_id):
    cita = CitaService.get_cita_by_id(cita_id)
    if not cita:
        messages.error(request, 'La cita no existe.')
        return redirect('citas_lista')

    if request.method == 'POST':
        try:
            CitaService.delete_cita(cita_id)
            messages.success(request, 'Cita eliminada correctamente.')
            return redirect('citas_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'confirmar_eliminacion.html', {'object': cita, 'cancel_url': reverse('citas_lista')})
