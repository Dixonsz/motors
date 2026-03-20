from django.contrib import messages
from django.shortcuts import redirect, render
from ...services.marca_service import MarcaService

def marca_lista(request):
    marcas = MarcaService.get_all_marcas()
    return render(request, 'marcas/marcas_lista.html', {'marcas': marcas})

def marca_create(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        try:
            MarcaService.create_marca(nombre)
            messages.success(request, 'Marca creada correctamente.')
            return redirect('marcas_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'marcas/marcas_crear.html')

def marca_editar(request, marca_id):
    marca = MarcaService.get_marca_by_id(marca_id)
    if not marca:
        messages.error(request, 'La marca no existe.')
        return redirect('marcas_lista')

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        try:
            MarcaService.update_marca(marca_id, nombre)
            messages.success(request, 'Marca actualizada correctamente.')
            return redirect('marcas_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'marcas/marcas_editar.html', {'marca': marca})

def marca_eliminar(request, marca_id):
    marca = MarcaService.get_marca_by_id(marca_id)
    if not marca:
        messages.error(request, 'La marca no existe.')
        return redirect('marcas_lista')

    if request.method == 'POST':
        try:
            MarcaService.delete_marca(marca_id)
            messages.success(request, 'Marca eliminada correctamente.')
            return redirect('marcas_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'marcas/marcas_eliminar.html', {'marca_id': marca_id})