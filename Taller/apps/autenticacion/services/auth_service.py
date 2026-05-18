from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model          
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()                                


class AuthService:

    @staticmethod
    def login(request, username: str, password: str) -> dict:
        user = authenticate(request, username=username, password=password)

        if user is None:
            return {
                'success': False,
                'user': None,
                'message': 'Usuario o contraseña incorrectos'
            }
        if not user.is_active:
            return {
                'success': False,
                'user': None,
                'message': 'La cuenta de usuario está deshabilitada'
            }
        login(request, user)
        return {
            'success': True,
            'user': user,
            'message': 'Inicio de sesión exitoso'
        }

    @staticmethod
    def logout_user(request):
        logout(request)

    @staticmethod
    def reset_password(request, email: str) -> dict:
        try:
            user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist:

            return {
                'success': True,
                'message': 'Se enviar[a] un enlace para restablecer tu contraseña.'
            }

        token = default_token_generator.make_token(user)   
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        domain = request.get_host()
        protocol = 'https' if request.is_secure() else 'http'
        reset_link = f"{protocol}://{domain}/autenticacion/reset-password/{uid}/{token}/"

        try:
            send_mail(
                subject='Restablecer contraseña',
                message=                                    
                    f'Hola {user.nombre} {user.apellido},\n'
                    f'Recibimos una solicitud para restablecer tu contraseña.\n\n'
                    f'Haz clic en el siguiente enlace (válido por 5 minutos):\n{reset_link}\n\n'
                    f'Si no solicitaste esto, ignora este mensaje.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )

        except Exception as e:

            return {
                'success': False,
                'message': f'Error al enviar el correo: {str(e)}'
            }

        return {
            'success': True,
            'message': 'Si el correo existe, recibirás un enlace para restablecer tu contraseña.'
        }

    @staticmethod
    def confirm_reset_password(uidb64: str, token: str, new_password: str) -> dict:
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return {
                'success': False,
                'message': 'Enlace de restablecimiento de contraseña no válido'
            }

        if not default_token_generator.check_token(user, token):
            return {
                'success': False,
                'message': 'Enlace de restablecimiento de contraseña no válido o ha expirado'
            }


        user.set_password(new_password)
        user.save()
        return {
            'success': True,
            'message': 'Contraseña restablecida exitosamente'
        }
