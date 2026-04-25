from rest_framework import serializers
from ..models.recepcion import Recepcion


class RecepcionSerializer(serializers.ModelSerializer):
    vehiculo_placa = serializers.CharField(source='vehiculo.placa', read_only=True)
    usuario_nombre = serializers.SerializerMethodField()
    cliente_nombre = serializers.SerializerMethodField()
    cita_id = serializers.IntegerField(source='cita.id', read_only=True)

    class Meta:
        model = Recepcion
        fields = [
            'id', 'vehiculo', 'vehiculo_placa', 'usuario', 'usuario_nombre',
            'cliente_nombre', 'cita', 'cita_id', 'fecha_ingreso',
            'observaciones', 'kilometraje', 'nivel_combustible'
        ]
        read_only_fields = ['fecha_ingreso']

    def get_usuario_nombre(self, obj):
        return f"{obj.usuario.nombre} {obj.usuario.apellido}"

    def get_cliente_nombre(self, obj):
        return obj.vehiculo.cliente.nombre if obj.vehiculo.cliente else 'Sin cliente'