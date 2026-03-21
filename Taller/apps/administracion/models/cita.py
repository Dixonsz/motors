from django.db import models

class Cita(models.Model):
    vehiculo = models.ForeignKey('Vehiculo', on_delete=models.CASCADE, related_name='citas')
    servicio = models.ForeignKey('Servicio', on_delete=models.CASCADE, related_name='citas')
    usuario = models.ForeignKey('Usuario', on_delete=models.PROTECT, related_name='citas_asignadas', null=True, blank=True)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    estado = models.ForeignKey('Estado', on_delete=models.PROTECT, related_name='citas')
    anotaciones = models.TextField(blank=True, null=True)
    
    def __str__(self):
        usuario_nombre = f"{self.usuario.nombre} {self.usuario.apellido}" if self.usuario else "Sin usuario"
        return f"Cita {self.id} - {self.vehiculo.placa} - {self.fecha} - {self.hora_inicio} a {self.hora_fin} - {usuario_nombre} - Estado: {self.estado.nombre}"