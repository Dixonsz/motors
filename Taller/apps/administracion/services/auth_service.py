from django.contrib.auth import authenticate, login, logout

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
    def logout_user( request):
          logout(request)
        
        
        
      
      

        