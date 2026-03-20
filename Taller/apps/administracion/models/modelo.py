from django.db import models

class Modelo(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return f" modelo: {self.nombre}"