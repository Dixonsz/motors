from django.db import models


class RolPermiso(models.Model):

    rol = models.ForeignKey('Rol', on_delete=models.CASCADE)
    permiso = models.ForeignKey('Permiso', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('rol', 'permiso')

    def __str__(self):
        return f"{self.rol.nombre} - {self.permiso}"