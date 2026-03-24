from django.db import models
from .categoria_herramienta import CategoriaHerramienta
from .estado_herramienta import EstadoHerramienta

class Herramienta(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    codigo_interno = models.CharField(max_length=50, unique=True, db_index=True, blank=True, null=True)
    categoria_herramienta = models.ForeignKey(CategoriaHerramienta, on_delete=models.SET_NULL, null=True, related_name='herramientas')
    marca = models.CharField(max_length=50, blank=True, null=True)
    modelo = models.CharField(max_length=50, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

class Meta:
    unique_together = ('nombre', 'codigo_interno', 'modelo')

def __str__(self):
    categoria = self.categoria_herramienta.nombre if self.categoria_herramienta else 'Sin categoría'
    return f"{self.nombre} ({self.codigo_interno}) - {categoria} - Marca: {self.marca} - Modelo: {self.modelo}"