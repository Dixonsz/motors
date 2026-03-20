from rest_framework import viewsets, status
from rest_framework.response import Response
from ...services.agenda_horario_service import AgendaHorarioService
from ...serializers.agenda_horario_serializers import AgendaHorarioSerializer
from django.views.decorators.cache import never_cache


class AgendaHorarioView(viewsets.ViewSet):

    @never_cache
    def list(self, request):
        agenda_horarios = AgendaHorarioService.get_all_agenda_horarios()
        serializer = AgendaHorarioSerializer(agenda_horarios, many=True)
        return Response(serializer.data)

    @never_cache
    def retrieve(self, request, pk=None):
        agenda_horario = AgendaHorarioService.get_agenda_horario_by_id(pk)

        if not agenda_horario:
            return Response({'error': 'Horario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AgendaHorarioSerializer(agenda_horario)
        return Response(serializer.data)

    @never_cache
    def create(self, request):
        data = request.data

        try:
            dias_semana = data.get('dias_semana', [])

            if dias_semana:
                agenda_horarios = AgendaHorarioService.create_agenda_horarios_por_dias(
                    dias_semana=dias_semana,
                    hora_inicio=data['hora_inicio'],
                    hora_fin=data['hora_fin'],
                    tipo_bloque=data.get('tipo_bloque', 'disponible'),
                    is_active=data.get('is_active', True),
                )
                serializer = AgendaHorarioSerializer(agenda_horarios, many=True)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            agenda_horario = AgendaHorarioService.create_agenda_horario(
                fecha=data.get('fecha'),
                dia_semana=data.get('dia_semana'),
                hora_inicio=data['hora_inicio'],
                hora_fin=data['hora_fin'],
                tipo_bloque=data.get('tipo_bloque', 'disponible'),
                is_active=data.get('is_active', True)
            )

            serializer = AgendaHorarioSerializer(agenda_horario)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @never_cache
    def update(self, request, pk=None):
        data = request.data

        try:
            agenda_horario = AgendaHorarioService.update_agenda_horario(
                pk,
                fecha=data.get('fecha'),
                dia_semana=data.get('dia_semana'),
                hora_inicio=data.get('hora_inicio'),
                hora_fin=data.get('hora_fin'),
                tipo_bloque=data.get('tipo_bloque'),
                is_active=data.get('is_active')
            )

            serializer = AgendaHorarioSerializer(agenda_horario)
            return Response(serializer.data)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

    @never_cache
    def destroy(self, request, pk=None):
        try:
            agenda_horario_nombre = AgendaHorarioService.delete_agenda_horario(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Error al eliminar: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)