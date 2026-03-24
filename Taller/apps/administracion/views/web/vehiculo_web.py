from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from ...services.vehiculo_service import VehiculoService
from ...services.cliente_service import ClienteService
from ...services.modelo_service import ModeloService
from ...services.marca_service import MarcaService
from ...services.combustible_service import CombustibleService


def vehiculo_lista(request):
    vehiculos = VehiculoService.get_all_vehiculos()
    paginator = Paginator(vehiculos, 10)
    page_number = request.GET.get('page')
    vehiculos = paginator.get_page(page_number)

    return render(request, 'vehiculos/vehiculos_lista.html', {'vehiculos': vehiculos})

def vehiculo_create(request):
    if request.method == 'POST':
        placa = request.POST.get('placa')
        anio = request.POST.get('anio')
        color = request.POST.get('color')
        vin = request.POST.get('vin')
        cliente_id = request.POST.get('cliente_id')
        modelo_id = request.POST.get('modelo_id')
        marca_id = request.POST.get('marca_id')
        combustible_id = request.POST.get('combustible_id')

        try:
            VehiculoService.create_vehiculo(placa, anio, color, vin, cliente_id, modelo_id, marca_id, combustible_id)
            messages.success(request, 'Vehiculo creado correctamente.')
            return redirect('vehiculos_lista')
        except ValueError as exc:
            messages.error(request, str(exc))
    
    clientes = ClienteService.get_all_clientes()
    modelos = ModeloService.get_all_modelos()
    marcas = MarcaService.get_all_marcas()
    combustibles = CombustibleService.get_all_combustibles()
    return render(request, 'vehiculos/vehiculos_crear.html', {'clientes': clientes, 'modelos': modelos, 'marcas': marcas, 'combustibles': combustibles})    


def vehiculo_editar(request, vehiculo_id):
    vehiculo = VehiculoService.get_vehiculo_by_id(vehiculo_id)
    clientes = ClienteService.get_all_clientes()
    modelos = ModeloService.get_all_modelos()
    marcas = MarcaService.get_all_marcas()
    combustibles = CombustibleService.get_all_combustibles()

    if not vehiculo:
        messages.error(request, 'El vehiculo no existe.')
        return redirect('vehiculos_lista')

    if request.method == 'POST':
        placa = request.POST.get('placa')
        anio = request.POST.get('anio')
        color = request.POST.get('color')
        vin = request.POST.get('vin')
        cliente_id = request.POST.get('cliente_id')
        modelo_id = request.POST.get('modelo_id')
        marca_id = request.POST.get('marca_id')
        combustible_id = request.POST.get('combustible_id')

        try:
            VehiculoService.update_vehiculo(vehiculo_id, placa, anio, color, vin, cliente_id, modelo_id, marca_id, combustible_id)
            messages.success(request, 'Vehiculo actualizado correctamente.')
            return redirect('vehiculos_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'vehiculos/vehiculos_editar.html', {'vehiculo': vehiculo, 'clientes': clientes, 'modelos': modelos, 'marcas': marcas, 'combustibles': combustibles})

def vehiculo_eliminar(request, vehiculo_id):
    vehiculo = VehiculoService.get_vehiculo_by_id(vehiculo_id)
    if not vehiculo:
        messages.error(request, 'El vehiculo no existe.')
        return redirect('vehiculos_lista')

    if request.method == 'POST':
        try:
            VehiculoService.delete_vehiculo(vehiculo_id)
            messages.success(request, 'Vehiculo eliminado correctamente.')
            return redirect('vehiculos_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'vehiculos/vehiculos_eliminar.html', {'vehiculo_id': vehiculo_id})

