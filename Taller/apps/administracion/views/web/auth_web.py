from django.contrib import messages
from django.shortcuts import redirect, render
from ...services.auth_service import AuthService


def login(request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            try:
                usuario = AuthService.login(username, password)
                request.session['usuario_id'] = usuario.id
                messages.success(request, 'Inicio de sesión exitoso.')
                return redirect('clientes_lista')
            except ValueError as e:
                messages.error(request, str(e))
        return render(request, 'auth/login.html')
    