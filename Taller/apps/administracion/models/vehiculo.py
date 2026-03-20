from django.db import models

class Vehiculo(models.Model):

    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE, related_name='vehiculos')
    placa = models.CharField(max_length=20, unique=True)
    anio = models.PositiveIntegerField()
    color = models.CharField(max_length=50)
    vin = models.CharField(max_length=17, unique=True, blank=True)
    modelo = models.ForeignKey('Modelo', on_delete=models.CASCADE, related_name='vehiculos')
    combustible = models.ForeignKey('Combustible', on_delete=models.CASCADE, related_name='vehiculos')
    marca = models.ForeignKey('Marca', on_delete=models.CASCADE, related_name='vehiculos')

    def __str__(self):
        return f"   Placa: {self.placa} - Modelo: {self.modelo.nombre} - Marca: {self.marca.nombre}"
