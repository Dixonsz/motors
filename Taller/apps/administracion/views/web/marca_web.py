from django.shortcuts import redirect, render
from ...services.marca_service import MarcaService

def marca_lista(request):
    marcas = MarcaService.get_all_marcas()
    return render(request, 'marcas/marcas_lista.html', {'marcas': marcas})

def marca_create(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        MarcaService.create_marca(nombre)
        return redirect('marcas_lista')

    return render(request, 'marcas/marcas_crear.html')

def marca_editar(request, marca_id):
    marca = MarcaService.get_marca_by_id(marca_id)

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        MarcaService.update_marca(marca_id, nombre)
        return redirect('marcas_lista')

    return render(request, 'marcas/marcas_editar.html', {'marca': marca})

def marca_eliminar(request, marca_id):
    if request.method == 'POST':
        MarcaService.delete_marca(marca_id)
        return redirect('marcas_lista')

    return render(request, 'marcas/marcas_eliminar.html', {'marca_id': marca_id})