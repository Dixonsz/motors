from rest_framework import serializers
from ..models.orden_servicio import OrdenServicio

class OrdenServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenServicio
        fields = '__all__'