from django.db import models
from cloudinary.models import CloudinaryField
from .recepcion import Recepcion



class Evidencia(models.Model):

    TIPO_EVIDENCIA = [
        ('foto', 'Foto'),
        ('video', 'Video'),
    ]
    recepcion = models.ForeignKey(Recepcion, on_delete=models.PROTECT, related_name='evidencias')

    tipo = models.CharField(max_length=10, choices=TIPO_EVIDENCIA)

    url_archivo = CloudinaryField('archivo')
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Evidencia: {self.tipo} Recepcion: {self.recepcion}"