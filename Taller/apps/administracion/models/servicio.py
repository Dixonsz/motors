from django.db import models

class Servicio(models.Model):
    nombre = models.CharField(max_length=100)    
    categoria_servicio = models.ForeignKey('CategoriaServicio', on_delete=models.CASCADE, related_name='servicios')
    descripcion = models.TextField(blank=True, null=True)
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)
    duracion_estimada = models.DurationField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return f" Nombre del servicio: {self.nombre} - Categoría: {self.categoria_servicio.nombre}"

    @property
    def duracion_hhmm(self):
        if not self.duracion_estimada:
            return ""
        total_segundos = int(self.duracion_estimada.total_seconds())
        horas = total_segundos // 3600
        minutos = (total_segundos % 3600) // 60
        return f"{horas:02d}:{minutos:02d}"