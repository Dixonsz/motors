from functools import wraps

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import redirect

import os

from apps.autenticacion.models import RolPermiso


def _is_security_active():
    if hasattr(settings, "SECURITY_ACTIVE"):
        return settings.SECURITY_ACTIVE
    if hasattr(settings, "DISABLE_ACCESS_SECURITY"):
        return not settings.DISABLE_ACCESS_SECURITY
    return True


def _user_has_permission(user, modulo, accion):
    maint_users = [item.strip() for item in os.environ.get("MAINT_USER", "").split(",") if item.strip()]
    if user.is_superuser and user.username in maint_users:
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


def protected_error_to_message(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except ProtectedError:
            message = "No se puede eliminar el registro porque esta asociado a otros datos."
            messages.error(request, message)
            return redirect(request.META.get("HTTP_REFERER", "/"))

    return _wrapped


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