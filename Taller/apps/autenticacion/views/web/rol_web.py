from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.urls import reverse
from ...services.rol_service import RolService
from config.security import access_required, protected_error_to_message

@access_required("Roles", "ver")
def rol_lista(request):
    rol = RolService.get_all_roles()
    paginator = Paginator(rol, 10)
    page_number = request.GET.get('page')
    rol = paginator.get_page(page_number)

    return render(request, 'roles/roles_lista.html', {'roles': rol})

@access_required("Roles", "crear")
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

@access_required("Roles", "editar")
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

@access_required("Roles", "eliminar")
@protected_error_to_message
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
    
    return render(request, 'confirmar_eliminacion.html', {'object': rol, 'cancel_url': reverse('roles_lista')})
