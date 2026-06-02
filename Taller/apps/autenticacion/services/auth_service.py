from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model          
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
import threading
import logging

logger = logging.getLogger(__name__)

User = get_user_model()                                


def send_email_async(subject, message, from_email, recipient_list):
    """Envía email en un thread separado para no bloquear la request"""
    logger.info(
        "Configuración de email — BACKEND: %s | HOST: %s | PORT: %s | "
        "USE_TLS: %s | HOST_USER: %s",
        getattr(settings, "EMAIL_BACKEND", "no configurado"),
        getattr(settings, "EMAIL_HOST", "no configurado"),
        getattr(settings, "EMAIL_PORT", "no configurado"),
        getattr(settings, "EMAIL_USE_TLS", "no configurado"),
        getattr(settings, "EMAIL_HOST_USER", "no configurado"),
    )
    logger.info(
        "Iniciando envío de email — asunto: %r | de: %s | para: %s",
        subject,
        from_email,
        recipient_list,
    )
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False,
        )
        logger.info(
            "Email enviado exitosamente — asunto: %r | para: %s",
            subject,
            recipient_list,
        )
    except Exception:
        logger.error(
            "Error enviando email — asunto: %r | de: %s | para: %s",
            subject,
            from_email,
            recipient_list,
            exc_info=True,
        )


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
                'message': 'Se enviará un enlace para restablecer tu contraseña.'
            }

        token = default_token_generator.make_token(user)   
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        domain = request.get_host()
        protocol = 'https' if request.is_secure() else 'http'
        reset_link = f"{protocol}://{domain}/autenticacion/reset-password/{uid}/{token}/"

        # Enviar email en un thread separado para no bloquear
        email_thread = threading.Thread(
            target=send_email_async,
            args=(
                'Restablecer contraseña',
                f'Hola {user.nombre} {user.apellido},\n'
                f'Recibimos una solicitud para restablecer tu contraseña.\n\n'
                f'Haz clic en el siguiente enlace (válido por 5 minutos):\n{reset_link}\n\n'
                f'Si no solicitaste esto, ignora este mensaje.',
                settings.DEFAULT_FROM_EMAIL,
                [email],
            )
        )
        email_thread.daemon = True
        email_thread.start()

        return {
            'success': True,
            'message': 'Si el correo existe, recibirás un enlace para restablecer tu contraseña.'
        }

    @staticmethod
    def confirm_reset_password(uidb64: str, token: str, new_password: str) -> dict:
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, User.DoesNotExist):
            return {
                'success': False,
                'message': 'El enlace de restablecimiento es inválido o ha expirado.'
            }

        if not default_token_generator.check_token(user, token):
            return {
                'success': False,
                'message': 'El enlace de restablecimiento es inválido o ha expirado.'
            }

        user.set_password(new_password)
        user.save()

        return {
            'success': True,
            'message': 'Tu contraseña ha sido restablecida exitosamente.'
        }

