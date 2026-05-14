import json
from django.http import JsonResponse
from ...services.cita_service import CitaService
from ...serializers.cita_serializers import CitaSerializer


class CalendarioApiView:

    def crear_cita(self, request):
        try:
            data = json.loads(request.body)
            cita = CitaService.create_cita(
                vehiculo_id  = data.get('vehiculo_id'),
                cliente_id   = data.get('cliente_id'),
                servicios_id = data.get('servicios_id', []),
                usuario_id   = data['usuario_id'],
                fecha        = data['fecha'],
                hora_inicio  = data['hora_inicio'],
                estado_id    = data['estado_id'],
                anotaciones  = data.get('anotaciones'),
            )
            serializer = CitaSerializer(cita)
            return JsonResponse(serializer.data, status=201)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except KeyError as e:
            return JsonResponse(
                {'error': f'Campo requerido faltante: {e.args[0]}'},
                status=400
            )
