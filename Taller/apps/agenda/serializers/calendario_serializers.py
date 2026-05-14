from rest_framework import serializers


class EventoCalendarioSerializer(serializers.Serializer):
    id    = serializers.IntegerField()
    title = serializers.CharField()
    start = serializers.CharField()
    color = serializers.CharField()
    extendedProps = serializers.DictField()


class VehiculoCalendarioSerializer(serializers.Serializer):
    id    = serializers.IntegerField()
    placa = serializers.CharField()


class FormDataCalendarioSerializer(serializers.Serializer):
    clientes  = serializers.ListField(child=serializers.DictField())
    estados   = serializers.ListField(child=serializers.DictField())
    servicios = serializers.ListField(child=serializers.DictField())
    usuarios  = serializers.ListField(child=serializers.DictField())
