from django.shortcuts import redirect, render
from ...services.cliente_service import ClienteService

def cliente_lista(request):
    clientes = ClienteService.get_all_clientes()

    return render(request, 'clientes/clientes_lista.html', {'clientes': clientes})

def cliente_create(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        telefono = request.POST.get('telefono')
        cedula = request.POST.get('cedula')
        direccion = request.POST.get('direccion')

        ClienteService.create_cliente(nombre, correo, telefono, cedula, direccion)
        return redirect('clientes_lista')

    return render(request, 'clientes/clientes_crear.html')

def cliente_editar(request, cliente_id):
    cliente = ClienteService.get_cliente_by_id(cliente_id)

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        telefono = request.POST.get('telefono')
        cedula = request.POST.get('cedula')
        direccion = request.POST.get('direccion')

        ClienteService.update_cliente(cliente_id, nombre, correo, telefono, cedula, direccion)
        return redirect('clientes_lista')

    return render(request, 'clientes/clientes_editar.html', {'cliente': cliente})

def cliente_eliminar(request, cliente_id):
    if request.method == 'POST':
        ClienteService.delete_cliente(cliente_id)
        return redirect('clientes_lista')

    return render(request, 'clientes/clientes_eliminar.html', {'cliente_id': cliente_id})