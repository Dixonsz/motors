from django.db import models

class Permiso(models.Model):
 
    PERMISOS = [
        ('crear', 'Crear'),
        ('editar', 'Editar'),
        ('eliminar', 'Eliminar'),
        ('ver', 'Ver'),
    ]

    modulo = models.ForeignKey('Modulo', on_delete=models.CASCADE)
    permiso = models.CharField(max_length=20, choices=PERMISOS)

    class Meta:
        unique_together = ('modulo', 'permiso')

    def __str__(self):
        return f"{self.modulo.nombre} - {self.permiso}"