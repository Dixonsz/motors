from django.db import models


def default_dias_laborales():
    return [0, 1, 2, 3, 4]


class ConfiguracionCalendario(models.Model):

    TIPO_CHOICES = [
        ('dia_completo', 'Día completo'),
        ('franja',       'Franja horaria'),
        ('laboral',      'Horario laboral'),
    ]

    RECURRENCIA_CHOICES = [
        ('ninguna',  'Sin recurrencia'),
        ('diaria',   'Diaria'),
        ('semanal',  'Semanal'),
        ('mensual',  'Mensual'),
    ]

    tipo        = models.CharField(max_length=20, choices=TIPO_CHOICES)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin    = models.DateField(null=True, blank=True,
                                    help_text='Solo para rangos de días completos')
    hora_inicio  = models.TimeField(null=True, blank=True,
                                    help_text='Solo para franjas horarias')
    hora_fin     = models.TimeField(null=True, blank=True,
                                    help_text='Solo para franjas horarias')
    recurrencia  = models.CharField(max_length=20, choices=RECURRENCIA_CHOICES,
                                    default='ninguna')
    dias_laborales = models.JSONField(
        null=True,
        blank=True,
        default=default_dias_laborales,
        help_text='Dias laborales (0=Lunes, 6=Domingo)'
    )
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
        if self.tipo == 'laboral':
            if not self.hora_inicio or not self.hora_fin:
                raise ValidationError(
                    'El horario laboral debe tener hora de inicio y fin.'
                )
            if self.hora_inicio >= self.hora_fin:
                raise ValidationError(
                    'La hora de inicio debe ser menor a la hora de fin.'
                )
            if not self.dias_laborales:
                raise ValidationError(
                    'Debe seleccionar al menos un dia laboral.'
                )
        if self.tipo != 'laboral' and not self.fecha_inicio:
            raise ValidationError(
                'La fecha de inicio es obligatoria para este tipo de configuracion.'
            )
        if self.fecha_fin and self.fecha_fin < self.fecha_inicio:
            raise ValidationError(
                'La fecha de fin no puede ser anterior a la de inicio.'
            )

    @property
    def dias_laborales_label(self):
        if not self.dias_laborales:
            return '-'
        etiquetas = {
            0: 'Lun',
            1: 'Mar',
            2: 'Mie',
            3: 'Jue',
            4: 'Vie',
            5: 'Sab',
            6: 'Dom',
        }
        dias_ordenados = sorted(self.dias_laborales)
        return ', '.join(etiquetas.get(dia, str(dia)) for dia in dias_ordenados)

    def __str__(self):
        if self.tipo == 'dia_completo':
            return f"Configuración {self.fecha_inicio} — {self.motivo or 'Sin motivo'}"
        if self.tipo == 'laboral':
            return (
                f"Horario laboral {self.fecha_inicio} "
                f"{self.hora_inicio}-{self.hora_fin}"
            )
        return (f"Franja {self.fecha_inicio} "
                f"{self.hora_inicio}-{self.hora_fin} — {self.motivo or 'Sin motivo'}")
