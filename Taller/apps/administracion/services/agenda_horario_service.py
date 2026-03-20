from ..models.agenda_horario import AgendaHorario
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

class AgendaHorarioService:

    @staticmethod
    def get_dias_semana_choices():
        return AgendaHorario.DIAS_SEMANA

    @staticmethod
    def get_tipos_bloque_choices():
        return AgendaHorario.TIPOS_BLOQUE

    @staticmethod
    def _normalize_tipo_bloque(tipo_bloque):
        validos = {value for value, _ in AgendaHorario.TIPOS_BLOQUE}
        tipo = tipo_bloque or 'disponible'
        if tipo not in validos:
            raise ValueError('El tipo de bloque no es valido.')
        return tipo

    @staticmethod
    def _to_time(value):
        if value is None:
            return None

        if hasattr(value, 'hour') and hasattr(value, 'minute'):
            return value

        if isinstance(value, str):
            for fmt in ('%H:%M', '%H:%M:%S'):
                try:
                    return datetime.strptime(value, fmt).time()
                except ValueError:
                    continue

        raise ValueError('La hora debe tener formato HH:MM.')

    @staticmethod
    def _validate_selector(fecha=None, dia_semana=None):
        has_fecha = bool(fecha)
        has_dia = bool(dia_semana)

        if has_fecha and has_dia:
            raise ValueError('Define solo fecha o dia de la semana, no ambos.')

        if not has_fecha and not has_dia:
            raise ValueError('Debes indicar una fecha o dia de la semana.')

    @staticmethod
    def _validate_time_range_and_overlap_v2(fecha=None, dia_semana=None, hora_inicio=None, hora_fin=None, tipo_bloque='disponible', excluding_id=None, is_active=True):
        AgendaHorarioService._validate_selector(fecha, dia_semana)
        tipo = AgendaHorarioService._normalize_tipo_bloque(tipo_bloque)

        hora_inicio_time = AgendaHorarioService._to_time(hora_inicio)
        hora_fin_time = AgendaHorarioService._to_time(hora_fin)

        if hora_inicio_time >= hora_fin_time:
            raise ValueError('La hora de fin debe ser mayor a la hora de inicio.')

        if not is_active:
            return

        query = AgendaHorario.objects.filter(
            is_active=True,
            hora_inicio__lt=hora_fin_time,
            hora_fin__gt=hora_inicio_time,
        )

        if fecha:
            query = query.filter(fecha=fecha, tipo_bloque=tipo)
        else:
            query = query.filter(dia_semana=dia_semana, tipo_bloque=tipo)

        if excluding_id is not None:
            query = query.exclude(id=excluding_id)

        if query.exists():
            if tipo == 'bloqueado':
                raise ValueError('Ya existe un bloqueo cruzado en ese mismo dia y horario.')
            raise ValueError('El horario se cruza con otra disponibilidad activa del mismo dia.')

    @staticmethod
    def get_all_agenda_horarios():
        return AgendaHorario.objects.order_by('dia_semana', 'fecha', 'hora_inicio')
    
    @staticmethod
    def get_agenda_horario_by_id(agenda_horario_id):
        try:
            return AgendaHorario.objects.get(id=agenda_horario_id)
        except ObjectDoesNotExist:
            return None
       
        
    @staticmethod
    def create_agenda_horario(fecha=None, dia_semana=None, hora_inicio=None, hora_fin=None, tipo_bloque='disponible', is_active=True):
        tipo = AgendaHorarioService._normalize_tipo_bloque(tipo_bloque)
        AgendaHorarioService._validate_time_range_and_overlap_v2(
            fecha=fecha,
            dia_semana=dia_semana,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            tipo_bloque=tipo,
            is_active=is_active,
        )

        agenda_horario = AgendaHorario(
            fecha=fecha if fecha else None,
            dia_semana=dia_semana if dia_semana else None,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            tipo_bloque=tipo,
            is_active=is_active,
        )
        agenda_horario.save()
        return agenda_horario

    @staticmethod
    def create_agenda_horarios_por_dias(dias_semana, hora_inicio, hora_fin, tipo_bloque='disponible', is_active=True):
        if not dias_semana:
            raise ValueError('Selecciona al menos un dia de la semana.')

        horarios = []
        for dia in dias_semana:
            horario = AgendaHorarioService.create_agenda_horario(
                dia_semana=dia,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin,
                tipo_bloque=tipo_bloque,
                is_active=is_active,
            )
            horarios.append(horario)

        return horarios

    @staticmethod
    def update_agenda_horario(agenda_horario_id, fecha=None, dia_semana=None, hora_inicio=None, hora_fin=None, tipo_bloque=None, is_active=None):
        agenda_horario = AgendaHorarioService.get_agenda_horario_by_id(agenda_horario_id)
        if not agenda_horario:
            raise ValueError("El horario no existe.")

        if fecha:
            new_fecha = fecha
            new_dia_semana = None
        elif dia_semana:
            new_fecha = None
            new_dia_semana = dia_semana
        else:
            new_fecha = agenda_horario.fecha
            new_dia_semana = agenda_horario.dia_semana

        new_hora_inicio = hora_inicio if hora_inicio is not None else agenda_horario.hora_inicio
        new_hora_fin = hora_fin if hora_fin is not None else agenda_horario.hora_fin
        new_tipo_bloque = tipo_bloque if tipo_bloque is not None else agenda_horario.tipo_bloque
        new_is_active = is_active if is_active is not None else agenda_horario.is_active

        AgendaHorarioService._validate_time_range_and_overlap_v2(
            fecha=new_fecha,
            dia_semana=new_dia_semana,
            hora_inicio=new_hora_inicio,
            hora_fin=new_hora_fin,
            tipo_bloque=new_tipo_bloque,
            excluding_id=agenda_horario_id,
            is_active=new_is_active,
        )

        agenda_horario.fecha = new_fecha
        agenda_horario.dia_semana = new_dia_semana

        if hora_inicio is not None:
            agenda_horario.hora_inicio = hora_inicio

        if hora_fin is not None:
            agenda_horario.hora_fin = hora_fin

        if tipo_bloque is not None:
            agenda_horario.tipo_bloque = new_tipo_bloque

        if is_active is not None:
            agenda_horario.is_active = is_active

        agenda_horario.save()
        return agenda_horario
          
    @staticmethod
    def delete_agenda_horario(agenda_horario_id):
        agenda_horario = AgendaHorarioService.get_agenda_horario_by_id(agenda_horario_id)
        if not agenda_horario:
            raise ValueError("El horario no existe.")
        agenda_horario_nombre = agenda_horario.fecha
        agenda_horario.delete()
        return agenda_horario_nombre

        