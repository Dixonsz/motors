from rest_framework import serializers
from ..models.permiso import Permiso


class PermisoSerializer(serializers.ModelSerializer):
    modulo_nombre = serializers.CharField(source='modulo.nombre', read_only=True)

    class Meta:
        model = Permiso
        fields = ['id', 'modulo', 'modulo_nombre', 'accion']
