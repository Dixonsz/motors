from rest_framework import serializers
from ..models.configuracion_calendario import BloqueoCalendario


class BloqueoSerializer(serializers.ModelSerializer):
    tipo_display        = serializers.CharField(source='get_tipo_display',        read_only=True)
    recurrencia_display = serializers.CharField(source='get_recurrencia_display', read_only=True)

    class Meta:
        model  = BloqueoCalendario
        fields = [
            'id', 'tipo', 'tipo_display', 'fecha_inicio', 'fecha_fin',
            'hora_inicio', 'hora_fin', 'recurrencia', 'recurrencia_display',
            'motivo', 'capacidad_maxima', 'activo',
        ]
