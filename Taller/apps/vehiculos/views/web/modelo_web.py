from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.urls import reverse
from ...services.modelo_service import ModeloService
from config.security import access_required, protected_error_to_message

@access_required("Vehiculos", "ver")
def modelo_lista(request):
    nombre = request.GET.get('nombre', '').strip()

    
    modelo = ModeloService.get_modelos_filtrados(nombre=nombre or None)
    paginator = Paginator(modelo, 10)
    page_number = request.GET.get('page')
    modelo = paginator.get_page(page_number)
    filtros_query = request.GET.copy()
    filtros_query.pop('page', None)

    return render(request, 'modelos/modelos_lista.html', {'modelos': modelo, 'filtros': {'nombre': nombre}, 'filtros_query': filtros_query})

@access_required("Vehiculos", "crear")
def modelo_create(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        try:
            ModeloService.create_modelo(nombre)
            messages.success(request, 'Modelo creado correctamente.')
            return redirect('modelos_lista')
        except ValueError as exc:
            messages.error(request, str(exc))
    
    return render(request, 'modelos/modelos_crear.html')

@access_required("Vehiculos", "editar")
def modelo_editar(request, modelo_id):
    modelo = ModeloService.get_modelo_by_id(modelo_id)
    if not modelo:
        messages.error(request, 'El modelo no existe.')
        return redirect('modelos_lista')

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        try:
            ModeloService.update_modelo(modelo_id, nombre)
            messages.success(request, 'Modelo actualizado correctamente.')
            return redirect('modelos_lista')
        except ValueError as exc:
            messages.error(request, str(exc))
    
    return render(request, 'modelos/modelos_editar.html', {'modelo': modelo})

@access_required("Vehiculos", "eliminar")
@protected_error_to_message
def modelo_eliminar(request, modelo_id):
    modelo = ModeloService.get_modelo_by_id(modelo_id)
    if not modelo:
        messages.error(request, 'El modelo no existe.')
        return redirect('modelos_lista')

    if request.method == 'POST':
        try:
            ModeloService.delete_modelo(modelo_id)
            messages.success(request, 'Modelo eliminado correctamente.')
            return redirect('modelos_lista')
        except ValueError as exc:
            messages.error(request, str(exc))
    
    return render(request, 'confirmar_eliminacion.html', {'object': modelo, 'cancel_url': reverse('modelos_lista')})
