from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from ...services.configuracion_calendario_service import ConfiguracionCalendarioService as BloqueoService


def bloqueo_lista(request):
    bloqueos = BloqueoService.get_all_bloqueos()
    return render(request, 'citas/configuraciones/configuracion_lista.html', {
        'bloqueos': bloqueos
    })


def bloqueo_create(request):
    if request.method == 'POST':
        try:
            BloqueoService.create_bloqueo(
                tipo             = request.POST.get('tipo'),
                fecha_inicio     = request.POST.get('fecha_inicio'),
                fecha_fin        = request.POST.get('fecha_fin') or None,
                hora_inicio      = request.POST.get('hora_inicio') or None,
                hora_fin         = request.POST.get('hora_fin') or None,
                recurrencia      = request.POST.get('recurrencia'),
                motivo           = request.POST.get('motivo'),
                capacidad_maxima = request.POST.get('capacidad_maxima') or None,
            )
            messages.success(request, 'Bloqueo creado correctamente.')
            return redirect('configuracion_lista')
        except (ValueError, Exception) as e:
            messages.error(request, str(e))

    return render(request, 'citas/configuraciones/configuracion_form.html', {
        'accion': 'Crear'
    })


def bloqueo_editar(request, bloqueo_id):
    bloqueo = BloqueoService.get_bloqueo_by_id(bloqueo_id)
    if not bloqueo:
        messages.error(request, 'El bloqueo no existe.')
        return redirect('configuracion_lista')

    if request.method == 'POST':
        try:
            BloqueoService.update_bloqueo(
                bloqueo_id,
                tipo             = request.POST.get('tipo'),
                fecha_inicio     = request.POST.get('fecha_inicio'),
                fecha_fin        = request.POST.get('fecha_fin') or None,
                hora_inicio      = request.POST.get('hora_inicio') or None,
                hora_fin         = request.POST.get('hora_fin') or None,
                recurrencia      = request.POST.get('recurrencia'),
                motivo           = request.POST.get('motivo'),
                capacidad_maxima = request.POST.get('capacidad_maxima') or None,
                activo           = request.POST.get('activo') == 'on',
            )
            messages.success(request, 'Bloqueo actualizado correctamente.')
            return redirect('configuracion_lista')
        except (ValueError, Exception) as e:
            messages.error(request, str(e))

    return render(request, 'citas/configuraciones/configuracion_form.html', {
        'bloqueo': bloqueo,
        'accion':  'Editar'
    })


def bloqueo_eliminar(request, bloqueo_id):
    bloqueo = BloqueoService.get_bloqueo_by_id(bloqueo_id)
    if not bloqueo:
        messages.error(request, 'El bloqueo no existe.')
        return redirect('bloqueos_lista')

    if request.method == 'POST':
        try:
            BloqueoService.delete_bloqueo(bloqueo_id)
            messages.success(request, 'Bloqueo eliminado correctamente.')
            return redirect('bloqueos_lista')
        except ValueError as e:
            messages.error(request, str(e))

    return render(request, 'confirmar_eliminacion.html', {
        'object':     bloqueo,
        'cancel_url': reverse('bloqueos_lista')
    })