from rest_framework import status
from rest_framework.response import Response
from django.views.decorators.cache import never_cache
from ...services.orden_servicio_service import OrdenServicioService
from ...serializers.orden_servicio_serializers import OrdenServicioSerializer
from ...serializers.orden_servicio_and_detalle_serializers import OrdenServicioAndDetallesSerializer


class OrdenServicioView():

    @never_cache
    def list(self, request):
        ordenes = OrdenServicioService.get_all_ordenes_servicio()
        serializer = OrdenServicioSerializer(ordenes, many=True)
        return Response(serializer.data)

    @never_cache
    def retrieve(self, request, pk=None):
        orden = OrdenServicioService.get_orden_servicio_by_id(pk)
        if not orden:
            return Response({'error': 'Orden de servicio no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrdenServicioAndDetallesSerializer(orden)
        return Response(serializer.data)

    @never_cache
    def create(self, request):
        data = request.data
        try:
            orden = OrdenServicioService.create_orden_servicio(
                recepcion_id=data['recepcion_id'],
                usuario_id=data['usuario_id'],
                estado_id=data['estado_id'],
                diagnostico=data.get('diagnostico'),
                observaciones=data.get('observaciones')
            )
            serializer = OrdenServicioSerializer(orden)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as e:
            return Response({'error': f'Campo requerido faltante: {e.args[0]}'}, status=status.HTTP_400_BAD_REQUEST)

    @never_cache
    def update(self, request, pk=None):
        data = request.data
        try:
            orden = OrdenServicioService.update_orden_servicio(
                pk,
                recepcion_id=data.get('recepcion_id'),
                usuario_id=data.get('usuario_id'),
                estado_id=data.get('estado_id'),
                diagnostico=data.get('diagnostico'),
                observaciones=data.get('observaciones')
            )
            serializer = OrdenServicioSerializer(orden)
            return Response(serializer.data)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @never_cache
    def cerrar(self, request, pk=None):
        try:
            orden = OrdenServicioService.cerrar_orden_servicio(pk)
            serializer = OrdenServicioSerializer(orden)
            return Response(serializer.data)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @never_cache
    def destroy(self, request, pk=None):
        try:
            OrdenServicioService.delete_orden_servicio(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
