from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from apps.agenda.services.configuracion_calendario_service import ConfiguracionCalendarioService as BloqueoService
from config.security import access_required


@access_required("Configuraciones", "ver")
def configuracion_lista(request):
    bloqueos = BloqueoService.get_all_bloqueos()
    return render(request, 'calendario/configuracion/configuracion_lista.html', {
        'bloqueos': bloqueos
    })


@access_required("Configuraciones", "crear")
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
                dias_laborales   = request.POST.getlist('dias_laborales'),
            )
            messages.success(request, 'Configuración creada correctamente.')
            return redirect('configuracion_lista')
        except Exception as e:
            messages.error(request, str(e))

    return render(request, 'calendario/configuracion/configuracion_form.html', {
        'accion': 'Crear',
        'bloqueo': None,
    })


@access_required("Configuraciones", "editar")
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
                dias_laborales   = request.POST.getlist('dias_laborales'),
            )
            messages.success(request, 'Configuración actualizada correctamente.')
            return redirect('configuracion_lista')
        except Exception as e:
            messages.error(request, str(e))

    return render(request, 'calendario/configuracion/configuracion_form.html', {
        'configuracion': configuracion,
        'bloqueo': configuracion,
        'accion': 'Editar'
    })


@access_required("Configuraciones", "eliminar")
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