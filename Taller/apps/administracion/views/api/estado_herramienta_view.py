from rest_framework import viewsets, status
from rest_framework.response import Response
from ...services.estado_herramienta_service import EstadoHerramientaService
from ...serializers.estado_herramienta_serializers import EstadoHerramientaSerializer
from django.views.decorators.cache import never_cache


class EstadoHerramientaView(viewsets.ViewSet):

    @never_cache
    def list(self, request):
        estados = EstadoHerramientaService.get_all_estados()
        serializer = EstadoHerramientaSerializer(estados, many=True)
        return Response(serializer.data)

    @never_cache
    def retrieve(self, request, pk=None):
        estado = EstadoHerramientaService.get_estado_by_id(pk)

        if not estado:
            return Response({'error': 'Estado no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        serializer = EstadoHerramientaSerializer(estado)
        return Response(serializer.data)

    @never_cache
    def create(self, request):
        data = request.data

        try:
            estado = EstadoHerramientaService.create_estado(
                nombre=data['nombre'],
                is_active=data.get('is_active', True)
            )

            serializer = EstadoHerramientaSerializer(estado)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as e:
            return Response({'error': f'Campo requerido faltante: {e.args[0]}'}, status=status.HTTP_400_BAD_REQUEST)

    @never_cache
    def update(self, request, pk=None):
        data = request.data

        try:
            estado = EstadoHerramientaService.update_estado(
                pk,
                nombre=data.get('nombre'),
                is_active=data.get('is_active')
            )

            serializer = EstadoHerramientaSerializer(estado)
            return Response(serializer.data)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

    @never_cache
    def destroy(self, request, pk=None):
        try:
            EstadoHerramientaService.delete_estado(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)