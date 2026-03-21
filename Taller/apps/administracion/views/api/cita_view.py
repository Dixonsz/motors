from django.views.decorators.cache import never_cache
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from ...serializers.cita_serializers import CitaSerializer
from ...services.cita_service import CitaService


class CitaView(viewsets.ViewSet):

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
            estado_id = data.get('estado_id', data.get('estado'))
            servicio_ids = None
            if hasattr(data, 'getlist'):
                servicio_ids = data.getlist('servicio_ids')

            if servicio_ids in (None, []):
                servicio_ids = data.get('servicio_ids')

            citas = CitaService.create_citas(
                vehiculo_id=data.get('vehiculo_id', data.get('vehiculo')),
                servicio_id=data.get('servicio_id', data.get('servicio')),
                servicio_ids=servicio_ids,
                fecha=data.get('fecha'),
                hora_inicio=data.get('hora_inicio'),
                hora_fin=data.get('hora_fin'),
                estado_id=estado_id,
                anotaciones=data.get('anotaciones'),
                usuario_id=data.get('usuario_id')
            )
        except ValueError as exc:
            return Response({'error': str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        if len(citas) == 1:
            serializer = CitaSerializer(citas[0])
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        serializer = CitaSerializer(citas, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @never_cache
    def update(self, request, pk=None):
        data = request.data

        try:
            estado_id = data.get('estado_id', data.get('estado'))
            cita = CitaService.update_cita(
                cita_id=pk,
                vehiculo_id=data.get('vehiculo_id', data.get('vehiculo')),
                servicio_id=data.get('servicio_id', data.get('servicio')),
                fecha=data.get('fecha'),
                hora_inicio=data.get('hora_inicio'),
                hora_fin=data.get('hora_fin'),
                estado_id=estado_id,
                anotaciones=data.get('anotaciones'),
                usuario_id=data.get('usuario_id'),
            )
        except ValueError as exc:
            return Response({'error': str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CitaSerializer(cita)
        return Response(serializer.data)

    @never_cache
    def destroy(self, request, pk=None):
        try:
            CitaService.delete_cita(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError as exc:
            return Response({'error': str(exc)}, status=status.HTTP_404_NOT_FOUND)

    @never_cache
    @action(detail=False, methods=['get'], url_path='disponibilidad')
    def disponibilidad(self, request):
        fecha = request.query_params.get('fecha')
        servicio_id = request.query_params.get('servicio_id')
        vehiculo_id = request.query_params.get('vehiculo_id')
        usuario_id = request.query_params.get('usuario_id', request.query_params.get('mecanico_id'))

        if not fecha:
            return Response({'error': 'El parametro fecha es requerido.'}, status=status.HTTP_400_BAD_REQUEST)

        if not servicio_id:
            return Response({'error': 'El parametro servicio_id es requerido.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            disponibilidad = CitaService.get_disponibilidad(
                fecha=fecha,
                servicio_id=servicio_id,
                vehiculo_id=vehiculo_id,
                usuario_id=usuario_id,
            )
            return Response(disponibilidad)
        except ValueError as exc:
            return Response({'error': str(exc)}, status=status.HTTP_400_BAD_REQUEST)
