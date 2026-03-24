from rest_framework import viewsets, status
from rest_framework.response import Response
from ...services.categoria_herramienta_service import CategoriaHerramientaService
from ...serializers.categoria_herramienta_serializers import CategoriaHerramientaSerializer
from django.views.decorators.cache import never_cache


class CategoriaHerramientaView(viewsets.ViewSet):

    @never_cache
    def list(self, request):
        categorias = CategoriaHerramientaService.get_all_categorias()
        serializer = CategoriaHerramientaSerializer(categorias, many=True)
        return Response(serializer.data)

    @never_cache
    def retrieve(self, request, pk=None):
        categoria = CategoriaHerramientaService.get_categoria_by_id(pk)

        if not categoria:
            return Response({'error': 'Categoria no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategoriaHerramientaSerializer(categoria)
        return Response(serializer.data)

    @never_cache
    def create(self, request):
        data = request.data

        try:
            categoria = CategoriaHerramientaService.create_categoria(
                nombre=data['nombre'],
                descripcion=data['descripcion']
            )

            serializer = CategoriaHerramientaSerializer(categoria)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as e:
            return Response({'error': f'Campo requerido faltante: {e.args[0]}'}, status=status.HTTP_400_BAD_REQUEST)

    @never_cache
    def update(self, request, pk=None):
        data = request.data

        try:
            categoria = CategoriaHerramientaService.update_categoria(
                pk,
                nombre=data.get('nombre'),
                descripcion=data.get('descripcion')
            )

            serializer = CategoriaHerramientaSerializer(categoria)
            return Response(serializer.data)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

    @never_cache
    def destroy(self, request, pk=None):
        try:
            CategoriaHerramientaService.delete_categoria(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)