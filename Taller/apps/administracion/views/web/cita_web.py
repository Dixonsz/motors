from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from ...services.cita_service import CitaService
from ...services.cliente_service import ClienteService
from ...services.vehiculo_service import VehiculoService
from ...services.servicio_service import ServicioService
from ...services.usuario_service import UsuarioService
from ...services.estado_service import EstadoService


def cita_lista(request):
    citas = CitaService.get_all_citas()
    paginator = Paginator(citas, 10)
    page_number = request.GET.get('page')
    citas = paginator.get_page(page_number)
    return render(request, 'citas/citas_lista.html', {'citas': citas})


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

    return render(request, 'citas/citas_eliminar.html', {'cita': cita})