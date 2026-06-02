from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
import requests
from ...services.public.historial_public_service import HistorialPublicService
from ...serializers.public.historial_serializers import OrdenServicioPublicSerializer
from ....vehiculos.serializers.public.vehiculo_public_serializers import VehiculoPublicSerializer
from ....taller.models.orden_servicio import OrdenServicio

# Constantes
TURNSTILE_VERIFY_URL = settings.TURNSTILE_VERIFY_URL
MSG_SEGURIDAD_FALLIDA = "Verificación de seguridad fallida. Por favor, inténtalo de nuevo."
TEMPLATE_BUSQUEDA = "consulta_publica/busqueda.html"

def _verify_turnstile(token):
    """Verifica el token de Cloudflare Turnstile."""
    resp = requests.post(
        TURNSTILE_VERIFY_URL,
        data={"secret": settings.TURNSTILE_SECRET_KEY, "response": token},
    )
    return resp.json().get("success", False)


def consulta_busqueda(request):

    if request.method == 'POST':
        if not _verify_turnstile(request.POST.get('cf-turnstile-response')):
            messages.error(request, MSG_SEGURIDAD_FALLIDA)
            return render(request, TEMPLATE_BUSQUEDA, {"site_key": settings.TURNSTILE_SITE_KEY})

        tipo = request.POST.get('tipo')
        valor = request.POST.get('valor', '').strip()

        if not valor:
            messages.error(request, 'Por favor ingrese un valor para buscar.')
            return render(request, TEMPLATE_BUSQUEDA, {"site_key": settings.TURNSTILE_SITE_KEY})

        if tipo == 'placa':
            return redirect('consulta_historial_placa', placa=valor.upper())
        elif tipo == 'cedula':
            return redirect('consulta_historial_cedula', cedula=valor)
        else:
            messages.error(request, 'Tipo de búsqueda no válido.')

    return render(request, TEMPLATE_BUSQUEDA, {"site_key": settings.TURNSTILE_SITE_KEY})


def consulta_historial_placa(request, placa):
  
    try:
        resultado = HistorialPublicService.obtener_historial_por_placa(placa)
    except ValueError as exc:
        messages.error(request, str(exc))
        return redirect('consulta_busqueda')

    vehiculo_data = VehiculoPublicSerializer(resultado['vehiculo']).data
    ordenes_data = OrdenServicioPublicSerializer(resultado['ordenes'], many=True).data

    context = {
        'vehiculo': vehiculo_data,
        'ordenes': ordenes_data,
        'placa': placa,
    }
    return render(request, 'consulta_publica/historial.html', context)
    

def consulta_historial_cedula(request, cedula):
 
    try:
        resultado = HistorialPublicService.obtener_historial_por_cedula(cedula)
    except ValueError as exc:
        messages.error(request, str(exc))
        return redirect('consulta_busqueda')

    vehiculos_data = []
    for item in resultado['vehiculos']:
        vehiculos_data.append({
            'vehiculo': VehiculoPublicSerializer(item['vehiculo']).data,
            'ordenes': OrdenServicioPublicSerializer(item['ordenes'], many=True).data,
        })

    context = {
        'cliente': {
            'nombre': resultado['cliente'].nombre,
            'cedula': resultado['cliente'].cedula,
        },
        'vehiculos': vehiculos_data,
    }
    return render(request, 'consulta_publica/historial_cedula.html', context)


def consulta_orden_detalle(request, orden_id):

    try:
        orden = OrdenServicio.objects.select_related(
            'estado',
            'recepcion__vehiculo__marca',
            'recepcion__vehiculo__modelo',
            'recepcion__vehiculo__combustible',
        ).prefetch_related(
            'ordenes_detalle__servicio',
            'recepcion__evidencias',
        ).get(id=orden_id)
    except OrdenServicio.DoesNotExist:
        messages.error(request, 'La orden de servicio no existe.')
        return redirect('consulta_busqueda')

    orden_data = OrdenServicioPublicSerializer(orden).data
    vehiculo_data = VehiculoPublicSerializer(orden.recepcion.vehiculo).data
    evidencias = orden.recepcion.evidencias.all()

    context = {
        'orden': orden_data,
        'vehiculo': vehiculo_data,
        'evidencias': evidencias,
    }
    return render(request, 'consulta_publica/orden_detalle.html', context)

def ratelimit_error(request, exception=None):
    referer = request.META.get('HTTP_REFERER', '')
    back_url = 'login' if 'autenticacion' in referer else 'consulta_busqueda'
    return render(request, 'consulta_publica/429.html', {
        'back_url': back_url
    }, status=429)