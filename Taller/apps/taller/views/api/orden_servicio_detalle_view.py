from rest_framework import status
from rest_framework.response import Response
from django.views.decorators.cache import never_cache
from ...services.orden_servicio_detalle_service import OrdenServicioDetalleService
from ...serializers.orden_servicio_detalle_serializers import OrdenServicioDetalleSerializer


class OrdenServicioDetalleView():

    @never_cache
    def list_by_orden(self, request, orden_id=None):
        detalles = OrdenServicioDetalleService.get_detalles_by_orden(orden_id)
        serializer = OrdenServicioDetalleSerializer(detalles, many=True)
        return Response(serializer.data)

    @never_cache
    def retrieve(self, request, pk=None):
        detalle = OrdenServicioDetalleService.get_detalle_by_id(pk)
        if not detalle:
            return Response({'error': 'Detalle no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrdenServicioDetalleSerializer(detalle)
        return Response(serializer.data)

    @never_cache
    def create(self, request):
        data = request.data
        try:
            detalle = OrdenServicioDetalleService.create_detalle(
                orden_id=data['orden_id'],
                servicio_id=data['servicio_id'],
                precio=data['precio'],
                cantidad=data.get('cantidad', 1),
                observaciones=data.get('observaciones')
            )
            serializer = OrdenServicioDetalleSerializer(detalle)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as e:
            return Response({'error': f'Campo requerido faltante: {e.args[0]}'}, status=status.HTTP_400_BAD_REQUEST)

    @never_cache
    def update(self, request, pk=None):
        data = request.data
        try:
            detalle = OrdenServicioDetalleService.update_detalle(
                pk,
                precio=data.get('precio'),
                cantidad=data.get('cantidad'),
                observaciones=data.get('observaciones')
            )
            serializer = OrdenServicioDetalleSerializer(detalle)
            return Response(serializer.data)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @never_cache
    def destroy(self, request, pk=None):
        try:
            OrdenServicioDetalleService.delete_detalle(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
