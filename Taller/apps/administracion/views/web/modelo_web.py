from django.contrib import messages
from django.shortcuts import redirect, render
from ...services.modelo_service import ModeloService

def modelo_lista(request):
    modelo = ModeloService.get_all_modelos()

    return render(request, 'modelos/modelos_lista.html', {'modelos': modelo})

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
    
    return render(request, 'modelos/modelos_eliminar.html',{'modelo_id': modelo_id})