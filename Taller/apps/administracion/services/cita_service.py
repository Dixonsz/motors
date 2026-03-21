from datetime import datetime, timedelta
import unicodedata

from django.db.models import Q

from ..models import Cita, Vehiculo, Servicio, Estado, Usuario
from ..models.agenda_horario import AgendaHorario
from .utils import get_required_instance

class CitaService:

    SLOT_MINUTOS = 15

    @staticmethod
    def _to_date(value):
        if value is None:
            raise ValueError("La fecha de la cita es obligatoria.")

        if hasattr(value, 'year') and hasattr(value, 'month') and hasattr(value, 'day'):
            return value

        if isinstance(value, str):
            for fmt in ('%Y-%m-%d', '%d/%m/%Y'):
                try:
                    return datetime.strptime(value, fmt).date()
                except ValueError:
                    continue

        raise ValueError("La fecha debe tener formato YYYY-MM-DD.")

    @staticmethod
    def _to_time(value):
        if value is None:
            raise ValueError("La hora de inicio es obligatoria.")

        if hasattr(value, 'hour') and hasattr(value, 'minute'):
            return value

        if isinstance(value, str):
            for fmt in ('%H:%M', '%H:%M:%S'):
                try:
                    return datetime.strptime(value, fmt).time()
                except ValueError:
                    continue

        raise ValueError("La hora debe tener formato HH:MM.")

    @staticmethod
    def _calcular_hora_fin(hora_inicio, servicio, hora_fin=None):
        hora_inicio_time = CitaService._to_time(hora_inicio)

        if servicio.duracion_estimada:
            referencia = datetime.combine(datetime.today(), hora_inicio_time)
            return (referencia + servicio.duracion_estimada).time()

        if hora_fin is None:
            raise ValueError("El servicio no tiene duración estimada. Debes indicar una hora de fin.")

        hora_fin_time = CitaService._to_time(hora_fin)
        if hora_inicio_time >= hora_fin_time:
            raise ValueError("La hora de fin debe ser mayor a la hora de inicio.")

        return hora_fin_time

    @staticmethod
    def _weekday_key(fecha):
        dias = [
            'lunes',
            'martes',
            'miercoles',
            'jueves',
            'viernes',
            'sabado',
            'domingo',
        ]
        return dias[fecha.weekday()]

    @staticmethod
    def _validate_day_not_fully_blocked(fecha):
        selector_fecha = Q(fecha=fecha)
        selector_dia = Q(dia_semana=CitaService._weekday_key(fecha), fecha__isnull=True)

        bloqueo_total = AgendaHorario.objects.filter(
            is_active=True,
            tipo_bloque='bloqueado',
            hora_inicio__lte='00:00',
            hora_fin__gte='23:59',
        ).filter(selector_fecha | selector_dia)

        if bloqueo_total.exists():
            raise ValueError("El día seleccionado está bloqueado en la agenda.")

    @staticmethod
    def _validate_time_block(fecha, hora_inicio, hora_fin, usuario_id=None, excluding_id=None):
        CitaService._validate_day_not_fully_blocked(fecha)

        if hora_inicio >= hora_fin:
            raise ValueError("La hora de fin debe ser mayor a la hora de inicio.")

        if usuario_id is not None:
            if not CitaService._is_mecanico_disponible(usuario_id, fecha, hora_inicio, hora_fin, excluding_id=excluding_id):
                raise ValueError("El mecánico seleccionado ya tiene una cita en ese rango.")
        else:
            mecanicos_activos = CitaService._get_mecanicos_activos()
            usuario_ids = [mecanico.id for mecanico in mecanicos_activos]

            citas_solapadas = Cita.objects.filter(
                fecha=fecha,
                hora_inicio__lt=hora_fin,
                hora_fin__gt=hora_inicio,
                usuario_id__in=usuario_ids,
            )
            if excluding_id is not None:
                citas_solapadas = citas_solapadas.exclude(id=excluding_id)

            mecanicos_ocupados = citas_solapadas.values_list('usuario_id', flat=True).distinct().count()
            if mecanicos_ocupados >= len(usuario_ids):
                raise ValueError("No hay mecánicos disponibles para ese rango de tiempo.")

        selector_fecha = Q(fecha=fecha)
        selector_dia = Q(dia_semana=CitaService._weekday_key(fecha), fecha__isnull=True)

        bloqueos = AgendaHorario.objects.filter(
            is_active=True,
            tipo_bloque='bloqueado',
            hora_inicio__lt=hora_fin,
            hora_fin__gt=hora_inicio,
        ).filter(selector_fecha | selector_dia)

        if bloqueos.exists():
            raise ValueError("El rango solicitado está bloqueado en la agenda.")

        disponibilidad = AgendaHorario.objects.filter(
            is_active=True,
            tipo_bloque='disponible',
            hora_inicio__lte=hora_inicio,
            hora_fin__gte=hora_fin,
        ).filter(selector_fecha | selector_dia)

        if not disponibilidad.exists():
            raise ValueError("No hay disponibilidad que cubra todo el rango de la cita.")

    @staticmethod
    def _to_datetime(fecha, hora):
        return datetime.combine(fecha, hora)

    @staticmethod
    def _overlaps(start_a, end_a, start_b, end_b):
        return start_a < end_b and end_a > start_b

    @staticmethod
    def _normalize_text(value):
        if not value:
            return ''

        decomposed = unicodedata.normalize('NFD', str(value).strip().lower())
        return ''.join(char for char in decomposed if unicodedata.category(char) != 'Mn')

    @staticmethod
    def _is_mecanico_role(rol_nombre):
        return CitaService._normalize_text(rol_nombre) == 'mecanico'

    @staticmethod
    def _get_estado_reservado():
        estados_activos = Estado.objects.filter(is_active=True)
        for estado in estados_activos:
            if CitaService._normalize_text(estado.nombre) == 'reservado':
                return estado
        raise ValueError("No existe un estado activo llamado 'Reservado'.")

    @staticmethod
    def _normalize_servicio_ids(servicio_id=None, servicio_ids=None):
        ids = []

        if servicio_ids is not None:
            if isinstance(servicio_ids, str):
                ids.extend([item.strip() for item in servicio_ids.split(',') if item.strip()])
            else:
                ids.extend([item for item in servicio_ids if item not in (None, '')])

        if servicio_id not in (None, ''):
            ids.append(servicio_id)

        ids_limpios = []
        seen = set()
        for item in ids:
            item_id = str(item).strip()
            if not item_id:
                continue
            if item_id in seen:
                continue
            seen.add(item_id)
            ids_limpios.append(item_id)

        if not ids_limpios:
            raise ValueError('Debes seleccionar al menos un servicio para crear la cita.')

        return ids_limpios

    @staticmethod
    def _get_mecanicos_activos():
        usuarios = Usuario.objects.select_related('rol').filter(is_active=True)
        mecanicos = [usuario for usuario in usuarios if usuario.rol and CitaService._is_mecanico_role(usuario.rol.nombre)]

        if not mecanicos:
            raise ValueError('No hay mecánicos activos configurados para asignar citas.')

        return sorted(mecanicos, key=lambda item: item.id)

    @staticmethod
    def _is_mecanico_disponible(usuario_id, fecha, hora_inicio, hora_fin, excluding_id=None):
        citas_mecanico = Cita.objects.filter(
            usuario_id=usuario_id,
            fecha=fecha,
            hora_inicio__lt=hora_fin,
            hora_fin__gt=hora_inicio,
        )

        if excluding_id is not None:
            citas_mecanico = citas_mecanico.exclude(id=excluding_id)

        return not citas_mecanico.exists()

    @staticmethod
    def _resolve_mecanico(fecha, hora_inicio, hora_fin, usuario_id=None, excluding_id=None):
        if usuario_id is not None:
            mecanico = get_required_instance(Usuario, usuario_id, 'El usuario mecánico no existe.')

            if not mecanico.is_active:
                raise ValueError('El usuario mecánico no está activo.')

            if not mecanico.rol or not CitaService._is_mecanico_role(mecanico.rol.nombre):
                raise ValueError('El usuario asignado no tiene rol de mecánico.')

            if not CitaService._is_mecanico_disponible(mecanico.id, fecha, hora_inicio, hora_fin, excluding_id=excluding_id):
                raise ValueError('El mecánico seleccionado ya tiene una cita en ese rango.')

            return mecanico

        mecanicos = CitaService._get_mecanicos_activos()

        for mecanico in mecanicos:
            if CitaService._is_mecanico_disponible(mecanico.id, fecha, hora_inicio, hora_fin, excluding_id=excluding_id):
                return mecanico

        raise ValueError('No hay mecánicos disponibles para ese rango de tiempo.')

    @staticmethod
    def get_disponibilidad(fecha, servicio_id, vehiculo_id=None, usuario_id=None):
        fecha_cita = CitaService._to_date(fecha)
        servicio = get_required_instance(Servicio, servicio_id, "El servicio no existe.")

        if vehiculo_id is not None:
            get_required_instance(Vehiculo, vehiculo_id, "El vehículo no existe.")

        if usuario_id is not None:
            mecanico = get_required_instance(Usuario, usuario_id, 'El usuario mecánico no existe.')
            if not mecanico.is_active:
                raise ValueError('El usuario mecánico no está activo.')
            if not mecanico.rol or not CitaService._is_mecanico_role(mecanico.rol.nombre):
                raise ValueError('El usuario asignado no tiene rol de mecánico.')
            mecanicos_activos = [mecanico]
        else:
            mecanicos_activos = CitaService._get_mecanicos_activos()

        if not servicio.duracion_estimada:
            raise ValueError("El servicio no tiene duración estimada configurada.")

        if servicio.duracion_estimada <= timedelta(0):
            raise ValueError("La duración estimada del servicio debe ser mayor a 0.")

        selector_fecha = Q(fecha=fecha_cita)
        selector_dia = Q(dia_semana=CitaService._weekday_key(fecha_cita), fecha__isnull=True)

        bloques_disponibles = AgendaHorario.objects.filter(
            is_active=True,
            tipo_bloque='disponible',
        ).filter(selector_fecha | selector_dia).order_by('hora_inicio')

        bloques_bloqueados = list(
            AgendaHorario.objects.filter(
                is_active=True,
                tipo_bloque='bloqueado',
                hora_inicio__isnull=False,
                hora_fin__isnull=False,
            ).filter(selector_fecha | selector_dia)
        )

        citas_dia = list(Cita.objects.filter(fecha=fecha_cita).only('hora_inicio', 'hora_fin', 'usuario_id'))

        slots = []
        salto = timedelta(minutes=CitaService.SLOT_MINUTOS)
        usuario_ids = {m.id for m in mecanicos_activos}

        for bloque in bloques_disponibles:
            inicio_bloque = CitaService._to_datetime(fecha_cita, bloque.hora_inicio)
            fin_bloque = CitaService._to_datetime(fecha_cita, bloque.hora_fin)
            ultimo_inicio = fin_bloque - servicio.duracion_estimada

            cursor = inicio_bloque
            while cursor <= ultimo_inicio:
                fin_slot = cursor + servicio.duracion_estimada

                ocupado_por_bloque = any(
                    CitaService._overlaps(
                        cursor,
                        fin_slot,
                        CitaService._to_datetime(fecha_cita, bloqueo.hora_inicio),
                        CitaService._to_datetime(fecha_cita, bloqueo.hora_fin),
                    )
                    for bloqueo in bloques_bloqueados
                )

                citas_solapadas = sum(
                    1
                    for cita in citas_dia
                    if cita.usuario_id in usuario_ids
                    and CitaService._overlaps(
                        cursor,
                        fin_slot,
                        CitaService._to_datetime(fecha_cita, cita.hora_inicio),
                        CitaService._to_datetime(fecha_cita, cita.hora_fin),
                    )
                )

                cupos_disponibles = len(mecanicos_activos) - citas_solapadas

                if not ocupado_por_bloque and cupos_disponibles > 0:
                    slots.append(
                        {
                            'hora_inicio': cursor.strftime('%H:%M'),
                            'hora_fin': fin_slot.strftime('%H:%M'),
                            'cupos_disponibles': cupos_disponibles,
                        }
                    )

                cursor += salto

        unique_slots = []
        seen = set()
        for slot in slots:
            key = (slot['hora_inicio'], slot['hora_fin'])
            if key not in seen:
                seen.add(key)
                unique_slots.append(slot)

        return {
            'fecha': fecha_cita.isoformat(),
            'servicio_id': servicio.id,
            'vehiculo_id': vehiculo_id,
            'usuario_id': mecanicos_activos[0].id if usuario_id is not None else None,
            'total_mecanicos_activos': len(mecanicos_activos),
            'duracion_minutos': int(servicio.duracion_estimada.total_seconds() // 60),
            'slots': unique_slots,
        }

    @staticmethod
    def get_all_citas():
        return Cita.objects.all()
    
    @staticmethod
    def get_cita_by_id(cita_id):
        try:
            return Cita.objects.get(id=cita_id)
        except Cita.DoesNotExist:
            return None
        
    @staticmethod
    def create_citas(vehiculo_id, servicio_id=None, servicio_ids=None, fecha=None, hora_inicio=None, hora_fin=None, estado_id=None, anotaciones=None, usuario_id=None):
        vehiculo = get_required_instance(Vehiculo, vehiculo_id, "El vehículo no existe.")
        if estado_id is not None:
            estado = get_required_instance(Estado, estado_id, "El estado no existe.")
        else:
            estado = CitaService._get_estado_reservado()

        servicio_ids_resueltos = CitaService._normalize_servicio_ids(servicio_id=servicio_id, servicio_ids=servicio_ids)
        fecha_cita = CitaService._to_date(fecha)
        hora_cursor = CitaService._to_time(hora_inicio)
        citas_creadas = []

        for index, servicio_id_actual in enumerate(servicio_ids_resueltos):
            servicio = get_required_instance(Servicio, servicio_id_actual, "El servicio no existe.")

            if len(servicio_ids_resueltos) > 1 and not servicio.duracion_estimada:
                raise ValueError(
                    f"El servicio '{servicio.nombre}' no tiene duración estimada y no puede encadenarse con múltiples citas."
                )

            hora_fin_cita = CitaService._calcular_hora_fin(
                hora_cursor,
                servicio,
                hora_fin=hora_fin if index == 0 else None,
            )

            CitaService._validate_time_block(
                fecha_cita,
                hora_cursor,
                hora_fin_cita,
                usuario_id=usuario_id,
            )
            usuario_asignado = CitaService._resolve_mecanico(
                fecha_cita,
                hora_cursor,
                hora_fin_cita,
                usuario_id=usuario_id,
            )

            cita = Cita(
                vehiculo=vehiculo,
                servicio=servicio,
                usuario=usuario_asignado,
                fecha=fecha_cita,
                hora_inicio=hora_cursor,
                hora_fin=hora_fin_cita,
                estado=estado,
                anotaciones=anotaciones,
            )
            cita.save()
            citas_creadas.append(cita)

            hora_cursor = hora_fin_cita

        return citas_creadas

    @staticmethod
    def create_cita(vehiculo_id, servicio_id, fecha, hora_inicio, hora_fin, estado_id=None, anotaciones=None, usuario_id=None):
        citas = CitaService.create_citas(
            vehiculo_id=vehiculo_id,
            servicio_id=servicio_id,
            fecha=fecha,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            estado_id=estado_id,
            anotaciones=anotaciones,
            usuario_id=usuario_id,
        )
        return citas[0]
    
    @staticmethod
    def update_cita(cita_id, vehiculo_id=None, servicio_id=None, fecha=None, hora_inicio=None, hora_fin=None, estado_id=None, anotaciones=None, usuario_id=None):
        cita = CitaService.get_cita_by_id(cita_id)
        if not cita:
            raise ValueError("La cita no existe.")

        if vehiculo_id:
            vehiculo = get_required_instance(Vehiculo, vehiculo_id, "El vehículo no existe.")
            cita.vehiculo = vehiculo

        if servicio_id:
            servicio = get_required_instance(Servicio, servicio_id, "El servicio no existe.")
            cita.servicio = servicio

        servicio_obj = cita.servicio

        if fecha is not None:
            cita.fecha = CitaService._to_date(fecha)

        if hora_inicio is not None:
            cita.hora_inicio = CitaService._to_time(hora_inicio)

        cita.hora_fin = CitaService._calcular_hora_fin(
            cita.hora_inicio,
            servicio_obj,
            hora_fin=hora_fin if hora_fin is not None else cita.hora_fin,
        )

        usuario_referencia_id = usuario_id if usuario_id is not None else (cita.usuario.id if cita.usuario else None)

        CitaService._validate_time_block(
            cita.fecha,
            cita.hora_inicio,
            cita.hora_fin,
            usuario_id=usuario_referencia_id,
            excluding_id=cita.id,
        )

        usuario_resuelto = CitaService._resolve_mecanico(
            cita.fecha,
            cita.hora_inicio,
            cita.hora_fin,
            usuario_id=usuario_id if usuario_id is not None else (cita.usuario.id if cita.usuario else None),
            excluding_id=cita.id,
        )
        cita.usuario = usuario_resuelto

        if estado_id is not None:
            estado = get_required_instance(Estado, estado_id, "El estado no existe.")
            cita.estado = estado

        if anotaciones is not None:
            cita.anotaciones = anotaciones

        cita.save()
        return cita

    @staticmethod
    def delete_cita(cita_id):
        cita = CitaService.get_cita_by_id(cita_id)
        if not cita:
            raise ValueError("La cita no existe.")
        cita.delete()
