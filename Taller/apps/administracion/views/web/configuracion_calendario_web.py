from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from ...services.configuracion_calendario_service import ConfiguracionCalendarioService as BloqueoService


def configuracion_lista(request):
    bloqueos = BloqueoService.get_all_bloqueos()
    return render(request, 'citas/configuraciones/configuracion_lista.html', {
        'bloqueos': bloqueos
    })


def configuracion_create(request):
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
            messages.success(request, 'Configuración creada correctamente.')
            return redirect('configuracion_lista')
        except (ValueError, Exception) as e:
            messages.error(request, str(e))

    return render(request, 'citas/configuraciones/configuracion_form.html', {
        'accion': 'Crear'
    })


def configuracion_editar(request, configuracion_id):
    configuracion = BloqueoService.get_bloqueo_by_id(configuracion_id)
    if not configuracion:
        messages.error(request, 'La configuración no existe.')
        return redirect('configuracion_lista')

    if request.method == 'POST':
        try:
            BloqueoService.update_bloqueo(
                configuracion_id,
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
            messages.success(request, 'Configuración actualizada correctamente.')
            return redirect('configuracion_lista')
        except (ValueError, Exception) as e:
            messages.error(request, str(e))

    return render(request, 'citas/configuraciones/configuracion_form.html', {
        'configuracion': configuracion,
        'accion':  'Editar'
    })


def configuracion_eliminar(request, configuracion_id):
    configuracion = BloqueoService.get_bloqueo_by_id(configuracion_id)
    if not configuracion:
        messages.error(request, 'La configuración no existe.')
        return redirect('configuracion_lista')

    if request.method == 'POST':
        try:
            BloqueoService.delete_bloqueo(configuracion_id)
            messages.success(request, 'Configuración eliminada correctamente.')
            return redirect('configuracion_lista')
        except ValueError as e:
            messages.error(request, str(e))

    return render(request, 'confirmar_eliminacion.html', {
        'object':     configuracion,
        'cancel_url': reverse('configuracion_lista')
    })