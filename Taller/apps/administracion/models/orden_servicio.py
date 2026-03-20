from django.db import models

class OrdenServicio(models.Model):
    orden = models.ForeignKey('Orden', on_delete=models.CASCADE, related_name='ordenes_servicio')
    servicio = models.ForeignKey('Servicio', on_delete=models.CASCADE, related_name='ordenes_servicio')
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.PositiveIntegerField()
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Orden #{self.orden_id} - Servicio: {self.servicio.nombre}"