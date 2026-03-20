from rest_framework import viewsets, status
from rest_framework.response import Response
from ...services.combustible_service import CombustibleService
from ...serializers.combustible_serializers import CombustibleSerializer
from django.views.decorators.cache import never_cache

class CombustibleView(viewsets.ViewSet):

    @never_cache
    def list(self, request):
        combustibles = CombustibleService.get_all_combustibles()
        serializer = CombustibleSerializer(combustibles, many=True)
        return Response(serializer.data)
    
    @never_cache
    def retrieve(self, request, pk=None):
        combustible = CombustibleService.get_combustible_by_id(pk)

        if not combustible:
            return Response({'error': 'Tipo de combustible no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CombustibleSerializer(combustible)
        return Response(serializer.data)
    
    @never_cache
    def create(self, request):
        data = request.data

        try:
            combustible = CombustibleService.create_combustible(
                nombre=data['nombre']
            )

            serializer = CombustibleSerializer(combustible)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @never_cache
    def update(self, request, pk=None):
        data = request.data

        try:
            combustible = CombustibleService.update_combustible(
                pk,
                nombre=data.get('nombre')
            )

            serializer = CombustibleSerializer(combustible)
            return Response(serializer.data)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        
    @never_cache
    def destroy(self, request, pk=None):
        try:
            combustible_nombre = CombustibleService.delete_combustible(pk)
            return Response({'message': f'Tipo de combustible "{combustible_nombre}" eliminado exitosamente.'})

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)