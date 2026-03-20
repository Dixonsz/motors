from django.shortcuts import redirect, render
from ...services.servicio_service import ServicioService
from ...services.categoria_servicio_service import CategoriaServicioService

def servicio_lista(request):
    servicios = ServicioService.get_all_servicios()
    categorias = CategoriaServicioService.get_all_categorias()

    return render(request, 'servicios/servicios_lista.html', {'servicios': servicios, 'categorias': categorias})

def servicio_create(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        categoria_id = request.POST.get('categoria_id')
        precio_base = request.POST.get('precio_base')
        duracion_estimada = request.POST.get('duracion_estimada')
        is_active = request.POST.get('is_active') == 'on'
        ServicioService.create_servicio(nombre, categoria_id, descripcion, precio_base, duracion_estimada, is_active)
        return redirect('servicios_lista')

    categorias = CategoriaServicioService.get_all_categorias()
    return render(request, 'servicios/servicios_crear.html', {'categorias': categorias})    


def servicio_editar(request, servicio_id):
    servicio = ServicioService.get_servicio_by_id(servicio_id)
    categorias = CategoriaServicioService.get_all_categorias()

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        categoria_id = request.POST.get('categoria_id')
        precio_base = request.POST.get('precio_base')
        duracion_estimada = request.POST.get('duracion_estimada')
        is_active = request.POST.get('is_active') == 'on'   

        ServicioService.update_servicio(
            servicio_id,
            categoria_id=categoria_id,
            nombre=nombre,
            descripcion=descripcion,
            precio_base=precio_base,
            duracion_estimada=duracion_estimada,
            is_active=is_active,
        )
        return redirect('servicios_lista')

    return render(request, 'servicios/servicios_editar.html', {'servicio': servicio, 'categorias': categorias})

def servicio_eliminar(request, servicio_id):
    if request.method == 'POST':
        ServicioService.delete_servicio(servicio_id)
        return redirect('servicios_lista')

    return render(request, 'servicios/servicios_eliminar.html', {'servicio_id': servicio_id})

