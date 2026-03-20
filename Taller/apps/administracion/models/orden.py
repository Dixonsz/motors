from django.db import models

class Orden(models.Model):
   recepcion = models.ForeignKey('Recepcion', on_delete=models.CASCADE, related_name='ordenes')
   usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='ordenes')
   dignostico = models.TextField(blank=True, null=True)
   estado = models.ForeignKey('Estado', on_delete=models.PROTECT, related_name='ordenes')

   @property
   def diagnostico(self):
      return self.dignostico

   @diagnostico.setter
   def diagnostico(self, value):
      self.dignostico = value

   def __str__(self):
      estado_nombre = self.estado.nombre if self.estado_id else 'Sin estado'
      return f"Recepcion: {self.recepcion} - Usuario: {self.usuario} - Diagnostico: {self.dignostico} - Estado: {estado_nombre}"