from rest_framework import serializers
from ..models.orden_servicio import OrdenServicio


class OrdenServicioSerializer(serializers.ModelSerializer):
    recepcion_vehiculo = serializers.CharField(source='recepcion.vehiculo.placa', read_only=True)
    usuario_nombre = serializers.SerializerMethodField()
    estado_nombre = serializers.CharField(source='estado.nombre', read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = OrdenServicio
        fields = [
            'id', 'recepcion', 'recepcion_vehiculo', 'usuario', 'usuario_nombre',
            'estado', 'estado_nombre', 'diagnostico', 'observaciones',
            'fecha_creacion', 'fecha_entrega', 'total'
        ]
        read_only_fields = ['fecha_creacion']

    def get_usuario_nombre(self, obj):
        return f"{obj.usuario.nombre} {obj.usuario.apellido}"

    def get_total(self, obj):
        return obj.total()
