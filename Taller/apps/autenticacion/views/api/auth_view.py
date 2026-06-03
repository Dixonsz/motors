from django.contrib.auth import authenticate, login
from django.views.decorators.cache import never_cache
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ...services.auth_service import AuthService

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


@api_view(['POST'])
def reset_password_api(request):
    email = request.data.get('email')
    if not email:
        return Response(
            {'success': False, 'message': 'El campo email es requerido.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    result = AuthService.reset_password(request, email)
    if result['success']:
        return Response({'success': True, 'message': result['message']}, status=status.HTTP_200_OK)
    else:
        return Response({'success': False, 'message': result['message']}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
def confirm_reset_password_api(request):
    uidb64 = request.data.get('uid')
    token = request.data.get('token')
    new_password = request.data.get('new_password')
    confirm_password = request.data.get('confirm_password')

    if not all([uidb64, token, new_password, confirm_password]):
        return Response(
            {'success': False, 'message': 'Todos los campos son requeridos.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if new_password != confirm_password:
        return Response(
            {'success': False, 'message': 'Las contraseñas no coinciden.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    result = AuthService.confirm_reset_password(uidb64, token, new_password)
    http_status = status.HTTP_200_OK if result['success'] else status.HTTP_400_BAD_REQUEST
    return Response({'success': result['success'], 'message': result['message']}, status=http_status)
