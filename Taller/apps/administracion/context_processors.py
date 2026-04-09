from .services.access_control_service import AccessControlService


def user_access_permissions(request):
    user = getattr(request, 'user', None)
    permissions = AccessControlService.get_effective_permissions(user)

    return {
        'acceso': permissions,
    }
