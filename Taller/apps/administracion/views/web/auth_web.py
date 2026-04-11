from django.contrib import messages
from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils.http import url_has_allowed_host_and_scheme
from django.shortcuts import redirect, render
from ...services.auth_service import AuthService


def _resolve_next_url(request):
    next_url = request.POST.get('next') or request.GET.get('next') or ''
    if not next_url:
        return ''

    if not url_has_allowed_host_and_scheme(
        url=next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return ''

    # Evita ciclos de redireccion al login/logout.
    if next_url.startswith('/login') or next_url.startswith('/logout'):
        return ''

    return next_url


def login(request):
    next_url = _resolve_next_url(request)
    credenciales = getattr(settings, 'DEFAULT_LOGIN_CREDENTIALS', {})

    username_value = credenciales.get('username', '')
    if request.method == 'POST':
        username_value = (request.POST.get('username') or '').strip()

    context = {
        'default_username': username_value,
        'default_password': credenciales.get('password', '') if request.method != 'POST' else '',
        'next_url': next_url,
    }

    if request.method == 'POST':
        username = username_value
        password = request.POST.get('password')

        try:
            usuario = AuthService.login(username, password)
            django_login(request, usuario)
            request.session['usuario_id'] = usuario.id
            messages.success(request, 'Inicio de sesión exitoso.')
            return redirect(next_url or 'clientes_lista')
        except ValueError as e:
            messages.error(request, str(e))

    return render(request, 'auth/login.html', context)


@login_required(login_url='login')
def logout(request):
    django_logout(request)
    messages.success(request, 'Sesión cerrada correctamente.')
    return redirect('login')
    