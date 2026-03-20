from django.contrib import messages
from django.shortcuts import redirect, render
from ...services.rol_service import RolService


def rol_lista(request):
    roles = RolService.get_all_roles()

    return render(request, 'roles/roles_lista.html', {'roles': roles})

def rol_create(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')

        try:
            RolService.create_rol(nombre, descripcion)
            messages.success(request, 'Rol creado correctamente.')
            return redirect('roles_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'roles/roles_crear.html')

def rol_editar(request, rol_id):
    rol = RolService.get_rol_by_id(rol_id)
    if not rol:
        messages.error(request, 'El rol no existe.')
        return redirect('roles_lista')

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')

        try:
            RolService.update_rol(rol_id, nombre, descripcion)
            messages.success(request, 'Rol actualizado correctamente.')
            return redirect('roles_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'roles/roles_editar.html', {'rol': rol})

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
