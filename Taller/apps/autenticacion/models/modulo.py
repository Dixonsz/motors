from django.db import models

class Modulo(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.nombre
