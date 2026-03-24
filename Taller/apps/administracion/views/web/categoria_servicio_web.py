from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from ...services.categoria_servicio_service import CategoriaServicioService


def categoria_lista(request):
    categorias = CategoriaServicioService.get_all_categorias()
    paginator = Paginator(categorias, 10)
    page_number = request.GET.get('page')
    categorias = paginator.get_page(page_number)

    return render(request, 'categoria_servicios/categoria_servicios_lista.html', {'categorias': categorias})

def categoria_create(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        is_active = request.POST.get('is_active') == 'on'

        try:
            CategoriaServicioService.create_categoria(nombre, descripcion, is_active)
            messages.success(request, 'Categoria creada correctamente.')
            return redirect('categorias_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'categoria_servicios/categoria_servicios_crear.html')

def categoria_editar(request, categoria_id):
    categoria = CategoriaServicioService.get_categoria_by_id(categoria_id)
    if not categoria:
        messages.error(request, 'La categoria no existe.')
        return redirect('categorias_lista')

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        is_active = request.POST.get('is_active') == 'on'

        try:
            CategoriaServicioService.update_categoria(categoria_id, nombre, descripcion, is_active)
            messages.success(request, 'Categoria actualizada correctamente.')
            return redirect('categorias_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'categoria_servicios/categoria_servicios_editar.html', {'categoria': categoria})

def categoria_eliminar(request, categoria_id):
    categoria = CategoriaServicioService.get_categoria_by_id(categoria_id)
    if not categoria:
        messages.error(request, 'La categoria no existe.')
        return redirect('categorias_lista')

    if request.method == 'POST':
        try:
            CategoriaServicioService.delete_categoria(categoria_id)
            messages.success(request, 'Categoria eliminada correctamente.')
            return redirect('categorias_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'categoria_servicios/categoria_servicios_eliminar.html', {'categoria': categoria_id})
