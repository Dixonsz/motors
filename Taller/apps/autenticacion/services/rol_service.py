from ..models import Rol
from .rol_permiso_service import RolPermisoService
from .utils import get_required_instance

class RolService:

    @staticmethod
    def get_all_roles():
        return Rol.objects.all()
    
    @staticmethod
    def get_rol_by_id(rol_id):
        try:
            return Rol.objects.get(id=rol_id)
        except Rol.DoesNotExist:
            raise ValueError("Rol no encontrado.")
        
    @staticmethod
    def create_rol(nombre, descripcion=None):
        if Rol.objects.filter(nombre=nombre).exists():
            raise ValueError("Ya existe un rol con ese nombre.")
        
        rol = Rol(nombre=nombre, descripcion=descripcion or "")
        rol.save()
        return rol
    
    @staticmethod
    def update_rol(rol_id, nombre=None, descripcion=None):

        rol = RolService.get_rol_by_id(rol_id)
        if not rol:
            raise ValueError("Rol no encontrado.")
        
        if nombre:
            if Rol.objects.filter(nombre=nombre).exclude(id=rol_id).exists():
                raise ValueError("Ya existe un rol con ese nombre.")
            rol.nombre = nombre
        
        if descripcion is not None:
            rol.descripcion = descripcion

        rol.save()
        return rol
    
    @staticmethod
    def delete_rol(rol_id):
        rol = RolService.get_rol_by_id(rol_id)
        if not rol:
            raise ValueError("Rol no encontrado.")
        
        if rol.usuarios.exists():
            raise ValueError("No se puede eliminar el rol porque está asignado a usuarios.")
        
        rol.permisos.all().delete()
        rol.delete()


