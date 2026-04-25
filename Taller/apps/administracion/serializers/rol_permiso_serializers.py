from rest_framework import serializers
from ..models.rol_permiso import RolPermiso
from ..models.rol import Rol
from ..models.permiso import Permiso


class RolPermisoSerializer(serializers.ModelSerializer):
    rol_nombre = serializers.CharField(source='rol.nombre', read_only=True)
    modulo_nombre = serializers.CharField(source='permiso.modulo.nombre', read_only=True)
    accion = serializers.CharField(source='permiso.accion', read_only=True)

    class Meta:
        model = RolPermiso
        fields = ['id', 'rol', 'rol_nombre', 'permiso', 'modulo_nombre', 'accion']