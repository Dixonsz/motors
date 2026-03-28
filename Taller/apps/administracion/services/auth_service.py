from ..models.usuario import Usuario
from django.contrib.auth.hashers import check_password

class AuthService:
    
    @staticmethod
    def login(username, password):
        try:
            usuario = Usuario.objects.get(username=username)

            if not check_password(password, usuario.password):
                raise ValueError("Contraseña incorrecta.")
            return usuario
        except Usuario.DoesNotExist:
            raise ValueError("El nombre de usuario no existe.")