from rest_framework import viewsets, status
from rest_framework.response import Response
from ...services.inventario_herramienta_service import InventarioHerramientaService
from ...serializers.inventario_herramienta_serializers import InventarioHerramientaSerializer
from django.views.decorators.cache import never_cache

class InventarioHerramientaView(viewsets.ViewSet):

    @never_cache
    def list(self, request):
        inventario = InventarioHerramientaService.get_all_inventario()
        serializer = InventarioHerramientaSerializer(inventario, many=True)
        return Response(serializer.data)

    @never_cache
    def retrieve(self, request, pk=None):
        inventario = InventarioHerramientaService.get_inventario_by_id(pk)

        if not inventario:
            return Response({'error': 'Inventario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        serializer = InventarioHerramientaSerializer(inventario)
        return Response(serializer.data)
    
    @never_cache
    def create(self, request):
        data = request.data

        try:
            inventario = InventarioHerramientaService.create_inventario(
                herramienta_id=data['herramienta_id'],
                cantidad_total=data['cantidad_total'],
                estado_nombre=data.get('estado_nombre', 'Disponible')
            )

            serializer = InventarioHerramientaSerializer(inventario)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as e:
            return Response({'error': f'Campo requerido faltante: {e.args[0]}'}, status=status.HTTP_400_BAD_REQUEST)
        
    @never_cache
    def update(self, request, pk=None):
        data = request.data

        try:
            inventario = InventarioHerramientaService.update_inventario(
                pk,
                herramienta_id=data.get('herramienta_id'),
                cantidad_total=data.get('cantidad_total'),
                estado_nombre=data.get('estado_nombre')
            )

            serializer = InventarioHerramientaSerializer(inventario)
            return Response(serializer.data)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        
    @never_cache
    def destroy(self, request, pk=None):
        try:
            InventarioHerramientaService.delete_inventario(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)