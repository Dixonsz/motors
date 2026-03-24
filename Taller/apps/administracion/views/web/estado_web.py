from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from ...services.estado_service import EstadoService


def estado_lista(request):
    estados = EstadoService.get_all_estados()
    paginator = Paginator(estados, 10)
    page_number = request.GET.get('page')
    estados = paginator.get_page(page_number)

    return render(request, 'estados/estados_lista.html', {'estados': estados})

def estado_create(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        is_active = request.POST.get('is_active') == 'on'

        try:
            EstadoService.create_estado(nombre, descripcion, is_active)
            messages.success(request, 'Estado creado correctamente.')
            return redirect('estados_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'estados/estados_crear.html')

def estado_editar(request, estado_id):
    estado = EstadoService.get_estado_by_id(estado_id)
    if not estado:
        messages.error(request, 'El estado no existe.')
        return redirect('estados_lista')

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        is_active = request.POST.get('is_active') == 'on'

        try:
            EstadoService.update_estado(estado_id, nombre, descripcion, is_active)
            messages.success(request, 'Estado actualizado correctamente.')
            return redirect('estados_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'estados/estados_editar.html', {'estado': estado})

def estado_eliminar(request, estado_id):
    estado = EstadoService.get_estado_by_id(estado_id)
    if not estado:
        messages.error(request, 'El estado no existe.')
        return redirect('estados_lista')

    if request.method == 'POST':
        try:
            EstadoService.delete_estado(estado_id)
            messages.success(request, 'Estado eliminado correctamente.')
            return redirect('estados_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'estados/estados_eliminar.html', {'estado_id': estado_id})
