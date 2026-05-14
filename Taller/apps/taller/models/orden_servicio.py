from django.db import models

class OrdenServicio(models.Model):
    recepcion = models.ForeignKey('taller.Recepcion', on_delete=models.PROTECT, related_name='ordenes_servicio')
    usuario = models.ForeignKey('autenticacion.Usuario', on_delete=models.PROTECT, related_name='ordenes_servicio')
    diagnostico = models.TextField(blank=True, null=True)
    estado = models.ForeignKey('vehiculos.Estado', on_delete=models.PROTECT, related_name='ordenes_servicio', default=1)
    observaciones = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_entrega = models.DateTimeField(blank=True, null=True)

    def total(self):
        return sum(detalle.precio * detalle.cantidad for detalle in self.ordenes_detalle.all())

    def __str__(self):
        estado_nombre = self.estado.nombre if self.estado_id else 'Sin estado'
        return f"Recepcion: {self.recepcion} - Usuario: {self.usuario} - Diagnostico: {self.diagnostico} - Estado: {estado_nombre}"
