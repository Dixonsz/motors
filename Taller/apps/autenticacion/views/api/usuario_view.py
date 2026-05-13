from rest_framework import status
from rest_framework.response import Response
from django.views.decorators.cache import never_cache
from ...services.usuario_service import UsuarioService
from ...serializers.usuario_serializers import UsuarioSerializer
from ...serializers.usuario_create_serializers import UsuarioCreateSerializer


class UsuarioView():

    @never_cache
    def list(self, request):
        usuarios = UsuarioService.get_all_usuarios()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)

    @never_cache
    def retrieve(self, request, pk=None):
        usuario = UsuarioService.get_usuario_by_id(pk)
        if not usuario:
            return Response({'error': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data)

    @never_cache
    def create(self, request):
        data = request.data
        try:
            usuario = UsuarioService.create_usuario(
                username=data['username'],
                email=data['email'],
                password=data['password'],
                nombre=data['nombre'],
                apellido=data['apellido'],
                cedula=data['cedula'],
                telefono=data['telefono'],
                direccion=data['direccion'],
                rol_id=data['rol_id'],
                especialidad=data.get('especialidad')
            )
            serializer = UsuarioCreateSerializer(usuario)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as e:
            return Response({'error': f'Campo requerido faltante: {e.args[0]}'}, status=status.HTTP_400_BAD_REQUEST)

    @never_cache
    def update(self, request, pk=None):
        data = request.data
        try:
            usuario = UsuarioService.update_usuario(
                pk,
                username=data.get('username'),
                email=data.get('email'),
                nombre=data.get('nombre'),
                apellido=data.get('apellido'),
                cedula=data.get('cedula'),
                telefono=data.get('telefono'),
                direccion=data.get('direccion'),
                especialidad=data.get('especialidad'),
                rol_id=data.get('rol_id')
            )
            serializer = UsuarioSerializer(usuario)
            return Response(serializer.data)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @never_cache
    def cambiar_password(self, request, pk=None):
        data = request.data
        try:
            UsuarioService.cambiar_password(
                pk,
                password_actual=data['password_actual'],
                password_nueva=data['password_nueva']
            )
            return Response({'message': 'Contraseña actualizada correctamente.'})
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as e:
            return Response({'error': f'Campo requerido faltante: {e.args[0]}'}, status=status.HTTP_400_BAD_REQUEST)

    @never_cache
    def activar_desactivar(self, request, pk=None):
        try:
            usuario = UsuarioService.activar_desactivar_usuario(pk)
            estado = 'activado' if usuario.estado else 'desactivado'
            return Response({'message': f'Usuario {estado} correctamente.'})
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @never_cache
    def destroy(self, request, pk=None):
        try:
            UsuarioService.delete_usuario(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)