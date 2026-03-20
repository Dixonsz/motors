from django.db import models

class Herramienta(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    codigo_interno = models.CharField(max_length=50, unique=True)
    categoria_herramienta = models.ForeignKey('CategoriaHerramienta', on_delete=models.SET_NULL, null=True, related_name='herramientas')
    marca = models.CharField(max_length=50, blank=True, null=True)
    modelo = models.CharField(max_length=50, blank=True, null=True)
    estado = models.CharField(max_length=20, default='Disponible')

    def __str__(self):
        return f"{self.nombre} - {self.codigo_interno}"