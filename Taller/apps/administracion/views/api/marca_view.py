from rest_framework import viewsets, status
from rest_framework.response import Response
from ...services.marca_service import MarcaService
from ...serializers.marca_serializers import MarcaSerializer
from django.views.decorators.cache import never_cache

class MarcaView(viewsets.ViewSet):

    @never_cache
    def list(self, request):
        marcas = MarcaService.get_all_marcas()
        serializer = MarcaSerializer(marcas, many=True)
        return Response(serializer.data)
    
    @never_cache
    def retrieve(self, request, pk=None):
        marca = MarcaService.get_marca_by_id(pk)

        if not marca:
            return Response({'error': 'Marca no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        serializer = MarcaSerializer(marca)
        return Response(serializer.data)
    
    @never_cache
    def create(self, request):
        data = request.data

        try:
            marca = MarcaService.create_marca(
                nombre=data['nombre']
            )

            serializer = MarcaSerializer(marca)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @never_cache
    def update(self, request, pk=None):
        data = request.data

        try:
            marca = MarcaService.update_marca(
                pk,
                nombre=data.get('nombre')
            )

            serializer = MarcaSerializer(marca)
            return Response(serializer.data)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        
    @never_cache
    def destroy(self, request, pk=None):
        try:
            marca_nombre = MarcaService.delete_marca(pk)
            return Response({'message': f'Marca "{marca_nombre}" eliminada exitosamente.'})

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        
