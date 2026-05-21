from rest_framework import serializers
from apps.taller.models.orden_servicio import OrdenServicio
from apps.taller.models.orden_servicio_detalle import OrdenServicioDetalle
from apps.taller.models.evidencia import Evidencia
from apps.taller.models.recepcion import Recepcion
from apps.vehiculos.models.estado import Estado


class EstadoPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = ['nombre']


class EvidenciaPublicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Evidencia
        fields = [
            'tipo',
            'url_archivo',
            'descripcion',
            'fecha_subida',
        ]
        read_only_fields = fields


class RecepcionPublicSerializer(serializers.ModelSerializer):

    evidencias = EvidenciaPublicSerializer(many=True, read_only=True)

    class Meta:
        model = Recepcion
        fields = [
            'fecha_ingreso',
            'kilometraje',
            'nivel_combustible',
            'observaciones',
            'evidencias',
        ]
        read_only_fields = fields


class OrdenServicioDetallePublicSerializer(serializers.ModelSerializer):

    servicio = serializers.StringRelatedField(read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = OrdenServicioDetalle
        fields = [
            'servicio',
            'precio',
            'cantidad',
            'subtotal',
        ]
        read_only_fields = fields

    def get_subtotal(self, obj):
        return obj.subtotal()


class OrdenServicioPublicSerializer(serializers.ModelSerializer):

    estado = EstadoPublicSerializer(read_only=True)
    ordenes_detalle = OrdenServicioDetallePublicSerializer(many=True, read_only=True)
    recepcion = RecepcionPublicSerializer(read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = OrdenServicio
        fields = [
            'id',
            'fecha_creacion',
            'fecha_entrega',
            'estado',
            'diagnostico',
            'total',
            'recepcion',
            'ordenes_detalle',
        ]
        read_only_fields = fields

    def get_total(self, obj):
        return obj.total()