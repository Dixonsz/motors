from ..models import Modulo
from .utils import get_required_instance

class ModuloService:

    @staticmethod
    def get_all_modulos():
        return Modulo.objects.all()
    
    @staticmethod
    def get_modulo_by_id(modulo_id):
        try:
            return Modulo.objects.get(id=modulo_id)
        except Modulo.DoesNotExist:
            return None
        
    @staticmethod
    def create_modulo(nombre, descripcion=None):
        
        if Modulo.objects.filter(nombre__iexact=nombre).exists():
            raise ValueError("Ya existe un módulo con ese nombre.")
        
        modulo = Modulo(nombre=nombre, descripcion=descripcion or "")
        modulo.save()
        return modulo
    
    @staticmethod
    def update_modulo(modulo_id, nombre=None, descripcion=None, is_active=None):

        modulo = ModuloService.get_modulo_by_id(modulo_id)
        if not modulo:
            raise ValueError("Módulo no encontrado.")
        
        if nombre:
            if Modulo.objects.filter(nombre__iexact=nombre).exclude(id=modulo_id).exists():
                raise ValueError("Ya existe un módulo con ese nombre.")
            modulo.nombre = nombre
        if descripcion is not None:
            modulo.descripcion = descripcion
        if is_active is not None:
            modulo.is_active = is_active

        modulo.save()
        return modulo
    
    @staticmethod
    def delete_modulo(modulo_id):
        modulo = ModuloService.get_modulo_by_id(modulo_id)
        if not modulo:
            raise ValueError("Módulo no encontrado.")
        
        if modulo.permisos.exists():
            raise ValueError("No se puede eliminar el módulo porque tiene permisos asociados.")
        
        modulo.delete()