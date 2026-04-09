from django.http import JsonResponse
from django.shortcuts import redirect


class LoginRequiredMiddleware:
    """Bloquea rutas no autenticadas en web y API, dejando público solo login."""

    EXEMPT_PATHS = (
        '/login/',
        '/api/auth/login/',
    )

    EXEMPT_PREFIXES = (
        '/admin/',
        '/static/',
        '/media/',
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        if path in self.EXEMPT_PATHS:
            return self.get_response(request)

        if any(path.startswith(prefix) for prefix in self.EXEMPT_PREFIXES):
            return self.get_response(request)

        if request.user.is_authenticated:
            return self.get_response(request)

        if path.startswith('/api/'):
            return JsonResponse(
                {'detail': 'Authentication credentials were not provided.'},
                status=401,
            )

        return redirect(f"/login/?next={path}")
