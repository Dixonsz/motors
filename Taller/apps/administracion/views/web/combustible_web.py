from django.contrib import messages
from django.shortcuts import redirect, render
from ...services.combustible_service import CombustibleService

def combustible_lista(request):
    combustibles = CombustibleService.get_all_combustibles()

    return render(request, 'combustibles/combustibles_lista.html', {'combustibles': combustibles})

def combustible_create(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        try:
            CombustibleService.create_combustible(nombre)
            messages.success(request, 'Combustible creado correctamente.')
            return redirect('combustibles_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'combustibles/combustibles_crear.html')

def combustible_editar(request, combustible_id):
    combustible = CombustibleService.get_combustible_by_id(combustible_id)
    if not combustible:
        messages.error(request, 'El combustible no existe.')
        return redirect('combustibles_lista')

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        try:
            CombustibleService.update_combustible(combustible_id, nombre)
            messages.success(request, 'Combustible actualizado correctamente.')
            return redirect('combustibles_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'combustibles/combustibles_editar.html', {'combustible': combustible})

def combustible_eliminar(request, combustible_id):
    combustible = CombustibleService.get_combustible_by_id(combustible_id)
    if not combustible:
        messages.error(request, 'El combustible no existe.')
        return redirect('combustibles_lista')

    if request.method == 'POST':
        try:
            CombustibleService.delete_combustible(combustible_id)
            messages.success(request, 'Combustible eliminado correctamente.')
            return redirect('combustibles_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'combustibles/combustibles_eliminar.html', {'combustible_id': combustible_id})