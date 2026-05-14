from django.db import models

class Recepcion(models.Model):
    vehiculo = models.ForeignKey('vehiculos.Vehiculo', on_delete=models.CASCADE, related_name='recepciones')
    usuario = models.ForeignKey('autenticacion.Usuario', on_delete=models.CASCADE, related_name='recepciones')
    cita = models.ForeignKey('agenda.Cita', on_delete=models.SET_NULL, related_name='recepciones', null=True, blank=True)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    observaciones = models.TextField(blank=True)
    kilometraje = models.PositiveIntegerField()
    nivel_combustible = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"Recepción de {self.vehiculo} por {self.usuario} el {self.fecha_ingreso}"
    
