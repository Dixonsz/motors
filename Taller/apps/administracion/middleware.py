from django.http import JsonResponse
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from .services.access_control_service import AccessControlService


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

    PATH_PERMISSIONS = (
        ('/roles/', 'acceso_roles'),
        ('/usuarios/', 'acceso_usuarios'),
        ('/reportes/', 'acceso_reportes'),
        ('/citas/', 'acceso_citas'),
        ('/recepciones/', 'acceso_recepciones'),
        ('/evidencias/', 'acceso_recepciones'),
        ('/ordenes/', 'acceso_ordenes'),
        ('/flujo/', 'acceso_flujo'),
        ('/clientes/', 'acceso_catalogo'),
        ('/vehiculos/', 'acceso_catalogo'),
        ('/servicios/', 'acceso_catalogo'),
        ('/categorias/', 'acceso_catalogo'),
        ('/marcas/', 'acceso_catalogo'),
        ('/modelos/', 'acceso_catalogo'),
        ('/combustibles/', 'acceso_catalogo'),
        ('/estados/', 'acceso_catalogo'),
        ('/agenda-horarios/', 'acceso_catalogo'),
        ('/categoria_herramientas/', 'acceso_inventario'),
        ('/estado_herramientas/', 'acceso_inventario'),
        ('/herramientas/', 'acceso_inventario'),
        ('/inventario_herramientas/', 'acceso_inventario'),
    )

    @staticmethod
    def _required_permission(path):
        if path == '/':
            return 'acceso_dashboard'

        for prefix, permission_key in LoginRequiredMiddleware.PATH_PERMISSIONS:
            if path.startswith(prefix):
                return permission_key

        return None

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        if path in self.EXEMPT_PATHS:
            return self.get_response(request)

        if any(path.startswith(prefix) for prefix in self.EXEMPT_PREFIXES):
            return self.get_response(request)

        if request.user.is_authenticated:
            required_permission = self._required_permission(path)
            if required_permission and not AccessControlService.has_permission(request.user, required_permission):
                if path.startswith('/api/'):
                    return JsonResponse({'detail': 'No tienes permisos para este recurso.'}, status=403)
                return HttpResponseForbidden('No tienes permisos para acceder a esta ruta.')

            return self.get_response(request)

        if path.startswith('/api/'):
            return JsonResponse(
                {'detail': 'Authentication credentials were not provided.'},
                status=401,
            )

        return redirect(f"/login/?next={path}")
