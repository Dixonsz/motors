from ..models.estado_herramienta import EstadoHerramienta

class EstadoHerramientaService:

    @staticmethod
    def get_all_estados():
        return EstadoHerramienta.objects.all()
    
    @staticmethod
    def get_estado_by_id(estado_id):
        try:
            return EstadoHerramienta.objects.get(id=estado_id)
        except EstadoHerramienta.DoesNotExist:
            return None
       
        
    @staticmethod
    def create_estado(nombre, is_active=True):
        if EstadoHerramienta.objects.filter(nombre=nombre).exists():
            raise ValueError("El nombre del estado ya existe.")
        estado = EstadoHerramienta(nombre=nombre, is_active=is_active)
        estado.save()
        return estado
    
    @staticmethod
    def update_estado(estado_id, nombre=None, is_active=None):
        estado = EstadoHerramientaService.get_estado_by_id(estado_id)
        if not estado:
            raise ValueError("El estado no existe.")
        
        if nombre:
            if EstadoHerramienta.objects.filter(nombre=nombre).exclude(id=estado_id).exists():
                raise ValueError("El nombre del estado ya existe.")
            estado.nombre = nombre
        
        if is_active is not None:
            estado.is_active = is_active
        
        estado.save()
        return estado     
    
    @staticmethod
    def delete_estado(estado_id):
        estado = EstadoHerramientaService.get_estado_by_id(estado_id)
        if not estado:
            raise ValueError("El estado no existe.")
        estado.delete()
        return estado.nombre

    

