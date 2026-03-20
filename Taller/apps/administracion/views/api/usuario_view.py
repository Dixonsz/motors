from rest_framework import viewsets, status
from rest_framework.response import Response
from ...services.usuario_service import UsuarioService
from ...serializers.usuario_serializers import UsuarioSerializer
from django.views.decorators.cache import never_cache

class UsuarioView(viewsets.ViewSet):

    @never_cache
    def list(self, request):
        usuarios = UsuarioService.get_all_usuarios()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)

    @never_cache
    def retrieve(self, request, pk=None):
        usuario = UsuarioService.get_usuario_by_id(pk)

        if not usuario:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data)
    
    @never_cache
    def create(self, request):
        data = request.data

        try:
            usuario = UsuarioService.create_usuario(
                nombre=data['nombre'],
                apellido=data['apellido'],
                telefono=data['telefono'],
                correo=data['correo'],
                rol_id=data['rol_id'],
                password=data['password']
            )

            serializer = UsuarioSerializer(usuario)
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
                nombre=data.get('nombre'),
                apellido=data.get('apellido'),
                telefono=data.get('telefono'),
                correo=data.get('correo'),
                rol_id=data.get('rol_id'),
                password=data.get('password')
            )

            serializer = UsuarioSerializer(usuario)
            return Response(serializer.data)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        
    @never_cache
    def destroy(self, request, pk=None):
        try:
            UsuarioService.delete_usuario(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)