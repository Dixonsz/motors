from ..models import Permiso
from ..models.modulo import Modulo
from utils import get_required_instance

class PermisoService:

    @staticmethod
    def get_all_permisos():
        return Permiso.objects.all()
    
    @staticmethod
    def get_permiso_by_id(permiso_id):
        try:
            return Permiso.objects.get(id=permiso_id)
        except Permiso.DoesNotExist:
            return None
        
    @staticmethod
    def get_permisos_by_modulo(modulo_id):
        return Permiso.objects.filter(modulo_id=modulo_id)

    @staticmethod
    def create_permiso(modulo_id, accion):
        modulo = get_required_instance(Modulo, modulo_id, "Módulo no encontrado")

        if Permiso.objects.filter(modulo=modulo, accion=accion).exists():
            raise ValueError("El permiso ya existe para este módulo y acción")
        
        permiso = Permiso(modulo=modulo, accion=accion)
        permiso.save()
        return permiso
    
    @staticmethod
    def delete_permiso(permiso_id):
        permiso = PermisoService.get_permiso_by_id(permiso_id)

        if not permiso:
            raise ValueError("Permiso no encontrado")
        
        if permiso.roles.exists():
            raise ValueError("No se puede eliminar el permiso porque está asignado a uno o más roles")
        
        permiso.delete()

