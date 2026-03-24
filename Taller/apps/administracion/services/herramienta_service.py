from ..models import Herramienta, CategoriaHerramienta, EstadoHerramienta
from .utils import get_required_instance
import re


class HerramientaService:

    @staticmethod
    def get_all_herramientas():
        return Herramienta.objects.all()
    
    @staticmethod
    def get_herramienta_by_id(herramienta_id):
        try:
            return Herramienta.objects.get(id=herramienta_id)
        except Herramienta.DoesNotExist:
            return None
        
    @staticmethod
    def set_codigo_interno(nombre, categoria):
        set_nombre = re.sub(r'[^a-zA-Z]', '', nombre).upper()
        set_categoria = re.sub(r'[^a-zA-Z]', '', categoria.nombre).upper()

        prefix_nombre = set_nombre[:3]
        prefix_categoria = set_categoria[:3]

        base_codigo = f"{prefix_nombre}-{prefix_categoria}"

        for contador in range(1, 10000):
            codigo = f"{base_codigo}-{str(contador).zfill(3)}"
            if not Herramienta.objects.filter(codigo_interno=codigo).exists():
                return codigo

        raise Exception("No se pudo generar un código interno único para la herramienta.")

    @staticmethod
    def create_herramienta(nombre, descripcion, categoria_id, marca, modelo):
        categoria_herramienta = get_required_instance(CategoriaHerramienta, categoria_id, "La categoría no existe.")
        codigo_interno = HerramientaService.set_codigo_interno(nombre, categoria_herramienta)

        herramienta = Herramienta(
            nombre=nombre,
            descripcion=descripcion,
            codigo_interno=codigo_interno,
            categoria_herramienta=categoria_herramienta,
            marca=marca,
            modelo=modelo,
        )
        herramienta.save()
        return herramienta

    @staticmethod
    def update_herramienta(herramienta_id, nombre=None, descripcion=None, categoria_id=None, marca=None, modelo=None):
        update_codigo = False
        herramienta = HerramientaService.get_herramienta_by_id(herramienta_id)
        if not herramienta:
            raise ValueError("La herramienta no existe.")

        if nombre:
            herramienta.nombre = nombre
            update_codigo = True
        if descripcion:
            herramienta.descripcion = descripcion
        if categoria_id:
            categoria = get_required_instance(CategoriaHerramienta, categoria_id, "La categoría no existe.")
            herramienta.categoria_herramienta = categoria
            update_codigo = True
        if marca:
            herramienta.marca = marca
        if modelo:
            herramienta.modelo = modelo
        if update_codigo:
            herramienta.codigo_interno = HerramientaService.set_codigo_interno(herramienta.nombre, herramienta.categoria_herramienta)
        

        herramienta.save()
        return herramienta

    
    
    @staticmethod    
    def delete_herramienta(herramienta_id):
        herramienta = HerramientaService.get_herramienta_by_id(herramienta_id)
        if not herramienta:
            raise ValueError("La herramienta no existe.")
        herramienta.delete()
    
