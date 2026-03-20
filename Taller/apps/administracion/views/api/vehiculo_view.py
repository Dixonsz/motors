from rest_framework import viewsets, status
from rest_framework.response import Response
from ...services.vehiculo_service import VehiculoService
from ...serializers.vehiculo_serializers import VehiculoSerializer
from django.views.decorators.cache import never_cache

class VehiculoView(viewsets.ViewSet):

    @never_cache
    def list(self, request):
        vehiculos = VehiculoService.get_all_vehiculos()
        serializer = VehiculoSerializer(vehiculos, many=True)
        return Response(serializer.data)

    @never_cache
    def retrieve(self, request, pk=None):
        vehiculo = VehiculoService.get_vehiculo_by_id(pk)

        if not vehiculo:
            return Response({'error': 'Vehiculo no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        serializer = VehiculoSerializer(vehiculo)
        return Response(serializer.data)
    
    @never_cache
    def create(self, request):
        data = request.data

        try:
            vehiculo = VehiculoService.create_vehiculo(
                placa=data['placa'],
                anio=data['anio'],
                color=data['color'],
                vin=data['vin'],
                cliente_id=data['cliente_id'],
                modelo_id=data['modelo_id'],
                marca_id=data['marca_id'],
                combustible_id=data['combustible_id'],


            )

            serializer = VehiculoSerializer(vehiculo)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as e:
            return Response({'error': f'Campo requerido faltante: {e.args[0]}'}, status=status.HTTP_400_BAD_REQUEST)
        
    @never_cache
    def update(self, request, pk=None):
        data = request.data

        try:
            vehiculo = VehiculoService.update_vehiculo(
                pk,
                placa=data.get('placa'),
                anio=data.get('anio'),
                color=data.get('color'),
                vin=data.get('vin'),
                cliente_id=data.get('cliente_id'),
                modelo_id=data.get('modelo_id'),
                marca_id=data.get('marca_id'),
                combustible_id=data.get('combustible_id')


            )

            serializer = VehiculoSerializer(vehiculo)
            return Response(serializer.data)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        
    @never_cache
    def destroy(self, request, pk=None):
        try:
            VehiculoService.delete_vehiculo(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)