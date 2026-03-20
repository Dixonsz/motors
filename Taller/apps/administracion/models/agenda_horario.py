from django.utils import timezone
from django.db import models

class AgendaHorario(models.Model):
    DIAS_SEMANA = [
        ('lunes', 'Lunes'),
        ('martes', 'Martes'),
        ('miercoles', 'Miercoles'),
        ('jueves', 'Jueves'),
        ('viernes', 'Viernes'),
        ('sabado', 'Sabado'),
        ('domingo', 'Domingo'),
    ]

    TIPOS_BLOQUE = [
        ('disponible', 'Disponible'),
        ('bloqueado', 'Bloqueado'),
    ]

    fecha = models.DateField(default=timezone.now, null=True, blank=True)
    dia_semana = models.CharField(max_length=20, choices=DIAS_SEMANA, null=True, blank=True)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    tipo_bloque = models.CharField(max_length=20, choices=TIPOS_BLOQUE, default='disponible')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        etiqueta = self.get_dia_semana_display() if self.dia_semana else self.fecha
        return f" {self.get_tipo_bloque_display()} | {etiqueta}: {self.hora_inicio} - {self.hora_fin}"