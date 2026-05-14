from rest_framework import serializers
from ..models.modulo import Modulo


class ModuloSerializer(serializers.ModelSerializer):
    total_permisos = serializers.SerializerMethodField()

    class Meta:
        model = Modulo
        fields = ['id', 'nombre', 'descripcion', 'is_active', 'total_permisos']

    def get_total_permisos(self, obj):
        return obj.permisos.count()
