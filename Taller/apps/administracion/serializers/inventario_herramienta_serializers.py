from rest_framework import serializers
from Taller.apps.administracion.models import InventarioHerramienta

class InventarioHerramientaSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventarioHerramienta
        fields = '__all__'