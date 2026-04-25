from rest_framework import  status
from rest_framework.response import Response
from ...services.permiso_service import PermisoService
from ...serializers.permiso_serializers import PermisoSerializer
from django.views.decorators.cache import never_cache 

class PermisoView():

    @never_cache
    def list(self, request):
        permisos = PermisoService.get_all_permisos()
        serializer = PermisoSerializer(permisos, many=True)
        return Response(serializer.data)
    
    @never_cache
    def retrieve(self, request, pk=None):
        permiso = PermisoService.get_permiso_by_id(pk)

        if not permiso:
            return Response({'error': 'Permiso no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PermisoSerializer(permiso)
        return Response(serializer.data)
    
    @never_cache
    def retrieve_by_modulo(self, request, modulo_id=None):
        permisos = PermisoService.get_permisos_by_modulo(modulo_id)

        if not permisos:
            return Response({'error': 'No se encontraron permisos para el módulo'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PermisoSerializer(permisos, many=True)
        return Response(serializer.data)
    
    @never_cache
    def create(self, request):
        data = request.data

        try:
            permiso = PermisoService.create_permiso(
                modulo_id=data['modulo_id'],
                accion=data['accion']
            )

            serializer = PermisoSerializer(permiso)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @never_cache
    def destroy(self, request, pk=None):
        try:
            PermisoService.delete_permiso(pk)
            return Response({'message': f'Permiso eliminado exitosamente.'}, status=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)