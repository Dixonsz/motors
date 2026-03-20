from ..models.categoria_servicio import CategoriaServicio
from django.core.exceptions import ObjectDoesNotExist

class CategoriaServicioService:

    @staticmethod
    def get_all_categorias():
        return CategoriaServicio.objects.all()
    
    @staticmethod
    def get_categoria_by_id(categoria_id):
        try:
            return CategoriaServicio.objects.get(id=categoria_id)
        except ObjectDoesNotExist:
            return None
       
        
    @staticmethod
    def create_categoria(nombre, descripcion, is_active=True):
        if CategoriaServicio.objects.filter(nombre=nombre).exists():
            raise ValueError("El nombre de la categoria ya existe.")
        categoria = CategoriaServicio(nombre=nombre, descripcion=descripcion, is_active=is_active)
        categoria.save()
        return categoria
    
    @staticmethod
    def update_categoria(categoria_id, nombre=None, descripcion=None, is_active=None):
        categoria = CategoriaServicioService.get_categoria_by_id(categoria_id)
        if not categoria:
            raise ValueError("La categoria no existe.")
        
        if nombre:
            if CategoriaServicio.objects.filter(nombre=nombre).exclude(id=categoria_id).exists():
                raise ValueError("El nombre de la categoria ya existe.")
            categoria.nombre = nombre
        
        if descripcion is not None:
            categoria.descripcion = descripcion
        
        if is_active is not None:
            categoria.is_active = is_active
        
        categoria.save()
        return categoria  
    
    @staticmethod
    def delete_categoria(categoria_id):
        categoria = CategoriaServicioService.get_categoria_by_id(categoria_id)
        if not categoria:
            raise ValueError("La categoria no existe.")
        categoria_nombre = categoria.nombre
        categoria.delete()
        return categoria_nombre




        