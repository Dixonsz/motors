from rest_framework import viewsets, status
from rest_framework.response import Response
from ...services.recepcion_service import RecepcionService
from ...serializers.recepcion_serializers import RecepcionSerializer
from django.views.decorators.cache import never_cache

class RecepcionView(viewsets.ViewSet):

    @never_cache
    def list(self, request):
        recepcion = RecepcionService.get_all_recepciones()
        serializer = RecepcionSerializer(recepcion, many=True)
        return Response(serializer.data)

    @never_cache
    def retrieve(self, request, pk=None):
        recepcion = RecepcionService.get_recepcion_by_id(pk)

        if not recepcion:
            return Response({'error': 'Recepcion no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        serializer = RecepcionSerializer(recepcion)
        return Response(serializer.data)
    
    @never_cache
    def create(self, request):
        data = request.data

        try:
            recepcion = RecepcionService.create_recepcion(
                vehiculo_id=data['vehiculo_id'],
                usuario_id=data['usuario_id'],
                fecha_ingreso=data['fecha_ingreso'],
                observaciones=data['observaciones'],
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
    def update(self, request, pk=None):
        data = request.data

        try:
            recepcion = RecepcionService.update_recepcion(
                pk,
                vehiculo_id=data.get('vehiculo_id'),
                usuario_id=data.get('usuario_id'),
                fecha_ingreso=data.get('fecha_ingreso'),
                observaciones=data.get('observaciones'),
                kilometraje=data.get('kilometraje'),
                nivel_combustible=data.get('nivel_combustible')
            )

            serializer = RecepcionSerializer(recepcion)
            return Response(serializer.data)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        
    @never_cache
    def destroy(self, request, pk=None):
        try:
            RecepcionService.delete_recepcion(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)