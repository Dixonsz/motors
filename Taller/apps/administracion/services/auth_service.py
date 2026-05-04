from django.contrib.auth import authenticate

class AuthService:

    @staticmethod
    def login(username: str, password: str) -> dict:
        user = authenticate(username=username, password=password)

        if user is None:
                    return {
                        'success': False,
                        'user': None,
                        'message': 'Invalid username or password'
                    }
        if not user.is_active:
            return {
                'success': False,
                'user': None,
                'message': 'User account is disabled'
            }
        if user is not None:
            return {
                'success': True,
                'message': 'Login successful',
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
            }
            
    @staticmethod
    def request_password_reset(email: str) -> dict:
        user = authenticate(email=email)
        
       
        if user is None:
            return {
                'success': False,
                'message': 'Se enviara un correo de restablecimiento de contraseña'
            }
        if not user.is_active:
            return {
                'success': False,
                'message': 'User account is disabled'
            }
        if user is not None:
            return {
                'success': True,
                'message': 'Password reset email sent successfully'
            }
        
        
      
      

        