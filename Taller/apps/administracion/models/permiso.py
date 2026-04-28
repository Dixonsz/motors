from django.db import models

class Permiso(models.Model):
 
    ACCIONES = [
        ('crear', 'Crear'),
        ('editar', 'Editar'),
        ('eliminar', 'Eliminar'),
        ('ver', 'Ver'),
    ]

    modulo = models.ForeignKey('Modulo', on_delete=models.CASCADE)
    accion = models.CharField(max_length=20, choices=ACCIONES)

    class Meta:
        unique_together = ('modulo', 'accion')

    def __str__(self):
        return f"{self.modulo.nombre} - {self.accion}"