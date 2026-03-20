from rest_framework import viewsets, status
from rest_framework.response import Response
from ...services.rol_service import RolService
from ...serializers.rol_serializers import RolSerializer
from django.views.decorators.cache import never_cache


class RolView(viewsets.ViewSet):

    @never_cache
    def list(self, request):
        roles = RolService.get_all_roles()
        serializer = RolSerializer(roles, many=True)
        return Response(serializer.data)

    @never_cache
    def retrieve(self, request, pk=None):
        rol = RolService.get_rol_by_id(pk)

        if not rol:
            return Response({'error': 'Rol no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        serializer = RolSerializer(rol)
        return Response(serializer.data)

    @never_cache
    def create(self, request):
        data = request.data

        try:
            rol = RolService.create_rol(
                nombre=data['nombre'],
                descripcion=data['descripcion']
            )

            serializer = RolSerializer(rol)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @never_cache
    def update(self, request, pk=None):
        data = request.data

        try:
            rol = RolService.update_rol(
                pk,
                nombre=data.get('nombre'),
                descripcion=data.get('descripcion')
            )

            serializer = RolSerializer(rol)
            return Response(serializer.data)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

    @never_cache
    def destroy(self, request, pk=None):
        try:
            rol_nombre = RolService.delete_rol(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Error al eliminar: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)