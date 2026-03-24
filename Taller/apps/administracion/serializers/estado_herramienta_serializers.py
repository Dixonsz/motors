from rest_framework import serializers
from ..models.estado_herramienta import EstadoHerramienta

class EstadoHerramientaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoHerramienta
        fields = ['__all__']