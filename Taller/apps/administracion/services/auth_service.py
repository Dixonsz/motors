from django.contrib.auth import authenticate

class AuthService:
    
    @staticmethod
    def login(username, password):
        if not username or not password:
            raise ValueError("Debes ingresar usuario y contraseña.")

        usuario = authenticate(username=username, password=password)
        if not usuario:
            raise ValueError("Credenciales inválidas.")

        if not usuario.is_active:
            raise ValueError("Tu usuario está inactivo. Contacta al administrador.")

        return usuario