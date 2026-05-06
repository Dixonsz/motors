from django.contrib.auth import authenticate, login
from django.views.decorators.cache import never_cache
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ...serializers.usuario_serializers import UsuarioSerializer


@api_view(['POST'])
@never_cache
def login_api(request):
    data = request.data
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return Response(
            {'success': False, 'message': 'Username y password son requeridos.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(request, username=username, password=password)

    if user is None:
        return Response(
            {'success': False, 'message': 'Usuario o contraseña incorrectos'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    if not user.is_active:
        return Response(
            {'success': False, 'message': 'La cuenta de usuario está deshabilitada'},
            status=status.HTTP_403_FORBIDDEN
        )

    login(request, user)
    serializer = UsuarioSerializer(user)

    return Response(
        {
            'success': True,
            'message': 'Inicio de sesión exitoso',
            'user': serializer.data
        },
        status=status.HTTP_200_OK
    )
