from django.db import models

class Cita(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE, related_name='citas')
    vehiculo = models.ForeignKey('Vehiculo', on_delete=models.CASCADE, related_name='citas')
    servicio = models.ForeignKey('Servicio', on_delete=models.CASCADE, related_name='citas')
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    estado = models.CharField(max_length=20, default='Pendiente')
    anotaciones = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Cita {self.id} - {self.cliente.nombre} - {self.vehiculo.placa} - {self.fecha} - {self.hora_inicio}"