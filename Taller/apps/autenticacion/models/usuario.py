from django.db import models
from .rol import Rol
from django.contrib.auth.models import AbstractUser 

class Usuario(AbstractUser):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20)
    estado = models.BooleanField(default=True)
    direccion = models.CharField(max_length=255)
    fecha_ingreso = models.DateField(auto_now_add=True)
    especialidad = models.CharField(max_length=100, blank=True, null=True)
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT, related_name='usuarios', null=True, blank=True)
   
   
    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.rol.nombre})"
