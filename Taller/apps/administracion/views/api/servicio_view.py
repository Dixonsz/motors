from rest_framework import viewsets, status
from rest_framework.response import Response
from ...services.servicio_service import ServicioService
from ...serializers.servicio_serializers import ServicioSerializer
from django.views.decorators.cache import never_cache

class ServicioView(viewsets.ViewSet):

    @never_cache
    def list(self, request):
        servicios = ServicioService.get_all_servicios()
        serializer = ServicioSerializer(servicios, many=True)
        return Response(serializer.data)

    @never_cache
    def retrieve(self, request, pk=None):
        servicio = ServicioService.get_servicio_by_id(pk)

        if not servicio:
            return Response({'error': 'Servicio no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ServicioSerializer(servicio)
        return Response(serializer.data)
    
    @never_cache
    def create(self, request):
        data = request.data

        try:
            servicio = ServicioService.create_servicio(
                nombre=data['nombre'],
                categoria_id=data['categoria_id'],
                descripcion=data['descripcion'],
                precio_base=data['precio_base'],
                duracion_estimada=data['duracion_estimada'],
                is_active=data.get('is_active', True)
            )

            serializer = ServicioSerializer(servicio)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as e:
            return Response({'error': f'Campo requerido faltante: {e.args[0]}'}, status=status.HTTP_400_BAD_REQUEST)
        
    @never_cache
    def update(self, request, pk=None):
        data = request.data

        try:
            servicio = ServicioService.update_servicio(
                pk,
                categoria_id=data.get('categoria_id'),
                nombre=data.get('nombre'),
                descripcion=data.get('descripcion'),
                precio_base=data.get('precio_base'),
                duracion_estimada=data.get('duracion_estimada'),
                is_active=data.get('is_active')
            )

            serializer = ServicioSerializer(servicio)
            return Response(serializer.data)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        
    @never_cache
    def destroy(self, request, pk=None):
        try:
            ServicioService.delete_servicio(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)