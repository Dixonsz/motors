from django.conf import settings

from .services.access_control_service import AccessControlService


def user_access_permissions(request):
    if getattr(settings, 'DISABLE_ACCESS_SECURITY', False):
        permissions = AccessControlService._all_permissions()
        return {
            'acceso': permissions,
        }

    user = getattr(request, 'user', None)
    permissions = AccessControlService.get_effective_permissions(user)

    return {
        'acceso': permissions,
    }
