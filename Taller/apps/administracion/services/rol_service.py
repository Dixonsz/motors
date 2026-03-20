from ..models.rol import Rol

class RolService:

    @staticmethod
    def get_all_roles():
        return Rol.objects.all()
    
    @staticmethod
    def get_rol_by_id(rol_id):
        try:
            return Rol.objects.get(id=rol_id)
        except Rol.DoesNotExist:
            return None
       
        
    @staticmethod
    def create_rol(nombre, descripcion):
        if Rol.objects.filter(nombre=nombre).exists():
            raise ValueError("El nombre del rol ya existe.")
        rol = Rol(nombre=nombre, descripcion=descripcion)
        rol.save()
        return rol
    
    @staticmethod
    def update_rol(rol_id, nombre=None, descripcion=None):
        rol = RolService.get_rol_by_id(rol_id)
        if not rol:
            raise ValueError("El rol no existe.")
        
        if nombre:
            if Rol.objects.filter(nombre=nombre).exclude(id=rol_id).exists():
                raise ValueError("El nombre del rol ya existe.")
            rol.nombre = nombre
        
        if descripcion is not None:
            rol.descripcion = descripcion
        
        rol.save()
        return rol  
    
    @staticmethod
    def delete_rol(rol_id):
        rol = RolService.get_rol_by_id(rol_id)
        if not rol:
            raise ValueError("El rol no existe.")
        rol.delete()
        return rol.nombre

    

