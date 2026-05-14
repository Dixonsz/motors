from django.db import models


class ConfiguracionCalendario(models.Model):

    TIPO_CHOICES = [
        ('dia_completo', 'Día completo'),
        ('franja',       'Franja horaria'),
    ]

    RECURRENCIA_CHOICES = [
        ('ninguna',  'Sin recurrencia'),
        ('diaria',   'Diaria'),
        ('semanal',  'Semanal'),
        ('mensual',  'Mensual'),
    ]

    tipo        = models.CharField(max_length=20, choices=TIPO_CHOICES)
    fecha_inicio = models.DateField()
    fecha_fin    = models.DateField(null=True, blank=True,
                                    help_text='Solo para rangos de días completos')
    hora_inicio  = models.TimeField(null=True, blank=True,
                                    help_text='Solo para franjas horarias')
    hora_fin     = models.TimeField(null=True, blank=True,
                                    help_text='Solo para franjas horarias')
    recurrencia  = models.CharField(max_length=20, choices=RECURRENCIA_CHOICES,
                                    default='ninguna')
    motivo       = models.CharField(max_length=255, blank=True, null=True)
    capacidad_maxima = models.PositiveIntegerField(
        null=True, blank=True,
        help_text='Máximo de citas permitidas en esa franja. Vacío = bloqueado total.'
    )
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name        = 'Configuración de calendario'
        verbose_name_plural = 'Configuraciones de calendario'
        ordering            = ['fecha_inicio', 'hora_inicio']

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.tipo == 'dia_completo':
                if self.hora_inicio or self.hora_fin:
                    raise ValidationError(
                        'Un bloqueo de día completo no debe tener horas.'
                    )
        if self.tipo == 'franja':
            if not self.hora_inicio or not self.hora_fin:
                raise ValidationError(
                    'Una franja horaria debe tener hora de inicio y fin.'
                )
            if self.hora_inicio >= self.hora_fin:
                raise ValidationError(
                    'La hora de inicio debe ser menor a la hora de fin.'
                )
        if self.fecha_fin and self.fecha_fin < self.fecha_inicio:
            raise ValidationError(
                'La fecha de fin no puede ser anterior a la de inicio.'
            )

    def __str__(self):
        if self.tipo == 'dia_completo':
            return f"Configuración {self.fecha_inicio} — {self.motivo or 'Sin motivo'}"
        return (f"Franja {self.fecha_inicio} "
                f"{self.hora_inicio}-{self.hora_fin} — {self.motivo or 'Sin motivo'}")
