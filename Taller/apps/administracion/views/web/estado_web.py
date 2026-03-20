from django.shortcuts import redirect, render
from ...services.estado_service import EstadoService


def estado_lista(request):
    estados = EstadoService.get_all_estados()

    return render(request, 'estados/estados_lista.html', {'estados': estados})

def estado_create(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        is_active = request.POST.get('is_active') == 'on'

        EstadoService.create_estado(nombre, descripcion, is_active)
        return redirect('estados_lista')

    return render(request, 'estados/estados_crear.html')

def estado_editar(request, estado_id):
    estado = EstadoService.get_estado_by_id(estado_id)

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        is_active = request.POST.get('is_active') == 'on'

        EstadoService.update_estado(estado_id, nombre, descripcion, is_active)
        return redirect('estados_lista')

    return render(request, 'estados/estados_editar.html', {'estado': estado})

def estado_eliminar(request, estado_id):
    if request.method == 'POST':
        EstadoService.delete_estado(estado_id)
        return redirect('estados_lista')

    return render(request, 'estados/estados_eliminar.html', {'estado_id': estado_id})
