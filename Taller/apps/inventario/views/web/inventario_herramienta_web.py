from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.urls import reverse
from ...services.inventario_herramienta_service import InventarioHerramientaService
from ...services.estado_herramienta_service import EstadoHerramientaService
from ...services.herramienta_service import HerramientaService
from config.security import access_required, protected_error_to_message

@access_required("Herramientas", "ver")
def inventario_herramientas_lista(request):
    herramienta_id = request.GET.get('herramienta_id', '').strip()
    codigo_interno = request.GET.get('codigo_interno', '').strip()
    estado_id = request.GET.get('estado', '').strip()

    inventario = InventarioHerramientaService.get_inventario_filtrado(
        herramienta_id=herramienta_id if herramienta_id else None,
        codigo_interno=codigo_interno if codigo_interno else None,
        estado_id=estado_id if estado_id else None
    )
    paginator = Paginator(inventario, 10)
    page_number = request.GET.get('page')
    inventario = paginator.get_page(page_number)

    filtros_query = request.GET.copy()
    filtros_query.pop('page', None)

    return render(request, 'inventario_herramientas/inventario_herramientas_lista.html', {
        'inventario': inventario,
        'herramientas': HerramientaService.get_all_herramientas(),
        'estados': EstadoHerramientaService.get_all_estados(),
        'filtros': {
            'herramienta_id': herramienta_id,
            'codigo_interno': codigo_interno,
            'estado_id': estado_id
        },
        'filtros_query': filtros_query.urlencode(),
    })

@access_required("Herramientas", "crear")
def inventario_herramientas_create(request):
    if request.method == 'POST':
        herramienta_id = request.POST.get('herramienta_id')
        cantidad = request.POST.get('cantidad')
        estado_id = request.POST.get('estado_id')

        try:
            if not herramienta_id:
                raise ValueError('Debe seleccionar una herramienta.')
            if not estado_id:
                raise ValueError('Debe seleccionar un estado.')

            estado = EstadoHerramientaService.get_estado_by_id(estado_id)
            if not estado:
                raise ValueError('El estado de herramienta no existe.')

            InventarioHerramientaService.agregar_stock(
                herramienta_id=int(herramienta_id),
                cantidad=int(cantidad),
                estado_nombre=estado.nombre,
            )
            messages.success(request, 'Inventario creado correctamente.')
            return redirect('inventario_herramientas_lista')
        except (TypeError, ValueError) as exc:
            messages.error(request, str(exc))
    
    herramientas = HerramientaService.get_all_herramientas()
    estados = EstadoHerramientaService.get_all_estados()
    return render(request, 'inventario_herramientas/inventario_herramientas_crear.html', {'herramientas': herramientas, 'estados': estados})    


@access_required("Herramientas", "editar")
def inventario_herramientas_editar(request, inventario_id):
    inventario = InventarioHerramientaService.get_inventario_by_id(inventario_id)
    estados = EstadoHerramientaService.get_all_estados()
    if not inventario:
        messages.error(request, 'El inventario no existe.')
        return redirect('inventario_herramientas_lista')

    if request.method == 'POST':
        estado_destino_id = request.POST.get('estado_destino_id')
        cantidad = request.POST.get('cantidad')

        try:
            if not estado_destino_id:
                raise ValueError('Debe seleccionar un estado destino.')

            if int(estado_destino_id) == inventario.estado_id:
                raise ValueError('El estado destino debe ser diferente al estado origen.')

            InventarioHerramientaService.mover_herramienta(
                herramienta_id=inventario.herramienta_id,
                estado_origen_id=inventario.estado_id,
                estado_destino_id=int(estado_destino_id),
                cantidad=int(cantidad),
            )
            messages.success(request, 'Inventario actualizado correctamente.')
            return redirect('inventario_herramientas_lista')
        except (TypeError, ValueError) as exc:
            messages.error(request, str(exc))

    return render(
        request,
        'inventario_herramientas/inventario_herramientas_editar.html',
        {
            'inventario': inventario,
            'estados': estados,
        },
    )

@access_required("Herramientas", "eliminar")
@protected_error_to_message
def inventario_herramientas_eliminar(request, inventario_id):
    inventario = InventarioHerramientaService.get_inventario_by_id(inventario_id)
    if not inventario:
        messages.error(request, 'El inventario no existe.')
        return redirect('inventario_herramientas_lista')

    if request.method == 'POST':
        try:
            InventarioHerramientaService.delete_inventario(inventario_id)
            messages.success(request, 'Inventario eliminado correctamente.')
            return redirect('inventario_herramientas_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'confirmar_eliminacion.html', {'object': inventario, 'cancel_url': reverse('inventario_herramientas_lista')})
