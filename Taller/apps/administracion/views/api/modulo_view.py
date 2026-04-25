from rest_framework import  status
from rest_framework.response import Response
from ...services.modulo_service import ModuloService
from ...serializers.modulo_serializers import ModuloSerializer
from django.views.decorators.cache import never_cache 

class ModuloView():

    @never_cache
    def list(self, request):
        modulos = ModuloService.get_all_modulos()
        serializer = ModuloSerializer(modulos, many=True)
        return Response(serializer.data)
    
    @never_cache
    def retrieve(self, request, pk=None):
        modulo = ModuloService.get_modulo_by_id(pk)

        if not modulo:
            return Response({'error': 'Módulo no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ModuloSerializer(modulo)
        return Response(serializer.data)
    
    @never_cache
    def create(self, request):
        data = request.data

        try:
            modulo = ModuloService.create_modulo(
                nombre=data['nombre'],
                descripcion=data['descripcion']
            )

            serializer = ModuloSerializer(modulo)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @never_cache
    def update(self, request, pk=None):
        data = request.data

        try:
            modulo = ModuloService.update_modulo(
                pk,
                nombre=data.get('nombre'),
                descripcion=data.get('descripcion')
            )

            serializer = ModuloSerializer(modulo)
            return Response(serializer.data)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        
    @never_cache
    def destroy(self, request, pk=None):
        try:
            modulo_nombre = ModuloService.delete_modulo(pk)
            return Response({'message': f'Módulo "{modulo_nombre}" eliminado exitosamente.'})

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        


    