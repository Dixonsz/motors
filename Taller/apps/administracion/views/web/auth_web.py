from django.contrib import messages
from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import redirect, render
from ...services.auth_service import AuthService


def login(request):
    if request.user.is_authenticated:
        return redirect('inicio')

    credenciales = getattr(settings, 'DEFAULT_LOGIN_CREDENTIALS', {})
    context = {
        'default_username': credenciales.get('username', ''),
        'default_password': credenciales.get('password', ''),
        'next_url': request.POST.get('next') or request.GET.get('next') or '',
    }

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            usuario = AuthService.login(username, password)
            django_login(request, usuario)
            request.session['usuario_id'] = usuario.id
            messages.success(request, 'Inicio de sesión exitoso.')
            next_url = request.POST.get('next') or request.GET.get('next')
            return redirect(next_url or 'inicio')
        except ValueError as e:
            messages.error(request, str(e))

    return render(request, 'auth/login.html', context)


@login_required(login_url='login')
def logout(request):
    django_logout(request)
    messages.success(request, 'Sesión cerrada correctamente.')
    return redirect('login')
    