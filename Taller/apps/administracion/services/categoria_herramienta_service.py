from ..models.categoria_herramienta import CategoriaHerramienta


class CategoriaHerramientaService:

    @staticmethod
    def get_all_categorias():
        return CategoriaHerramienta.objects.all()
    
    @staticmethod
    def get_categoria_by_id(categoria_id):
        try:
            return CategoriaHerramienta.objects.get(id=categoria_id)
        except CategoriaHerramienta.DoesNotExist:
            return None
       
        
    @staticmethod
    def create_categoria(nombre, descripcion):
        if CategoriaHerramienta.objects.filter(nombre=nombre).exists():
            raise ValueError("El nombre de la categoria ya existe.")
        categoria = CategoriaHerramienta(nombre=nombre, descripcion=descripcion)
        categoria.save()
        return categoria
    
    @staticmethod
    def update_categoria(categoria_id, nombre=None, descripcion=None):
        categoria = CategoriaHerramientaService.get_categoria_by_id(categoria_id)
        if not categoria:
            raise ValueError("La categoria no existe.")
        
        if nombre:
            if CategoriaHerramienta.objects.filter(nombre=nombre).exclude(id=categoria_id).exists():
                raise ValueError("El nombre de la categoria ya existe.")
            categoria.nombre = nombre
        
        if descripcion is not None:
            categoria.descripcion = descripcion
        
        categoria.save()
        return categoria  
    
    @staticmethod
    def delete_categoria(categoria_id):
        categoria = CategoriaHerramientaService.get_categoria_by_id(categoria_id)
        if not categoria:
            raise ValueError("La categoria no existe.")
        categoria.delete()
        return categoria.nombre

    

