from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from ...services.categoria_herramienta_service import CategoriaHerramientaService

def categoria_lista(request):
    categorias = CategoriaHerramientaService.get_all_categorias().order_by('id')
    paginator = Paginator(categorias, 10)
    page_number = request.GET.get('page')
    categorias_paginadas = paginator.get_page(page_number)
    return render(request, 'categoria_herramienta/categoria_herramientas_lista.html', {'categorias': categorias_paginadas})

def categoria_create(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        try:
            CategoriaHerramientaService.create_categoria(nombre, descripcion)
            messages.success(request, 'Categoría creada correctamente.')
            return redirect('categorias_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'categoria_herramienta/categoria_herramientas_crear.html')

def categoria_editar(request, categoria_id):
    categoria = CategoriaHerramientaService.get_categoria_by_id(categoria_id)
    if not categoria:
        messages.error(request, 'La categoría no existe.')
        return redirect('categorias_lista')

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        try:
            CategoriaHerramientaService.update_categoria(categoria_id, nombre, descripcion)
            messages.success(request, 'Categoría actualizada correctamente.')
            return redirect('categorias_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'categoria_herramienta/categoria_herramientas_editar.html', {'categoria': categoria})

def categoria_eliminar(request, categoria_id):
    categoria = CategoriaHerramientaService.get_categoria_by_id(categoria_id)
    if not categoria:
        messages.error(request, 'La categoría no existe.')
        return redirect('categorias_lista')

    if request.method == 'POST':
        try:
            CategoriaHerramientaService.delete_categoria(categoria_id)
            messages.success(request, 'Categoría eliminada correctamente.')
            return redirect('categorias_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'categoria_herramienta/categoria_herramientas_eliminar.html', {'categoria': categoria})