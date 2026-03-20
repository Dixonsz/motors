from rest_framework import viewsets, status
from rest_framework.response import Response
from django.views.decorators.cache import never_cache

from ...services.evidencia_service import EvidenciaService
from ...serializers.evidencia_serializers import EvidenciaSerializer
from ...models.evidencia import Evidencia


class EvidenciaView(viewsets.ViewSet):

    @never_cache
    def list(self, request):

        recepcion_id = request.query_params.get('recepcion_id')

        if recepcion_id:
            evidencias = EvidenciaService.get_evidencias_by_recepcion(recepcion_id)
        else:
            evidencias = Evidencia.objects.all()

        serializer = EvidenciaSerializer(evidencias, many=True)
        return Response(serializer.data)


    @never_cache
    def retrieve(self, request, pk=None):

        evidencia = Evidencia.objects.filter(id=pk).first()

        if not evidencia:
            return Response(
                {'error': 'Evidencia no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = EvidenciaSerializer(evidencia)
        return Response(serializer.data)


    @never_cache
    def create(self, request):

        data = request.data
        archivos = request.FILES.getlist('archivos')

        try:

            evidencias = EvidenciaService.create_multiple_evidencias(
                recepcion_id=data['recepcion_id'],
                archivos=archivos,
                tipo=data['tipo']
            )

            serializer = EvidenciaSerializer(evidencias, many=True)

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        except ValueError as e:

            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


    @never_cache
    def update(self, request, pk=None):

        data = request.data
        archivo = request.FILES.get('archivo')

        try:

            evidencia = EvidenciaService.update_evidencia(
                pk,
                tipo=data.get('tipo'),
                archivo=archivo,
                descripcion=data.get('descripcion')
            )

            serializer = EvidenciaSerializer(evidencia)

            return Response(serializer.data)

        except ValueError as e:

            return Response(
                {'error': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )


    @never_cache
    def destroy(self, request, pk=None):

        try:

            EvidenciaService.delete_evidencia(pk)

            return Response(
                {"mensaje": "Evidencia eliminada"},
                status=status.HTTP_204_NO_CONTENT
            )

        except ValueError as e:

            return Response(
                {'error': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )