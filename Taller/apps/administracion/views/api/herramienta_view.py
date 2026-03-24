from rest_framework import viewsets, status
from rest_framework.response import Response
from ...services.herramienta_service import HerramientaService
from ...serializers.herramienta_serializers import HerramientaSerializer
from django.views.decorators.cache import never_cache

class HerramientaView(viewsets.ViewSet):

    @never_cache
    def list(self, request):
        herramientas = HerramientaService.get_all_herramientas()
        serializer = HerramientaSerializer(herramientas, many=True)
        return Response(serializer.data)

    @never_cache
    def retrieve(self, request, pk=None):
        herramienta = HerramientaService.get_herramienta_by_id(pk)

        if not herramienta:
            return Response({'error': 'Herramienta no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        serializer = HerramientaSerializer(herramienta)
        return Response(serializer.data)
    
    @never_cache
    def create(self, request):
        data = request.data

        try:
            herramienta = HerramientaService.create_herramienta(
                nombre=data['nombre'],
                descripcion=data['descripcion'],
                categoria_id=data['categoria_id'],
                marca=data['marca'],
                modelo=data['modelo']
            )

            serializer = HerramientaSerializer(herramienta)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as e:
            return Response({'error': f'Campo requerido faltante: {e.args[0]}'}, status=status.HTTP_400_BAD_REQUEST)
        
    @never_cache
    def update(self, request, pk=None):
        data = request.data

        try:
            herramienta = HerramientaService.update_herramienta(
                pk,
                nombre=data.get('nombre'),
                descripcion=data.get('descripcion'),
                categoria_id=data.get('categoria_id'),
                marca=data.get('marca'),
                modelo=data.get('modelo'),
            )

            serializer = HerramientaSerializer(herramienta)
            return Response(serializer.data)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        
    @never_cache
    def destroy(self, request, pk=None):
        try:
            HerramientaService.delete_herramienta(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)