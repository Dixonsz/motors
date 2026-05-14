from rest_framework import serializers
from ..models.rol import Rol


class RolSerializer(serializers.ModelSerializer):
    total_usuarios = serializers.SerializerMethodField()
    total_permisos = serializers.SerializerMethodField()

    class Meta:
        model = Rol
        fields = ['id', 'nombre', 'descripcion', 'total_usuarios', 'total_permisos']

    def get_total_usuarios(self, obj):
        return obj.usuarios.count()

    def get_total_permisos(self, obj):
        return obj.permisos.count()
