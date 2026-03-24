from rest_framework import serializers
from ..models.herramienta import Herramienta

class HerramientaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Herramienta
        fields = '__all__'