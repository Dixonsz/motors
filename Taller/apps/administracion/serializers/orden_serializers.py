from rest_framework import serializers
from apps.administracion.models import Orden, OrdenServicio


class OrdenServicioSerializer(serializers.ModelSerializer):
    servicio_nombre = serializers.CharField(source='servicio.nombre', read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = OrdenServicio
        fields = ['id', 'orden', 'servicio', 'servicio_nombre', 'precio', 'cantidad', 'observaciones', 'subtotal']

    def get_subtotal(self, obj):
        return obj.precio * obj.cantidad


class OrdenSerializer(serializers.ModelSerializer):
    detalles = OrdenServicioSerializer(source='ordenes_servicio', many=True, read_only=True)
    estado_nombre = serializers.CharField(source='estado.nombre', read_only=True)

    class Meta:
        model = Orden
        fields = ['id', 'recepcion', 'usuario', 'diagnostico', 'estado', 'estado_nombre', 'detalles']