from rest_framework import viewsets, status
from rest_framework.response import Response
from ...services.cliente_service import ClienteService
from ...serializers.cliente_serializers import ClienteSerializer
from ...models.cliente import Cliente
from django.views.decorators.cache import never_cache

class ClienteView(viewsets.ViewSet):

    @never_cache
    def list(self, request):
        clientes = ClienteService.get_all_clientes()
        serializer = ClienteSerializer(clientes, many=True)
        return Response(serializer.data)
    
    @never_cache
    def retrieve(self, request, pk=None):
        cliente = ClienteService.get_cliente_by_id(pk)

        if not cliente:
            return Response({'error': 'Cliente no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ClienteSerializer(cliente)
        return Response(serializer.data)
    
    @never_cache
    def create(self, request):
        data = request.data

        try:
            cliente = ClienteService.create_cliente(
                nombre=data['nombre'],
                correo=data['correo'],
                telefono=data['telefono'],
                cedula=data['cedula'],
                direccion=data['direccion']
            )

            serializer = ClienteSerializer(cliente)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @never_cache
    def update(self, request, pk=None):
        data = request.data

        try:
            cliente = ClienteService.update_cliente(
                pk,
                nombre=data.get('nombre'),
                correo=data.get('correo'),
                telefono=data.get('telefono'),
                cedula=data.get('cedula'),
                direccion=data.get('direccion')
            )

            serializer = ClienteSerializer(cliente)
            return Response(serializer.data)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        
    @never_cache
    def destroy(self, request, pk=None):
        try:
            cliente_nombre = ClienteService.delete_cliente(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)