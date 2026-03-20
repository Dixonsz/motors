from django.shortcuts import redirect, render
from ...services.modelo_service import ModeloService

def modelo_lista(request):
    modelo = ModeloService.get_all_modelos()

    return render(request, 'modelos/modelos_lista.html', {'modelos': modelo})

def modelo_create(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')

        ModeloService.create_modelo(nombre)
        return redirect('modelos_lista')
    
    return render(request, 'modelos/modelos_crear.html')

def modelo_editar(request, modelo_id):
    modelo = ModeloService.get_modelo_by_id(modelo_id)

    if request.method == 'POST':
        nombre = request.POST.get('nombre')

        ModeloService.update_modelo(modelo_id, nombre)
        return redirect('modelos_lista')
    
    return render(request, 'modelos/modelos_editar.html', {'modelo': modelo})

def modelo_eliminar(request, modelo_id):
    if request.method == 'POST':
        ModeloService.delete_modelo(modelo_id)
        return redirect('modelos_lista')
    
    return render(request, 'modelos/modelos_eliminar.html',{'modelo_id': modelo_id})