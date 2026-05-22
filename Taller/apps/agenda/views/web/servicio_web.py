from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.urls import reverse
from apps.agenda.services.servicio_service import ServicioService
from apps.agenda.services.categoria_servicio_service import CategoriaServicioService
from config.security import access_required, protected_error_to_message

@access_required("Servicios", "ver")
def servicio_lista(request):
    servicios = ServicioService.get_all_servicios()
    paginator = Paginator(servicios, 10)
    page_number = request.GET.get('page')
    servicios = paginator.get_page(page_number)
    categorias = CategoriaServicioService.get_all_categorias()

    return render(request, 'servicios/servicios_lista.html', {'servicios': servicios, 'categorias': categorias})

@access_required("Servicios", "crear")
def servicio_create(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        categoria_id = request.POST.get('categoria_id')
        precio_base = request.POST.get('precio_base')
        duracion_estimada = request.POST.get('duracion_estimada')
        is_active = request.POST.get('is_active') == 'on'
        try:
            ServicioService.create_servicio(nombre, categoria_id, descripcion, precio_base, duracion_estimada, is_active)
            messages.success(request, 'Servicio creado correctamente.')
            return redirect('servicios_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    categorias = CategoriaServicioService.get_all_categorias()
    return render(request, 'servicios/servicios_crear.html', {'categorias': categorias})    

@access_required("Servicios", "editar")
def servicio_editar(request, servicio_id):
    servicio = ServicioService.get_servicio_by_id(servicio_id)
    categorias = CategoriaServicioService.get_all_categorias()
    if not servicio:
        messages.error(request, 'El servicio no existe.')
        return redirect('servicios_lista')

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        categoria_id = request.POST.get('categoria_id')
        precio_base = request.POST.get('precio_base')
        duracion_estimada = request.POST.get('duracion_estimada')
        is_active = request.POST.get('is_active') == 'on'   

        try:
            ServicioService.update_servicio(
                servicio_id,
                categoria_id=categoria_id,
                nombre=nombre,
                descripcion=descripcion,
                precio_base=precio_base,
                duracion_estimada=duracion_estimada,
                is_active=is_active,
            )
            messages.success(request, 'Servicio actualizado correctamente.')
            return redirect('servicios_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'servicios/servicios_editar.html', {'servicio': servicio, 'categorias': categorias})

@access_required("Servicios", "eliminar")
@protected_error_to_message
def servicio_eliminar(request, servicio_id):
    servicio = ServicioService.get_servicio_by_id(servicio_id)
    if not servicio:
        messages.error(request, 'El servicio no existe.')
        return redirect('servicios_lista')

    if request.method == 'POST':
        try:
            ServicioService.delete_servicio(servicio_id)
            messages.success(request, 'Servicio eliminado correctamente.')
            return redirect('servicios_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'confirmar_eliminacion.html', {'object': servicio, 'cancel_url': reverse('servicios_lista')})

