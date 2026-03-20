from rest_framework import serializers
from ..models.recepcion import Recepcion

class RecepcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recepcion
        fields = '__all__'