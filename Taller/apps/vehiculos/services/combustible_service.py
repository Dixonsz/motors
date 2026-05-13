from ..models.combustible import Combustible

class CombustibleService:

    @staticmethod
    def get_all_combustibles():
        return Combustible.objects.all()
    
    @staticmethod
    def get_combustible_by_id(combustible_id):
        try:
            return Combustible.objects.get(id=combustible_id)
        except Combustible.DoesNotExist:
            return None
        
    @staticmethod
    def create_combustible(nombre):
        if Combustible.objects.filter(nombre=nombre).exists():
            raise ValueError("El nombre del combustible ya existe.")
        combustible = Combustible(nombre=nombre)
        combustible.save()
        return combustible
    
    @staticmethod
    def update_combustible(combustible_id, nombre=None):
        combustible = CombustibleService.get_combustible_by_id(combustible_id)
        if not combustible:
            raise ValueError("El tipo de combustible no existe.")
        
        if nombre:
            if Combustible.objects.filter(nombre=nombre).exclude(id=combustible_id).exists():
                raise ValueError("El tipo de combustible ya existe.")
            combustible.nombre = nombre
        
        combustible.save()
        return combustible
    
    @staticmethod
    def delete_combustible(combustible_id):
        combustible = CombustibleService.get_combustible_by_id(combustible_id)
        if not combustible:
            raise ValueError("El tipo de combustible no existe.")
        combustible.delete()
        return combustible.nombre