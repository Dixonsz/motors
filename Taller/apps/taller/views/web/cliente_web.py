from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import redirect, render
from ...services.cliente_service import ClienteService
from config.security import access_required, protected_error_to_message

ERROR_CLIENTE = "El cliente no existe o no se puede procesar la solicitud."

@access_required("Clientes", "ver")
def cliente_lista(request):
    clientes = ClienteService.get_all_clientes().order_by('id')
    paginator = Paginator(clientes, 10)
    page_number = request.GET.get('page')
    clientes = paginator.get_page(page_number)

    return render(request, 'clientes/clientes_lista.html', {'clientes': clientes})

@access_required("Clientes", "crear")
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

@access_required("Clientes", "editar")
def cliente_editar(request, cliente_id):
    cliente = ClienteService.get_cliente_by_id(cliente_id)
    if not cliente:
        messages.error(request, ERROR_CLIENTE)
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

@access_required("Clientes", "eliminar")
@protected_error_to_message
def cliente_eliminar(request, cliente_id):
    cliente = ClienteService.get_cliente_by_id(cliente_id)
    if not cliente:
        messages.error(request, ERROR_CLIENTE)
        return redirect('clientes_lista')

    if request.method == 'POST':
        try:
            ClienteService.delete_cliente(cliente_id)
            messages.success(request, 'Cliente eliminado correctamente.')
            return redirect('clientes_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'clientes/clientes_eliminar.html', {'cliente_id': cliente_id})


@access_required("Clientes", "ver")
def cliente_detalle_json(request, cliente_id):
    cliente = ClienteService.get_cliente_by_id(cliente_id)
    if not cliente:
        return JsonResponse({'detalle': ERROR_CLIENTE}, status=404)

    return JsonResponse({
        'id': cliente.id,
        'cedula': cliente.cedula,
        'telefono': cliente.telefono,
        'correo': cliente.correo,
        'direccion': cliente.direccion,
    })
