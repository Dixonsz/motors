from rest_framework import serializers
from ..models.usuario import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    rol_nombre = serializers.CharField(source='rol.nombre', read_only=True)

    class Meta:
        model = Usuario
        fields = [
            'id', 'username', 'nombre', 'apellido', 'cedula',
            'telefono', 'direccion', 'especialidad', 'estado',
            'fecha_ingreso', 'rol', 'rol_nombre'
        ]
        read_only_fields = ['fecha_ingreso']


