from django.shortcuts import render
from ...services.calendario_cita_service import CalendarioService
from ...services.configuracion_calendario_service import ConfiguracionCalendarioService
from django.http import JsonResponse


def calendario_view(request):
    return render(request, 'citas/calendario/citas_calendario.html')


def citas_calendario(request):
    eventos  = CalendarioService.get_eventos_calendario()
    bloqueos = ConfiguracionCalendarioService.get_bloqueos_para_calendario()
    return JsonResponse(eventos + bloqueos, safe=False)


def calendario_form_data(request):
    data = CalendarioService.get_form_data()
    return JsonResponse(data)


def calendario_vehiculos_por_cliente(request, cliente_id):
    vehiculos = CalendarioService.get_vehiculos_por_cliente(cliente_id)
    return JsonResponse({'vehiculos': vehiculos})