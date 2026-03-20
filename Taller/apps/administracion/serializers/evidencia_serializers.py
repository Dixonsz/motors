from rest_framework import serializers
from ..models.evidencia import Evidencia

class EvidenciaSerializer(serializers.ModelSerializer):

    url_archivo = serializers.SerializerMethodField()
    class Meta:
        model = Evidencia
        fields = '__all__'
    
    def get_url_archivo(self, obj):
        if obj.url_archivo:
            return obj.url_archivo.url
        return None