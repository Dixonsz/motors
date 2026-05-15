from django.shortcuts import render
from apps.agenda.services.calendario_cita_service import CalendarioService
from apps.agenda.services.configuracion_calendario_service import ConfiguracionCalendarioService
from django.http import JsonResponse
from config.security import access_required


@access_required("Citas", "ver")
def calendario_view(request):
    return render(request, 'calendario/citas_calendario.html')


@access_required("Citas", "ver")
def citas_calendario(request):
    eventos  = CalendarioService.get_eventos_calendario()
    bloqueos = ConfiguracionCalendarioService.get_bloqueos_para_calendario()
    return JsonResponse(eventos + bloqueos, safe=False)


@access_required("Citas", "ver")
def calendario_form_data(request):
    data = CalendarioService.get_form_data()
    return JsonResponse(data)


@access_required("Citas", "ver")
def calendario_vehiculos_por_cliente(request, cliente_id):
    vehiculos = CalendarioService.get_vehiculos_por_cliente(cliente_id)
    return JsonResponse({'vehiculos': vehiculos})
