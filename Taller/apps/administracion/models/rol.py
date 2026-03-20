from django.db import models

class Rol(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return  f"Nombre del rol: {self.nombre}"