from rest_framework import serializers
from apps.administracion.models import Estado

class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = '__all__'