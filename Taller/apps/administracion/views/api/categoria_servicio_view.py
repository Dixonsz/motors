from rest_framework import viewsets, status
from rest_framework.response import Response
from ...services.categoria_servicio_service import CategoriaServicioService
from ...serializers.categoria_servicio_serializers import CategoriaServicioSerializer
from django.views.decorators.cache import never_cache


class CategoriaServicioView(viewsets.ViewSet):

    @never_cache
    def list(self, request):
        categorias = CategoriaServicioService.get_all_categorias()
        serializer = CategoriaServicioSerializer(categorias, many=True)
        return Response(serializer.data)

    @never_cache
    def retrieve(self, request, pk=None):
        categoria = CategoriaServicioService.get_categoria_by_id(pk)

        if not categoria:
            return Response({'error': 'Categoria no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategoriaServicioSerializer(categoria)
        return Response(serializer.data)

    @never_cache
    def create(self, request):
        data = request.data

        try:
            categoria = CategoriaServicioService.create_categoria(
                nombre=data['nombre'],
                descripcion=data['descripcion'],
                is_active=data.get('is_active', True)
            )

            serializer = CategoriaServicioSerializer(categoria)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as e:
            return Response({'error': f'Campo requerido faltante: {e.args[0]}'}, status=status.HTTP_400_BAD_REQUEST)

    @never_cache
    def update(self, request, pk=None):
        data = request.data

        try:
            categoria = CategoriaServicioService.update_categoria(
                pk,
                nombre=data.get('nombre'),
                descripcion=data.get('descripcion'),
                is_active=data.get('is_active')
            )

            serializer = CategoriaServicioSerializer(categoria)
            return Response(serializer.data)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

    @never_cache
    def destroy(self, request, pk=None):
        try:
            CategoriaServicioService.delete_categoria(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)