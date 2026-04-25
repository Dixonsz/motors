from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from ...services.permiso_service import PermisoService
from ...services.modulo_service import ModuloService


def permiso_lista(request):
    permisos = PermisoService.get_all_permisos()
    paginator = Paginator(permisos, 10)
    page_number = request.GET.get('page')
    permisos = paginator.get_page(page_number)

    return render(request, 'permisos/permisos_lista.html', {'permisos': permisos})

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
    return render(request, 'permisos/permisos_crear.html', {'modulos': modulos})


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
    
    return render(request, 'permisos/permisos_eliminar.html',{'permiso_id': permiso_id})