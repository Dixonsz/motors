from django.db import models

class EstadoHerramienta(models.Model):
    nombre = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


def __str__(self):
    return f" EstadoHerramienta(id={self.id}, nombre='{self.nombre}', is_active={self.is_active})"