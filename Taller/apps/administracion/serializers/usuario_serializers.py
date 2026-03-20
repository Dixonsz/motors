from rest_framework import serializers
from ..models.usuario import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = (
            'id',
            'nombre',
            'apellido',
            'telefono',
            'email',
            'username',
            'rol',
            'is_active',
            'date_joined',
            'password',
        )
        read_only_fields = ('id', 'date_joined', 'username')
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
        }