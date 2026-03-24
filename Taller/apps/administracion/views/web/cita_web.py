from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from ...services.cita_service import CitaService
from ...services.vehiculo_service import VehiculoService
from ...services.servicio_service import ServicioService

def cita_lista(request):
    citas = CitaService.get_all_citas()
    paginator = Paginator(citas, 10)
    page_number = request.GET.get('page')
    citas = paginator.get_page(page_number)

    return render(request, 'citas/citas_lista.html', {'citas': citas})


def calendario_citas_lista(request):
    citas = CitaService.get_all_citas()

    return render(request, 'calendarios/calendarios_lista.html', {'citas': citas})

def cita_create(request):
    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        hora_inicio = request.POST.get('hora_inicio')
        hora_fin = request.POST.get('hora_fin')
        servicio_id = request.POST.get('servicio_id')
        servicio_ids = request.POST.getlist('servicio_ids')
        vehiculo_id = request.POST.get('vehiculo_id')
        anotaciones = request.POST.get('anotaciones')

        try:
            citas = CitaService.create_citas(
                vehiculo_id=vehiculo_id,
                servicio_id=servicio_id,
                servicio_ids=servicio_ids,
                fecha=fecha,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin,
                anotaciones=anotaciones,
            )
            cantidad = len(citas)
            messages.success(request, f'Se crearon {cantidad} cita(s) correctamente.')
            return redirect('citas_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    servicios = ServicioService.get_all_servicios()
    vehiculos = VehiculoService.get_all_vehiculos()
    return render(request, 'citas/citas_crear.html', {'servicios': servicios, 'vehiculos': vehiculos})


def cita_editar(request, cita_id):
    cita = CitaService.get_cita_by_id(cita_id)
    servicios = ServicioService.get_all_servicios()
    vehiculos = VehiculoService.get_all_vehiculos()
    if not cita:
        messages.error(request, 'La cita no existe.')
        return redirect('citas_lista')

    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        hora_inicio = request.POST.get('hora_inicio')
        hora_fin = request.POST.get('hora_fin')
        servicio_id = request.POST.get('servicio_id')
        vehiculo_id = request.POST.get('vehiculo_id')
        anotaciones = request.POST.get('anotaciones')

        try:
            CitaService.update_cita(
                cita_id=cita_id,
                vehiculo_id=vehiculo_id,
                servicio_id=servicio_id,
                fecha=fecha,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin,
                anotaciones=anotaciones,
            )
            messages.success(request, 'Cita actualizada correctamente.')
            return redirect('citas_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'citas/citas_editar.html', {'cita': cita, 'servicios': servicios, 'vehiculos': vehiculos})

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
