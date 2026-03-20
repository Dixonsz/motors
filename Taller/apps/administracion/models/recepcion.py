from django.db import models

class Recepcion(models.Model):
    vehiculo = models.ForeignKey('Vehiculo', on_delete=models.CASCADE, related_name='recepciones')
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='recepciones')
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    observaciones = models.TextField(blank=True)
    kilometraje = models.PositiveIntegerField()
    nivel_combustible = models.PositiveBigIntegerField()

    def __str__(self):
        return f"Recepción de {self.vehiculo} por {self.usuario} el {self.fecha_ingreso}"
    
