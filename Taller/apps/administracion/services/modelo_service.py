from ..models.modelo import Modelo
from django.core.exceptions import ObjectDoesNotExist

class ModeloService:

    @staticmethod
    def get_all_modelos():
        return Modelo.objects.all()
    
    @staticmethod
    def get_modelo_by_id(modelo_id):
        try:
            return Modelo.objects.get(id=modelo_id)
        except ObjectDoesNotExist:
            return None
        
    @staticmethod
    def create_modelo(nombre):
        if Modelo.objects.filter(nombre=nombre).exists():
            raise ValueError("El modelo ya existe.")
        modelo = Modelo(nombre=nombre)
        modelo.save()
        return modelo
    
    @staticmethod
    def update_modelo(modelo_id, nombre=None):
        modelo = ModeloService.get_modelo_by_id(modelo_id)
        if not modelo:
            raise ValueError("El modelo no existe.")
        if modelo:
            if Modelo.objects.filter(nombre=nombre).exclude(id=modelo_id).exists():
                raise ValueError("El modelo ya existe.")
            modelo.nombre = nombre

        if nombre is not None:
            modelo.nombre = nombre

        modelo.save()
        return modelo
    
    @staticmethod
    def delete_modelo(modelo_id):
        modelo = ModeloService.get_modelo_by_id(modelo_id)
        if not modelo:
            raise ValueError("El modelo no existe.")
        modelo_nombre = modelo.nombre
        modelo.delete()
        return modelo_nombre

            