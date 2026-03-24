from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from ...services.cliente_service import ClienteService

def cliente_lista(request):
    clientes = ClienteService.get_all_clientes()
    paginator = Paginator(clientes, 10)
    page_number = request.GET.get('page')
    clientes = paginator.get_page(page_number)

    return render(request, 'clientes/clientes_lista.html', {'clientes': clientes})

def cliente_create(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        telefono = request.POST.get('telefono')
        cedula = request.POST.get('cedula')
        direccion = request.POST.get('direccion')

        try:
            ClienteService.create_cliente(nombre, correo, telefono, cedula, direccion)
            messages.success(request, 'Cliente creado correctamente.')
            return redirect('clientes_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'clientes/clientes_crear.html')

def cliente_editar(request, cliente_id):
    cliente = ClienteService.get_cliente_by_id(cliente_id)
    if not cliente:
        messages.error(request, 'El cliente no existe.')
        return redirect('clientes_lista')

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        telefono = request.POST.get('telefono')
        cedula = request.POST.get('cedula')
        direccion = request.POST.get('direccion')

        try:
            ClienteService.update_cliente(cliente_id, nombre, correo, telefono, cedula, direccion)
            messages.success(request, 'Cliente actualizado correctamente.')
            return redirect('clientes_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'clientes/clientes_editar.html', {'cliente': cliente})

def cliente_eliminar(request, cliente_id):
    cliente = ClienteService.get_cliente_by_id(cliente_id)
    if not cliente:
        messages.error(request, 'El cliente no existe.')
        return redirect('clientes_lista')

    if request.method == 'POST':
        try:
            ClienteService.delete_cliente(cliente_id)
            messages.success(request, 'Cliente eliminado correctamente.')
            return redirect('clientes_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'clientes/clientes_eliminar.html', {'cliente_id': cliente_id})