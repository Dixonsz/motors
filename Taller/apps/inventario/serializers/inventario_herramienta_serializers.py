from rest_framework import serializers
from models import InventarioHerramienta

class InventarioHerramientaSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventarioHerramienta
        fields = '__all__'
