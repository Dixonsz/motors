from django.shortcuts import redirect, render
from ...services.categoria_servicio_service import CategoriaServicioService


def categoria_lista(request):
    categorias = CategoriaServicioService.get_all_categorias()

    return render(request, 'categoria_servicios/categoria_servicios_lista.html', {'categorias': categorias})

def categoria_create(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        is_active = request.POST.get('is_active') == 'on'

        CategoriaServicioService.create_categoria(nombre, descripcion, is_active)
        return redirect('categorias_lista')

    return render(request, 'categoria_servicios/categoria_servicios_crear.html')

def categoria_editar(request, categoria_id):
    categoria = CategoriaServicioService.get_categoria_by_id(categoria_id)

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        is_active = request.POST.get('is_active') == 'on'

        CategoriaServicioService.update_categoria(categoria_id, nombre, descripcion, is_active)
        return redirect('categorias_lista')

    return render(request, 'categoria_servicios/categoria_servicios_editar.html', {'categoria': categoria})

def categoria_eliminar(request, categoria_id):
    if request.method == 'POST':
        CategoriaServicioService.delete_categoria(categoria_id)
        return redirect('categorias_lista')

    return render(request, 'categoria_servicios/categoria_servicios_eliminar.html', {'categoria': categoria_id})
