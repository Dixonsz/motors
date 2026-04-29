from rest_framework import serializers
from ..models.cita import Cita


class CitaSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.CharField(source='cliente.nombre', read_only=True)
    vehiculo_placa = serializers.CharField(source='vehiculo.placa', read_only=True)
    usuario_nombre = serializers.SerializerMethodField()
    estado_nombre = serializers.CharField(source='estado.nombre', read_only=True)
    servicios = serializers.SerializerMethodField()

    class Meta:
        model = Cita
        fields = [
            'id', 'cliente', 'cliente_nombre', 'vehiculo', 'vehiculo_placa',
            'usuario', 'usuario_nombre', 'estado', 'estado_nombre',
            'servicios', 'fecha', 'hora_inicio', 'anotaciones'
        ]

    def get_usuario_nombre(self, obj):
        return f"{obj.usuario.nombre} {obj.usuario.apellido}"

    def get_servicios(self, obj):
        return list(obj.servicio.values('id', 'nombre', 'precio_base'))