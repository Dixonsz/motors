from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from ...services.rol_permiso_service import RolPermisoService
from ...services.permiso_service import PermisoService
from ...services.rol_service import RolService


def rol_permiso_lista(request, rol_id):
    rol = RolService.get_rol_by_id(rol_id)
    if not rol:
        messages.error(request, 'El rol no existe.')
        return redirect('roles_lista')

    permisos = RolPermisoService.get_permisos_by_rol(rol_id)
    paginator = Paginator(permisos, 10)
    page_number = request.GET.get('page')
    permisos = paginator.get_page(page_number)

    return render(request, 'rol_permisos/rol_permiso_lista.html', {
        'rol': rol,
        'permisos': permisos
    })


def rol_permiso_asignar(request, rol_id):
    rol = RolService.get_rol_by_id(rol_id)
    if not rol:
        messages.error(request, 'El rol no existe.')
        return redirect('roles_lista')

    if request.method == 'POST':
        permiso_id = request.POST.get('permiso_id')
        try:
            RolPermisoService.asignar_permiso(rol_id, permiso_id)
            messages.success(request, 'Permiso asignado correctamente.')
            return redirect('rol_permiso_lista', rol_id=rol_id)
        except ValueError as exc:
            messages.error(request, str(exc))

    # Permisos disponibles — los que el rol aún no tiene
    permisos_asignados = RolPermisoService.get_permisos_by_rol(rol_id).values_list('permiso_id', flat=True)
    permisos_disponibles = PermisoService.get_all_permisos().exclude(id__in=permisos_asignados)

    return render(request, 'rol_permisos/rol_permiso_asignar.html', {
        'rol': rol,
        'permisos_disponibles': permisos_disponibles
    })


def rol_permiso_asignar_modulo(request, rol_id):
    rol = RolService.get_rol_by_id(rol_id)
    if not rol:
        messages.error(request, 'El rol no existe.')
        return redirect('roles_lista')

    if request.method == 'POST':
        modulo_id = request.POST.get('modulo_id')
        try:
            RolPermisoService.asignar_permisos_modulo_completo(rol_id, modulo_id)
            messages.success(request, 'Permisos del módulo asignados correctamente.')
            return redirect('rol_permiso_lista', rol_id=rol_id)
        except ValueError as exc:
            messages.error(request, str(exc))

    from ...services.modulo_service import ModuloService
    modulos = ModuloService.get_all_modulos()

    return render(request, 'rol_permisos/rol_permiso_asignar_modulo.html', {
        'rol': rol,
        'modulos': modulos
    })


def rol_permiso_revocar(request, rol_id, permiso_id):
    rol = RolService.get_rol_by_id(rol_id)
    if not rol:
        messages.error(request, 'El rol no existe.')
        return redirect('roles_lista')

    if request.method == 'POST':
        try:
            RolPermisoService.revocar_permiso(rol_id, permiso_id)
            messages.success(request, 'Permiso revocado correctamente.')
            return redirect('rol_permiso_lista', rol_id=rol_id)
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'rol_permisos/rol_permiso_revocar.html', {
        'rol': rol,
        'permiso_id': permiso_id
    })


def rol_permiso_revocar_modulo(request, rol_id):
    rol = RolService.get_rol_by_id(rol_id)
    if not rol:
        messages.error(request, 'El rol no existe.')
        return redirect('roles_lista')

    if request.method == 'POST':
        modulo_id = request.POST.get('modulo_id')
        try:
            RolPermisoService.revocar_permisos_modulo_completo(rol_id, modulo_id)
            messages.success(request, 'Permisos del módulo revocados correctamente.')
            return redirect('rol_permiso_lista', rol_id=rol_id)
        except ValueError as exc:
            messages.error(request, str(exc))

    from ...services.modulo_service import ModuloService
    modulos = ModuloService.get_all_modulos()

    return render(request, 'rol_permisos/rol_permiso_revocar_modulo.html', {
        'rol': rol,
        'modulos': modulos
    })