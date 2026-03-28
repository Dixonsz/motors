from rest_framework import viewsets, status
from rest_framework.response import Response
from ...services.auth_service import AuthService
from ...serializers.usuario_serializers import UsuarioSerializer
from django.views.decorators.cache import never_cache


class AuthView(viewsets.ViewSet):


    @never_cache
    def login(self, request):
        data = request.data

        try:
            usuario = AuthService.login(
                username=data['username'],
                password=data['password']
            )

            request.session['usuario_id'] = usuario.id
            serializer = UsuarioSerializer(usuario)

            return Response({
                'success': True,
                'usuario': serializer.data
            })

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as e:
            return Response({'error': f'Campo requerido faltante: {e.args[0]}'}, status=status.HTTP_400_BAD_REQUEST)
