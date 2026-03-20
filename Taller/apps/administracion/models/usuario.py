from django.db import models
from .rol import Rol
from django.contrib.auth.models import AbstractUser 

class Usuario(AbstractUser):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT, related_name='usuarios')
   

    def __str__(self):
        correo = getattr(self, "correo", None) or getattr(self, "email", "sin-correo")
        rol_nombre = self.rol.nombre if self.rol else "sin-rol"
        return f"Nombre: {self.nombre} Apellido: {self.apellido} - Correo: {correo} - Rol: {rol_nombre}"