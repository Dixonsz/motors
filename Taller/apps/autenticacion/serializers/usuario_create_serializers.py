from rest_framework import serializers
from ..models.usuario import Usuario


class UsuarioCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    rol_nombre = serializers.CharField(source='rol.nombre', read_only=True)

    class Meta:
        model = Usuario
        fields = [
            'id', 'username', 'password', 'nombre', 'apellido', 'cedula',
            'telefono', 'direccion', 'especialidad', 'rol', 'rol_nombre'
        ]
