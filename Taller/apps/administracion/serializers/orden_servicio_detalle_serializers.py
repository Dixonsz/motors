from rest_framework import serializers
from ..models.orden_servicio_detalle import OrdenServicioDetalle


class OrdenServicioDetalleSerializer(serializers.ModelSerializer):
    servicio_nombre = serializers.CharField(source='servicio.nombre', read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = OrdenServicioDetalle
        fields = [
            'id', 'orden', 'servicio', 'servicio_nombre',
            'precio', 'cantidad', 'subtotal', 'observaciones'
        ]

    def get_subtotal(self, obj):
        return obj.subtotal()
