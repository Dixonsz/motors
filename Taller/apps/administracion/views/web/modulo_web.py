from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from ...services.modulo_service import ModuloService


def modulo_lista(request):
    modulos = ModuloService.get_all_modulos()
    paginator = Paginator(modulos, 10)
    page_number = request.GET.get('page')
    modulos = paginator.get_page(page_number)

    return render(request, 'modulos/modulos_lista.html', {'modulos': modulos})

def modulo_crear(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion', '')

        try:
            ModuloService.create_modulo(nombre, descripcion)
            messages.success(request, 'Módulo creado correctamente.')
            return redirect('modulos_lista')
        except ValueError as exc:
            messages.error(request, str(exc))
    
    return render(request, 'modulos/modulos_crear.html')

def modulo_editar(request, modulo_id):
    modulo = ModuloService.get_modulo_by_id(modulo_id)
    if not modulo:
        messages.error(request, 'El módulo no existe.')
        return redirect('modulos_lista')

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion', '')

        try:
            ModuloService.update_modulo(modulo_id, nombre, descripcion)
            messages.success(request, 'Módulo actualizado correctamente.')
            return redirect('modulos_lista')
        except ValueError as exc:
            messages.error(request, str(exc))
    
    return render(request, 'modulos/modulos_editar.html', {'modulo': modulo})

def modulo_eliminar(request, modulo_id):
    modulo = ModuloService.get_modulo_by_id(modulo_id)
    if not modulo:
        messages.error(request, 'El módulo no existe.')
        return redirect('modulos_lista')

    if request.method == 'POST':
        try:
            ModuloService.delete_modulo(modulo_id)
            messages.success(request, 'Módulo eliminado correctamente.')
            return redirect('modulos_lista')
        except ValueError as exc:
            messages.error(request, str(exc))
    
    return render(request, 'modulos/modulos_eliminar.html',{'modulo_id': modulo_id})