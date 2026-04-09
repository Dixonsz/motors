from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from ...services.rol_service import RolService
from ...services.access_control_service import AccessControlService


def _read_permissions_from_post(request, prefix='perm_'):
    permissions = {}
    for item in AccessControlService.PERMISSION_OPTIONS:
        key = item['key']
        permissions[key] = request.POST.get(f'{prefix}{key}') == 'on'
    return permissions


def rol_lista(request):
    roles = RolService.get_all_roles()
    paginator = Paginator(roles, 10)
    page_number = request.GET.get('page')
    roles = paginator.get_page(page_number)

    return render(request, 'roles/roles_lista.html', {'roles': roles})

def rol_create(request):
    permission_options = AccessControlService.PERMISSION_OPTIONS

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        permissions = _read_permissions_from_post(request)

        try:
            RolService.create_rol(nombre, descripcion, permissions=permissions)
            messages.success(request, 'Rol creado correctamente.')
            return redirect('roles_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'roles/roles_crear.html', {'permission_options': permission_options})

def rol_editar(request, rol_id):
    rol = RolService.get_rol_by_id(rol_id)
    permission_options = AccessControlService.PERMISSION_OPTIONS
    selected_permissions = AccessControlService.get_role_permissions(rol)
    selected_permission_keys = [key for key, value in selected_permissions.items() if value]

    if not rol:
        messages.error(request, 'El rol no existe.')
        return redirect('roles_lista')

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        permissions = _read_permissions_from_post(request)

        try:
            RolService.update_rol(rol_id, nombre, descripcion, permissions=permissions)
            messages.success(request, 'Rol actualizado correctamente.')
            return redirect('roles_lista')
        except ValueError as exc:
            messages.error(request, str(exc))
            selected_permissions = permissions
            selected_permission_keys = [key for key, value in selected_permissions.items() if value]

    return render(
        request,
        'roles/roles_editar.html',
        {
            'rol': rol,
            'permission_options': permission_options,
            'selected_permissions': selected_permissions,
            'selected_permission_keys': selected_permission_keys,
        },
    )

def rol_eliminar(request, rol_id):
    rol = RolService.get_rol_by_id(rol_id)
    if not rol:
        messages.error(request, 'El rol no existe.')
        return redirect('roles_lista')

    if request.method == 'POST':
        try:
            RolService.delete_rol(rol_id)
            messages.success(request, 'Rol eliminado correctamente.')
            return redirect('roles_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'roles/roles_eliminar.html', {'rol_id': rol_id})
