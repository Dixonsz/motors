from ..models.marca import Marca

class MarcaService:

    @staticmethod
    def get_all_marcas():
        return Marca.objects.all()
    
    @staticmethod
    def get_marca_by_id(marca_id):
        try:
            return Marca.objects.get(id=marca_id)
        except Marca.DoesNotExist:
            return None
       
        
    @staticmethod
    def create_marca(nombre):
        if Marca.objects.filter(nombre=nombre).exists():
            raise ValueError("El nombre de la marca ya existe.")
        marca = Marca(nombre=nombre)
        marca.save()
        return marca
    
    @staticmethod
    def update_marca(marca_id, nombre=None):
        marca = MarcaService.get_marca_by_id(marca_id)
        if not marca:
            raise ValueError("La marca no existe.")
        
        if nombre:
            if Marca.objects.filter(nombre=nombre).exclude(id=marca_id).exists():
                raise ValueError("El nombre de la marca ya existe.")
            marca.nombre = nombre
        
        marca.save()
        return marca  
    
    @staticmethod
    def delete_marca(marca_id):
        marca = MarcaService.get_marca_by_id(marca_id)
        if not marca:
            raise ValueError("La marca no existe.")
        marca.delete()
        return marca.nombre

