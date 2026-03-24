from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from ...services.estado_herramienta_service import EstadoHerramientaService


def estado_herramienta_lista(request):
    estados = EstadoHerramientaService.get_all_estados()
    paginator = Paginator(estados, 10)
    page_number = request.GET.get('page')
    estados = paginator.get_page(page_number)

    return render(request, 'estado_herramientas/estado_herramientas_lista.html', {'estados': estados})

def estado_herramienta_create(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        is_active = request.POST.get('is_active') == 'on'

        try:
            EstadoHerramientaService.create_estado(nombre, is_active)
            messages.success(request, 'Estado creado correctamente.')
            return redirect('estado_herramientas_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'estado_herramientas/estado_herramientas_crear.html')

def estado_herramienta_editar(request, estado_id):
    estado = EstadoHerramientaService.get_estado_by_id(estado_id)
    if not estado:
        messages.error(request, 'El estado no existe.')
        return redirect('estado_herramientas_lista')

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        is_active = request.POST.get('is_active') == 'on'

        try:
            EstadoHerramientaService.update_estado(estado_id, nombre, is_active)
            messages.success(request, 'Estado actualizado correctamente.')
            return redirect('estado_herramientas_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'estado_herramientas/estado_herramientas_editar.html', {'estado': estado})

def estado_herramienta_eliminar(request, estado_id):
    estado = EstadoHerramientaService.get_estado_by_id(estado_id)
    if not estado:
        messages.error(request, 'El estado no existe.')
        return redirect('estado_herramientas_lista')

    if request.method == 'POST':
        try:
            EstadoHerramientaService.delete_estado(estado_id)
            messages.success(request, 'Estado eliminado correctamente.')
            return redirect('estado_herramientas_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'estado_herramientas/estado_herramientas_eliminar.html', {'estado_id': estado_id})
