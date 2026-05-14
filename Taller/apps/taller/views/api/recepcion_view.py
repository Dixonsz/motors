from rest_framework import status
from rest_framework.response import Response
from django.views.decorators.cache import never_cache
from ...services.recepcion_service import RecepcionService
from ...serializers.recepcion_serializers import RecepcionSerializer


class RecepcionView():

    @never_cache
    def list(self, request):
        recepciones = RecepcionService.get_all_recepciones()
        serializer = RecepcionSerializer(recepciones, many=True)
        return Response(serializer.data)

    @never_cache
    def retrieve(self, request, pk=None):
        recepcion = RecepcionService.get_recepcion_by_id(pk)
        if not recepcion:
            return Response({'error': 'Recepción no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = RecepcionSerializer(recepcion)
        return Response(serializer.data)

    @never_cache
    def create(self, request):
        data = request.data
        try:
            recepcion = RecepcionService.create_recepcion(
                vehiculo_id=data['vehiculo_id'],
                usuario_id=data['usuario_id'],
                observaciones=data.get('observaciones', ''),
                kilometraje=data['kilometraje'],
                nivel_combustible=data['nivel_combustible']
            )
            serializer = RecepcionSerializer(recepcion)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as e:
            return Response({'error': f'Campo requerido faltante: {e.args[0]}'}, status=status.HTTP_400_BAD_REQUEST)

    @never_cache
    def destroy(self, request, pk=None):
        try:
            RecepcionService.delete_recepcion(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
