from rest_framework import serializers
from ..models.categoria_herramienta import CategoriaHerramienta

class CategoriaHerramientaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaHerramienta
        fields = ['__all__']