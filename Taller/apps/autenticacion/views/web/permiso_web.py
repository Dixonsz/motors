from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.urls import reverse
from ...services.permiso_service import PermisoService
from ...services.modulo_service import ModuloService
from ...services.rol_service import RolService
from config.security import access_required, protected_error_to_message


@access_required("Roles", "ver")
def permiso_lista(request):
    permisos = PermisoService.get_all_permisos()

    paginator = Paginator(permisos, 10)
    page_number = request.GET.get('page')
    permisos = paginator.get_page(page_number)

    return render(request, 'roles/permisos_lista.html', {
        'permisos': permisos,
    })

@access_required("Roles", "ver")
def rol_permisos_lista(request, rol_id):
    rol = RolService.get_rol_by_id(rol_id)
    permisos = PermisoService.get_all_permisos()

    paginator = Paginator(permisos, 10)
    page_number = request.GET.get('page')
    permisos = paginator.get_page(page_number)

    return render(request, 'roles/rol_permiso_lista.html', {
        'permisos': permisos,
        'rol': rol,
    })

@access_required("Roles", "crear")
def permiso_create(request):
    if request.method == 'POST':
        modulo_id = request.POST.get('modulo_id')
        accion = request.POST.get('accion')
        try:
            PermisoService.create_permiso(modulo_id, accion)
            messages.success(request, 'Permiso creado correctamente.')
            return redirect('permisos_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    modulos = ModuloService.get_all_modulos()
    return render(request, 'roles/permisos_crear.html', {'modulos': modulos})


@access_required("Roles", "eliminar")
@protected_error_to_message
def permiso_eliminar(request, permiso_id):
    permiso = PermisoService.get_permiso_by_id(permiso_id)
    if not permiso:
        messages.error(request, 'El permiso no existe.')
        return redirect('permisos_lista')

    if request.method == 'POST':
        try:
            PermisoService.delete_permiso(permiso_id)
            messages.success(request, 'Permiso eliminado correctamente.')
            return redirect('permisos_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'confirmar_eliminacion.html', {'object': permiso, 'cancel_url': reverse('permisos_lista')})
