from django.shortcuts import redirect, render
from ...services.rol_service import RolService


def rol_lista(request):
    roles = RolService.get_all_roles()

    return render(request, 'roles/roles_lista.html', {'roles': roles})

def rol_create(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')

        RolService.create_rol(nombre, descripcion)
        return redirect('roles_lista')

    return render(request, 'roles/roles_crear.html')

def rol_editar(request, rol_id):
    rol = RolService.get_rol_by_id(rol_id)

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')

        RolService.update_rol(rol_id, nombre, descripcion)
        return redirect('roles_lista')

    return render(request, 'roles/roles_editar.html', {'rol': rol})

def rol_eliminar(request, rol_id):
    if request.method == 'POST':
        RolService.delete_rol(rol_id)
        return redirect('roles_lista')

    return render(request, 'roles/roles_eliminar.html', {'rol_id': rol_id})
