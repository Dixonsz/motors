from rest_framework import serializers
from administracion.models import AgendaHorario

class AgendaHorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgendaHorario
        fields = '__all__'