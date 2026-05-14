from rest_framework import status
from rest_framework.response import Response
from django.views.decorators.cache import never_cache
from ...services.cita_service import CitaService
from ...serializers.cita_serializers import CitaSerializer


class CitaView():

    @never_cache
    def list(self, request):
        citas = CitaService.get_all_citas()
        serializer = CitaSerializer(citas, many=True)
        return Response(serializer.data)

    @never_cache
    def retrieve(self, request, pk=None):
        cita = CitaService.get_cita_by_id(pk)
        if not cita:
            return Response({'error': 'Cita no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CitaSerializer(cita)
        return Response(serializer.data)

    @never_cache
    def create(self, request):
        data = request.data
        try:
            cita = CitaService.create_cita(
                vehiculo_id=data.get('vehiculo_id'),
                cliente_id=data.get('cliente_id'),
                servicios_id=data.get('servicios_id', []),
                usuario_id=data['usuario_id'],
                fecha=data['fecha'],
                hora_inicio=data['hora_inicio'],
                estado_id=data['estado_id'],
                anotaciones=data.get('anotaciones')
            )
            serializer = CitaSerializer(cita)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as e:
            return Response({'error': f'Campo requerido faltante: {e.args[0]}'}, status=status.HTTP_400_BAD_REQUEST)

    @never_cache
    def update(self, request, pk=None):
        data = request.data
        try:
            cita = CitaService.update_cita(
                pk,
                vehiculo_id=data.get('vehiculo_id'),
                cliente_id=data.get('cliente_id'),
                servicios_id=data.get('servicios_id'),
                usuario_id=data.get('usuario_id'),
                fecha=data.get('fecha'),
                hora_inicio=data.get('hora_inicio'),
                estado_id=data.get('estado_id'),
                anotaciones=data.get('anotaciones')
            )
            serializer = CitaSerializer(cita)
            return Response(serializer.data)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @never_cache
    def destroy(self, request, pk=None):
        try:
            CitaService.delete_cita(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
