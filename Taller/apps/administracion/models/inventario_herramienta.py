from django.db import models

class InventarioHerramienta(models.Model):
    herramienta = models.ForeignKey('Herramienta', on_delete=models.CASCADE)
    estado = models.ForeignKey('EstadoHerramienta', on_delete=models.CASCADE)
    cantidad_total = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.herramienta.nombre} - Cantidad: {self.cantidad_total}"