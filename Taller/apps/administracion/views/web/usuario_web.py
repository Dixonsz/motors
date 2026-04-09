from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from ...services.usuario_service import UsuarioService
from ...services.rol_service import RolService
from ...services.access_control_service import AccessControlService


def _read_extra_permissions(request):
    permissions = {}
    for item in AccessControlService.PERMISSION_OPTIONS:
        key = item['key']
        permissions[key] = request.POST.get(f'extra_perm_{key}') == 'on'
    return permissions

def usuario_lista(request):
    usuarios = UsuarioService.get_all_usuarios()
    paginator = Paginator(usuarios, 10)
    page_number = request.GET.get('page')
    usuarios = paginator.get_page(page_number)

    return render(request, 'usuarios/usuarios_lista.html', {'usuarios': usuarios})

def usuario_create(request):
    permission_options = AccessControlService.PERMISSION_OPTIONS
    selected_extra_permissions = {}

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        telefono = request.POST.get('telefono')
        correo = request.POST.get('correo')
        rol_id = request.POST.get('rol_id')
        password = request.POST.get('password')
        extra_permissions = _read_extra_permissions(request)
        selected_extra_permissions = extra_permissions

        try:
            UsuarioService.create_usuario(
                nombre,
                apellido,
                telefono,
                correo,
                rol_id,
                password,
                extra_permissions=extra_permissions,
            )
            messages.success(request, 'Usuario creado correctamente.')
            return redirect('usuarios_lista')
        except ValueError as exc:
            messages.error(request, str(exc))
    
    roles = RolService.get_all_roles()
    return render(
        request,
        'usuarios/usuarios_crear.html',
        {
            'roles': roles,
            'permission_options': permission_options,
            'selected_extra_permissions': selected_extra_permissions,
            'selected_extra_permission_keys': [key for key, value in selected_extra_permissions.items() if value],
        },
    )    


def usuario_editar(request, usuario_id):
    usuario = UsuarioService.get_usuario_by_id(usuario_id)
    roles = RolService.get_all_roles()
    permission_options = AccessControlService.PERMISSION_OPTIONS
    selected_extra_permissions = AccessControlService.normalize_permissions(getattr(usuario, 'extra_permissions', {})) if usuario else {}
    selected_extra_permission_keys = [key for key, value in selected_extra_permissions.items() if value]

    if not usuario:
        messages.error(request, 'El usuario no existe.')
        return redirect('usuarios_lista')

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        telefono = request.POST.get('telefono')
        correo = request.POST.get('correo')
        rol_id = request.POST.get('rol_id')
        password = request.POST.get('password')
        extra_permissions = _read_extra_permissions(request)

        try:
            UsuarioService.update_usuario(
                usuario_id,
                nombre,
                apellido,
                telefono,
                correo,
                rol_id,
                password,
                extra_permissions=extra_permissions,
            )
            messages.success(request, 'Usuario actualizado correctamente.')
            return redirect('usuarios_lista')
        except ValueError as exc:
            messages.error(request, str(exc))
            selected_extra_permissions = extra_permissions
            selected_extra_permission_keys = [key for key, value in selected_extra_permissions.items() if value]

    return render(
        request,
        'usuarios/usuarios_editar.html',
        {
            'usuario': usuario,
            'roles': roles,
            'permission_options': permission_options,
            'selected_extra_permissions': selected_extra_permissions,
            'selected_extra_permission_keys': selected_extra_permission_keys,
        },
    )

def usuario_eliminar(request, usuario_id):
    usuario = UsuarioService.get_usuario_by_id(usuario_id)
    if not usuario:
        messages.error(request, 'El usuario no existe.')
        return redirect('usuarios_lista')

    if request.method == 'POST':
        try:
            UsuarioService.delete_usuario(usuario_id)
            messages.success(request, 'Usuario eliminado correctamente.')
            return redirect('usuarios_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'usuarios/usuarios_eliminar.html', {'usuario_id': usuario_id})

