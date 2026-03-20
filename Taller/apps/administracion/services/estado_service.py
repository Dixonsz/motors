from ..models.estado import Estado

class EstadoService:

    @staticmethod
    def get_all_estados():
        return Estado.objects.all()
    
    @staticmethod
    def get_estado_by_id(estado_id):
        try:
            return Estado.objects.get(id=estado_id)
        except Estado.DoesNotExist:
            return None
       
        
    @staticmethod
    def create_estado(nombre, descripcion, is_active=True):
        if Estado.objects.filter(nombre=nombre).exists():
            raise ValueError("El nombre del estado ya existe.")
        estado = Estado(nombre=nombre, descripcion=descripcion, is_active=is_active)
        estado.save()
        return estado
    
    @staticmethod
    def update_estado(estado_id, nombre=None, descripcion=None, is_active=None):
        estado = EstadoService.get_estado_by_id(estado_id)
        if not estado:
            raise ValueError("El estado no existe.")
        
        if nombre:
            if Estado.objects.filter(nombre=nombre).exclude(id=estado_id).exists():
                raise ValueError("El nombre del estado ya existe.")
            estado.nombre = nombre
        
        if descripcion is not None:
            estado.descripcion = descripcion
        
        if is_active is not None:
            estado.is_active = is_active
        
        estado.save()
        return estado     
    
    @staticmethod
    def delete_estado(estado_id):
        estado = EstadoService.get_estado_by_id(estado_id)
        if not estado:
            raise ValueError("El estado no existe.")
        estado.delete()
        return estado.nombre

    

