from rest_framework import status, viewsets
from rest_framework.response import Response
from django.views.decorators.cache import never_cache

from ...serializers.orden_serializers import OrdenServicioSerializer
from ...services.orden_servicio_service import OrdenServicioService


class OrdenServicioView(viewsets.ViewSet):

    @never_cache
    def list(self, request):
        orden_id = request.query_params.get('orden_id')
        if not orden_id:
            return Response({'error': 'El parametro orden_id es requerido.'}, status=status.HTTP_400_BAD_REQUEST)

        detalles = OrdenServicioService.get_detalles_by_orden(orden_id)
        serializer = OrdenServicioSerializer(detalles, many=True)
        return Response(serializer.data)

    @never_cache
    def retrieve(self, request, pk=None):
        detalle = OrdenServicioService.get_detalle_by_id(pk)
        if not detalle:
            return Response({'error': 'Detalle no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrdenServicioSerializer(detalle)
        return Response(serializer.data)

    @never_cache
    def create(self, request):
        data = request.data

        try:
            detalle = OrdenServicioService.create_detalle(
                orden_id=data.get('orden_id'),
                servicio_id=data.get('servicio_id'),
                cantidad=data.get('cantidad'),
                precio=data.get('precio'),
                observaciones=data.get('observaciones'),
            )
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = OrdenServicioSerializer(detalle)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @never_cache
    def update(self, request, pk=None):
        data = request.data

        try:
            detalle = OrdenServicioService.update_detalle(
                detalle_id=pk,
                cantidad=data.get('cantidad'),
                precio=data.get('precio'),
                observaciones=data.get('observaciones'),
            )
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = OrdenServicioSerializer(detalle)
        return Response(serializer.data)

    @never_cache
    def destroy(self, request, pk=None):
        try:
            OrdenServicioService.delete_detalle(detalle_id=pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
