from django.db import models

class Cita(models.Model):
    vehiculo = models.ForeignKey('Vehiculo', on_delete=models.CASCADE, related_name='citas', null=True, blank=True)
    cliente = models.ForeignKey('Cliente', on_delete=models.PROTECT, related_name='citas', null=True, blank=True)
    servicio = models.ManyToManyField('Servicio', related_name='citas', null=True, blank=True)
    usuario = models.ForeignKey('Usuario', on_delete=models.PROTECT, related_name='citas_asignadas')
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    estado = models.ForeignKey('Estado', on_delete=models.PROTECT, related_name='citas')
    anotaciones = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.cliente and not self.vehiculo:
            raise ValueError("Debe asignar al menos un cliente o un vehículo a la cita.")
        if self.vehiculo and self.cliente:
            if self.vehiculo.cliente != self.cliente:
                raise ValueError("El vehículo asignado no pertenece al cliente seleccionado.")
        super().save(*args, **kwargs)
    
    def __str__(self):
        data_cliente = self.cliente.nombre if self.cliente else 'Sin cliente'
        data_placa = self.vehiculo.placa if self.vehiculo else 'Sin vehículo'
        return f"Cita: {data_cliente} - {data_placa} - {self.fecha} {self.hora_inicio}"
