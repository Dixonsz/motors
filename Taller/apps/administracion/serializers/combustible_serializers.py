from rest_framework import serializers
from ..models.combustible import Combustible

class CombustibleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Combustible
        fields = '__all__'