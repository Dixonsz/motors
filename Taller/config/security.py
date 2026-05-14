from functools import wraps

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

from apps.autenticacion.models import RolPermiso


def _is_security_active():
    if hasattr(settings, "SEGURIDAD_ACTIVA"):
        return settings.SEGURIDAD_ACTIVA
    if hasattr(settings, "DISABLE_ACCESS_SECURITY"):
        return not settings.DISABLE_ACCESS_SECURITY
    return True


def _user_has_permission(user, modulo, accion):
    if user.is_superuser:
        return True
    if not modulo or not accion:
        return True
    if not getattr(user, "rol_id", None):
        return False
    return RolPermiso.objects.filter(
        rol_id=user.rol_id,
        permiso__modulo__nombre__iexact=modulo,
        permiso__accion=accion,
    ).exists()


def access_required(modulo=None, accion=None):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not _is_security_active():
                return view_func(request, *args, **kwargs)

            if not request.user.is_authenticated:
                return redirect('login')

            if not _user_has_permission(request.user, modulo, accion):
                raise PermissionDenied

            return view_func(request, *args, **kwargs)

        return _wrapped

    return decorator


class Security:
    modulo_requerido = None
    accion_requerida = None

    def dispatch(self, request, *args, **kwargs):
        
        if not _is_security_active():
            return super().dispatch(request, *args, **kwargs)

        if not request.user.is_authenticated:
            return redirect('login')

        if not _user_has_permission(
            request.user,
            self.modulo_requerido,
            self.accion_requerida,
        ):
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)