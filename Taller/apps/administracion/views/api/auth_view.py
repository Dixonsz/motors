from rest_framework import viewsets, status
from django.contrib.auth import login as django_login
from django.urls import reverse
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from ...services.auth_service import AuthService
from ...serializers.usuario_serializers import UsuarioSerializer
from django.views.decorators.cache import never_cache
from django.utils.http import url_has_allowed_host_and_scheme


class AuthView(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @staticmethod
    def _resolve_next_url(request):
        next_url = request.data.get('next') or request.query_params.get('next') or ''
        if not next_url:
            return reverse('clientes_lista')

        if not url_has_allowed_host_and_scheme(
            url=next_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        ):
            return reverse('clientes_lista')

        if next_url.startswith('/login') or next_url.startswith('/logout'):
            return reverse('clientes_lista')

        return next_url


    @never_cache
    def login(self, request):
        data = request.data
        redirect_url = self._resolve_next_url(request)

        try:
            usuario = AuthService.login(
                username=data['username'],
                password=data['password']
            )

            django_login(request, usuario)
            request.session['usuario_id'] = usuario.id
            serializer = UsuarioSerializer(usuario)

            return Response({
                'success': True,
                'usuario': serializer.data,
                'redirect_url': redirect_url,
            })

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as e:
            return Response({'error': f'Campo requerido faltante: {e.args[0]}'}, status=status.HTTP_400_BAD_REQUEST)
