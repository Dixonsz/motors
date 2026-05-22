from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.urls import reverse
from ...services.categoria_herramienta_service import CategoriaHerramientaService
from config.security import access_required, protected_error_to_message


@access_required("Herramientas", "ver")
def categoria_lista(request):
    categorias = CategoriaHerramientaService.get_all_categorias().order_by('id')
    paginator = Paginator(categorias, 10)
    page_number = request.GET.get('page')
    categorias_paginadas = paginator.get_page(page_number)
    return render(request, 'categoria_herramienta/categoria_herramientas_lista.html', {'categorias': categorias_paginadas})

@access_required("Herramientas", "crear")
def categoria_create(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        try:
            CategoriaHerramientaService.create_categoria(nombre, descripcion)
            messages.success(request, 'Categoría creada correctamente.')
            return redirect('categoria_herramientas_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'categoria_herramienta/categoria_herramientas_crear.html')

@access_required("Herramientas", "editar")
def categoria_editar(request, categoria_id):
    categoria = CategoriaHerramientaService.get_categoria_by_id(categoria_id)
    if not categoria:
        messages.error(request, 'La categoría no existe.')
        return redirect('categoria_herramientas_lista')

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        try:
            CategoriaHerramientaService.update_categoria(categoria_id, nombre, descripcion)
            messages.success(request, 'Categoría actualizada correctamente.')
            return redirect('categoria_herramientas_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'categoria_herramienta/categoria_herramientas_editar.html', {'categoria': categoria})

@access_required("Herramientas", "eliminar")
@protected_error_to_message
def categoria_eliminar(request, categoria_id):
    categoria = CategoriaHerramientaService.get_categoria_by_id(categoria_id)
    if not categoria:
        messages.error(request, 'La categoría no existe.')
        return redirect('categoria_herramientas_lista')

    if request.method == 'POST':
        try:
            CategoriaHerramientaService.delete_categoria(categoria_id)
            messages.success(request, 'Categoría eliminada correctamente.')
            return redirect('categoria_herramientas_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'confirmar_eliminacion.html', {'object': categoria, 'cancel_url': reverse('categoria_herramientas_lista'), 'categoria': categoria})
