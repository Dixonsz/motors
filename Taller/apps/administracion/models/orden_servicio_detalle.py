from django.db import models

class OrdenServicioDetalle(models.Model):
    orden = models.ForeignKey('OrdenServicio', on_delete=models.CASCADE, related_name='ordenes_detalle')
    servicio = models.ForeignKey('Servicio', on_delete=models.PROTECT, related_name='ordenes_detalle')
    precio = models.PositiveIntegerField()
    cantidad = models.PositiveIntegerField(default=1)
    observaciones = models.TextField(blank=True, null=True)

    def subtotal(self):
        return self.precio * self.cantidad

    def __str__(self):
        return f"Orden #{self.orden_id} - Servicio: {self.servicio.nombre} - Cantidad: {self.cantidad} - Subtotal: {self.subtotal()}"