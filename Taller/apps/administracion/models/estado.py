from django.db import models

class Estado(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return  f"Nombre del estado: {self.nombre} - Descripción: {self.descripcion} - Activo: {'Sí' if self.is_active else 'No'}"