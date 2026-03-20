from django.db import models

class InventarioHerramienta(models.Model):
    herramienta = models.ForeignKey('Herramienta', on_delete=models.CASCADE, related_name='inventarios')
    cantidad_total = models.PositiveIntegerField()
    cantidad_disponible = models.PositiveIntegerField()
    ubicacion = models.CharField(max_length=100, blank=True, null=True)
    fecha_ingreso = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.herramienta.nombre} - Cantidad Total: {self.cantidad_total}, Disponible: {self.cantidad_disponible}"