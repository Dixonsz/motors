from rest_framework import viewsets, status
from rest_framework.response import Response
from ...services.estado_service import EstadoService
from ...serializers.estado_serializers import EstadoSerializer
from django.views.decorators.cache import never_cache


class EstadoView(viewsets.ViewSet):

    @never_cache
    def list(self, request):
        estados = EstadoService.get_all_estados()
        serializer = EstadoSerializer(estados, many=True)
        return Response(serializer.data)

    @never_cache
    def retrieve(self, request, pk=None):
        estado = EstadoService.get_estado_by_id(pk)

        if not estado:
            return Response({'error': 'Estado no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        serializer = EstadoSerializer(estado)
        return Response(serializer.data)

    @never_cache
    def create(self, request):
        data = request.data

        try:
            estado = EstadoService.create_estado(
                nombre=data['nombre'],
                descripcion=data['descripcion'],
                is_active=data.get('is_active', True)
            )

            serializer = EstadoSerializer(estado)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as e:
            return Response({'error': f'Campo requerido faltante: {e.args[0]}'}, status=status.HTTP_400_BAD_REQUEST)

    @never_cache
    def update(self, request, pk=None):
        data = request.data

        try:
            estado = EstadoService.update_estado(
                pk,
                nombre=data.get('nombre'),
                descripcion=data.get('descripcion'),
                is_active=data.get('is_active')
            )

            serializer = EstadoSerializer(estado)
            return Response(serializer.data)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

    @never_cache
    def destroy(self, request, pk=None):
        try:
            EstadoService.delete_estado(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)