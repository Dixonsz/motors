from rest_framework import serializers
from apps.vehiculos.models.vehiculo import Vehiculo
from apps.vehiculos.models.marca import Marca
from apps.vehiculos.models.modelo import Modelo
from apps.vehiculos.models.combustible import Combustible


class MarcaPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = ['nombre']


class ModeloPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modelo
        fields = ['nombre']


class CombustiblePublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Combustible
        fields = ['nombre']


class VehiculoPublicSerializer(serializers.ModelSerializer):

    marca = MarcaPublicSerializer(read_only=True)
    modelo = ModeloPublicSerializer(read_only=True)
    combustible = CombustiblePublicSerializer(read_only=True)

    class Meta:
        model = Vehiculo
        fields = [
            'placa',
            'anio',
            'color',
            'marca',
            'modelo',
            'combustible',
        ]
        read_only_fields = fields