from rest_framework import status
from rest_framework.response import Response
from django.views.decorators.cache import never_cache
from ...services.rol_permiso_service import RolPermisoService
from ...serializers.rol_permiso_serializers import RolPermisoSerializer


class RolPermisoView():

    @never_cache
    def list(self, request, rol_id=None):
        try:
            permisos = RolPermisoService.get_permisos_by_rol(rol_id)
            serializer = RolPermisoSerializer(permisos, many=True)
            return Response(serializer.data)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @never_cache
    def asignar_permiso(self, request):
        data = request.data
        try:
            rol_permiso = RolPermisoService.asignar_permiso(
                rol_id=data['rol_id'],
                permiso_id=data['permiso_id']
            )
            serializer = RolPermisoSerializer(rol_permiso)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as e:
            return Response({'error': f'Campo requerido faltante: {e.args[0]}'}, status=status.HTTP_400_BAD_REQUEST)

    @never_cache
    def asignar_modulo_completo(self, request):
        data = request.data
        try:
            RolPermisoService.asignar_permisos_modulo_completo(
                rol_id=data['rol_id'],
                modulo_id=data['modulo_id']
            )
            return Response({'mensaje': 'Permisos del módulo asignados correctamente.'}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as e:
            return Response({'error': f'Campo requerido faltante: {e.args[0]}'}, status=status.HTTP_400_BAD_REQUEST)

    @never_cache
    def revocar_permiso(self, request):
        data = request.data
        try:
            RolPermisoService.revocar_permiso(
                rol_id=data['rol_id'],
                permiso_id=data['permiso_id']
            )
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as e:
            return Response({'error': f'Campo requerido faltante: {e.args[0]}'}, status=status.HTTP_400_BAD_REQUEST)

    @never_cache
    def revocar_modulo_completo(self, request):
        data = request.data
        try:
            RolPermisoService.revocar_permisos_modulo_completo(
                rol_id=data['rol_id'],
                modulo_id=data['modulo_id']
            )
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as e:
            return Response({'error': f'Campo requerido faltante: {e.args[0]}'}, status=status.HTTP_400_BAD_REQUEST)
