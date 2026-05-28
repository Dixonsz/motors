from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.urls import reverse
from ...services.estado_herramienta_service import EstadoHerramientaService
from config.security import access_required, protected_error_to_message


@access_required("Herramientas", "ver")
def estado_herramienta_lista(request):

    nombre = request.GET.get('nombre', '').strip()

    estados = EstadoHerramientaService.get_estados_filtrados(nombre=nombre.strip())
    paginator = Paginator(estados, 10)
    page_number = request.GET.get('page')
    estados = paginator.get_page(page_number)
    filtros_query = request.GET.copy()
    filtros_query.pop('page', None)

    return render(request, 'estado_herramientas/estado_herramientas_lista.html',
                   {'estados': estados,
                    'filtros': {
                       'nombre': nombre
                   },
                   'filtros_query': filtros_query.urlencode()
                   }
                   )


@access_required("Herramientas", "crear")
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

@access_required("Herramientas", "editar")
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

@access_required("Herramientas", "eliminar")
@protected_error_to_message
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

    return render(request, 'confirmar_eliminacion.html', {'object': estado, 'cancel_url': reverse('estado_herramientas_lista')})
