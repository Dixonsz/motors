from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from ...services.herramienta_service import HerramientaService
from ...services.estado_herramienta_service import EstadoHerramientaService
from ...services.categoria_herramienta_service import CategoriaHerramientaService

def herramienta_lista(request):
    herramientas = HerramientaService.get_all_herramientas()
    paginator = Paginator(herramientas, 10)
    page_number = request.GET.get('page')
    herramientas = paginator.get_page(page_number)

    return render(request, 'herramientas/herramientas_lista.html', {'herramientas': herramientas})

def herramienta_create(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        categoria_id = request.POST.get('categoria_id')
        marca = request.POST.get('marca')
        modelo = request.POST.get('modelo')

        try:
            HerramientaService.create_herramienta(nombre, descripcion, categoria_id, marca, modelo)
            messages.success(request, 'Herramienta creada correctamente.')
            return redirect('herramientas_lista')
        except ValueError as exc:
            messages.error(request, str(exc))
    
    categorias = CategoriaHerramientaService.get_all_categorias()
    return render(request, 'herramientas/herramientas_crear.html', {'categorias': categorias})    


def herramienta_editar(request, herramienta_id):
    herramienta = HerramientaService.get_herramienta_by_id(herramienta_id)
    categorias = CategoriaHerramientaService.get_all_categorias()
    if not herramienta:
        messages.error(request, 'La herramienta no existe.')
        return redirect('herramientas_lista')

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        categoria_id = request.POST.get('categoria_id')
        marca = request.POST.get('marca')
        modelo = request.POST.get('modelo')

        try:
            HerramientaService.update_herramienta(herramienta_id, nombre, descripcion, categoria_id, marca, modelo)
            messages.success(request, 'Herramienta actualizada correctamente.')
            return redirect('herramientas_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'herramientas/herramientas_editar.html', {'herramienta': herramienta, 'categorias': categorias})

def herramienta_eliminar(request, herramienta_id):
    herramienta = HerramientaService.get_herramienta_by_id(herramienta_id)
    if not herramienta:
        messages.error(request, 'La herramienta no existe.')
        return redirect('herramientas_lista')

    if request.method == 'POST':
        try:
            HerramientaService.delete_herramienta(herramienta_id)
            messages.success(request, 'Herramienta eliminada correctamente.')
            return redirect('herramientas_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'herramientas/herramientas_eliminar.html', {'herramienta': herramienta})
