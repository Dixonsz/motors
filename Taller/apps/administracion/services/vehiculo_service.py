from ..models import Vehiculo, Modelo, Marca, Combustible, Cliente
from .utils import get_required_instance

class VehiculoService:

    @staticmethod
    def get_all_vehiculos():
        return Vehiculo.objects.all()
    
    @staticmethod
    def get_vehiculo_by_id(vehiculo_id):
        try:
            return Vehiculo.objects.get(id=vehiculo_id)
        except Vehiculo.DoesNotExist:
            return None
        
    @staticmethod
    def create_vehiculo(placa, anio, color, vin, cliente_id, modelo_id, marca_id, combustible_id):
        if Vehiculo.objects.filter(placa=placa).exists():
            raise ValueError("La Placa ya está registrada.")
        if Vehiculo.objects.filter(vin=vin).exists():
            raise ValueError("El VIN ya está registrado. ")

        cliente = get_required_instance(Cliente, cliente_id, "El cliente no existe.")
        modelo = get_required_instance(Modelo, modelo_id, "El modelo no existe.")
        marca = get_required_instance(Marca, marca_id, "La marca no existe.")
        combustible = get_required_instance(Combustible, combustible_id, "El combustible no existe.")


        vehiculo = Vehiculo(placa=placa,
                          anio=anio,
                          color=color,
                          vin=vin,
                          cliente = cliente,
                          modelo=modelo,
                          marca= marca,
                          combustible=combustible)
        vehiculo.save()
        return vehiculo
    
    @staticmethod
    def update_vehiculo(vehiculo_id, placa = None, anio = None, color = None, vin = None, cliente_id = None, modelo_id = None, marca_id = None, combustible_id = None):
        vehiculo = VehiculoService.get_vehiculo_by_id(vehiculo_id)
        if not vehiculo:
            raise ValueError("El vehiculo no existe.")
        
        if placa:
            if Vehiculo.objects.filter(placa=placa).exclude(id=vehiculo_id).exists():
                raise ValueError("La Placa ya está registrado.")
            vehiculo.placa = placa
        if anio:
            vehiculo.anio = anio
        if color:
            vehiculo.color = color
        if vin:
            if Vehiculo.objects.filter(vin=vin).exclude(id=vehiculo_id).exists():
                raise ValueError("El VIN ya está registrado.")
            vehiculo.vin = vin
        if cliente_id:
            cliente = get_required_instance(Cliente, cliente_id, "El cliente no existe.")
            vehiculo.cliente = cliente
        if modelo_id:
            modelo = get_required_instance(Modelo, modelo_id, "El modelo no existe.")
            vehiculo.modelo = modelo
        if marca_id:
            marca = get_required_instance(Marca, marca_id, "La marca no existe.")
            vehiculo.marca = marca
        if combustible_id:
            combustible = get_required_instance(Combustible, combustible_id, "El combustible no existe.")
            vehiculo.combustible = combustible
        
        vehiculo.save()
        return vehiculo
    
    @staticmethod
    def delete_vehiculo(vehiculo_id):
        vehiculo = VehiculoService.get_vehiculo_by_id(vehiculo_id)
        if not vehiculo:
            raise ValueError("El Vehiculo no existe.")
        vehiculo.delete()
