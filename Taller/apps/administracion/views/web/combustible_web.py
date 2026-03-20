from django.shortcuts import redirect, render
from ...services.combustible_service import CombustibleService

def combustible_lista(request):
    combustibles = CombustibleService.get_all_combustibles()

    return render(request, 'combustibles/combustibles_lista.html', {'combustibles': combustibles})

def combustible_create(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')

        CombustibleService.create_combustible(nombre)
        return redirect('combustibles_lista')

    return render(request, 'combustibles/combustibles_crear.html')

def combustible_editar(request, combustible_id):
    combustible = CombustibleService.get_combustible_by_id(combustible_id)

    if request.method == 'POST':
        nombre = request.POST.get('nombre')

        CombustibleService.update_combustible(combustible_id, nombre)
        return redirect('combustibles_lista')

    return render(request, 'combustibles/combustibles_editar.html', {'combustible': combustible})

def combustible_eliminar(request, combustible_id):
    if request.method == 'POST':
        CombustibleService.delete_combustible(combustible_id)
        return redirect('combustibles_lista')

    return render(request, 'combustibles/combustibles_eliminar.html', {'combustible_id': combustible_id})