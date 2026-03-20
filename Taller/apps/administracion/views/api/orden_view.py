from rest_framework import viewsets, status
from rest_framework.response import Response
from ...services.orden_service import OrdenService
from ...serializers.orden_serializers import OrdenSerializer
from django.views.decorators.cache import never_cache

class OrdenView(viewsets.ViewSet):

    @never_cache
    def list(self, request):
        ordenes = OrdenService.get_all_ordenes()
        serializer = OrdenSerializer(ordenes, many=True)
        return Response(serializer.data)

    @never_cache
    def retrieve(self, request, pk=None):
        orden = OrdenService.get_orden_by_id(pk)

        if not orden:
            return Response({'error': 'Orden no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrdenSerializer(orden)
        return Response(serializer.data)
    
    @never_cache
    def create(self, request):
        data = request.data
        estado_id = data.get('estado_id', data.get('estado'))

        try:
            orden = OrdenService.create_orden(
                recepcion_id=data['recepcion_id'],
                usuario_id=data['usuario_id'],
                diagnostico=data['diagnostico'],
                estado_id=estado_id,
            )

            serializer = OrdenSerializer(orden)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @never_cache
    def update(self, request, pk=None):
        data = request.data
        estado_id = data.get('estado_id', data.get('estado'))

        try:
            orden = OrdenService.update_orden(
                pk,
                recepcion_id=data.get('recepcion_id'),
                usuario_id=data.get('usuario_id'),
                diagnostico=data.get('diagnostico'),
                estado_id=estado_id,
            )

            serializer = OrdenSerializer(orden)
            return Response(serializer.data)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

        
    @never_cache
    def destroy(self, request, pk=None):
        try:
            OrdenService.delete_orden(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Error al eliminar: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)