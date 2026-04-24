from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from .models.rol_permiso import RolPermiso


class Security:
    modulo_requerido = None
    accion_requerida = None

    def dispatch(self, request, *args, **kwargs):
        
        if not settings.SEGURIDAD_ACTIVA:
            return super().dispatch(request, *args, **kwargs)

        if not request.user.is_authenticated:
            return redirect('login')

        permisos_activos = RolPermiso.objects.filter(
            rol=request.user.rol,
            permiso__modulo__nombre__iexact=self.modulo_requerido,
            permiso__accion=self.accion_requerida
        ).exists()

        if not permisos_activos:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)