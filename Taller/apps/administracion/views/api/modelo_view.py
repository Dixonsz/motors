from rest_framework import viewsets,status
from rest_framework.response import Response
from ...services.modelo_service import ModeloService
from ...serializers.modelo_serializers import ModeloSerializer
from django.views.decorators.cache import never_cache

class ModeloView(viewsets.ViewSet):

    @never_cache
    def list(self, request):
        modelos = ModeloService.get_all_modelos()
        serializers = ModeloSerializer(modelos, many=True)
        return Response(serializers.data)
    

    @never_cache
    def retrieve(self, request, pk=None):
        modelo = ModeloService.get_modelo_by_id(pk)

        if not modelo:
            return Response({'error':  'Modelo no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ModeloSerializer(modelo)
        return Response(serializer.data)
    
    @never_cache
    def create(self, request):
        data = request.data

        try:
            modelo = ModeloService.create_modelo(
                nombre=data['nombre']
            )
            serializer = ModeloSerializer(modelo)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @never_cache
    def update(self, request, pk=None):
        data = request.data

        try:
            modelo = ModeloService.update_modelo(
                pk,
                nombre = data.get('nombre')
            )
            serializer = ModeloSerializer(modelo)
            return Response(serializer.data)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        
    @never_cache
    def destroy(self, request, pk=None):
        try:
            modelo_nombre = ModeloService.delete_modelo(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Error al eliminar:{str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)