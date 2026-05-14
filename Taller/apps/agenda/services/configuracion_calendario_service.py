from datetime import datetime
from ..models.configuracion_calendario import ConfiguracionCalendario


class ConfiguracionCalendarioService:

    @staticmethod
    def get_all_bloqueos():
        return ConfiguracionCalendario.objects.filter(activo=True).order_by('fecha_inicio')

    @staticmethod
    def get_bloqueo_by_id(bloqueo_id):
        try:
            return ConfiguracionCalendario.objects.get(id=bloqueo_id)
        except ConfiguracionCalendario.DoesNotExist:
            return None

    @staticmethod
    def create_bloqueo(tipo, fecha_inicio, recurrencia, motivo=None,
                       fecha_fin=None, hora_inicio=None, hora_fin=None,
                       capacidad_maxima=None):

        bloqueo = ConfiguracionCalendario(
            tipo             = tipo,
            fecha_inicio     = ConfiguracionCalendarioService._parse_fecha(fecha_inicio),
            fecha_fin        = ConfiguracionCalendarioService._parse_fecha(fecha_fin) if fecha_fin else None,
            hora_inicio      = ConfiguracionCalendarioService._parse_hora(hora_inicio) if hora_inicio else None,
            hora_fin         = ConfiguracionCalendarioService._parse_hora(hora_fin)    if hora_fin    else None,
            recurrencia      = recurrencia or 'ninguna',
            motivo           = motivo,
            capacidad_maxima = int(capacidad_maxima) if capacidad_maxima else None,
        )
        bloqueo.full_clean()
        bloqueo.save()
        return bloqueo

    @staticmethod
    def update_bloqueo(bloqueo_id, tipo=None, fecha_inicio=None, fecha_fin=None,
                       hora_inicio=None, hora_fin=None, recurrencia=None,
                       motivo=None, capacidad_maxima=None, activo=None):

        bloqueo = ConfiguracionCalendarioService.get_bloqueo_by_id(bloqueo_id)
        if not bloqueo:
            raise ValueError('Bloqueo no encontrado.')

        if tipo:             bloqueo.tipo         = tipo
        if fecha_inicio:     bloqueo.fecha_inicio = ConfiguracionCalendarioService._parse_fecha(fecha_inicio)
        if recurrencia:      bloqueo.recurrencia  = recurrencia
        if motivo is not None: bloqueo.motivo     = motivo
        if activo is not None: bloqueo.activo     = activo

        bloqueo.fecha_fin    = ConfiguracionCalendarioService._parse_fecha(fecha_fin) if fecha_fin else None
        bloqueo.hora_inicio  = ConfiguracionCalendarioService._parse_hora(hora_inicio) if hora_inicio else None
        bloqueo.hora_fin     = ConfiguracionCalendarioService._parse_hora(hora_fin)    if hora_fin    else None
        bloqueo.capacidad_maxima = int(capacidad_maxima) if capacidad_maxima else None

        bloqueo.full_clean()
        bloqueo.save()
        return bloqueo

    @staticmethod
    def delete_bloqueo(bloqueo_id):
        bloqueo = ConfiguracionCalendarioService.get_bloqueo_by_id(bloqueo_id)
        if not bloqueo:
            raise ValueError('Bloqueo no encontrado.')
        bloqueo.delete()

    @staticmethod
    def get_bloqueos_para_calendario():
        bloqueos = ConfiguracionCalendario.objects.filter(activo=True)
        eventos  = []

        for b in bloqueos:
            if b.tipo == 'dia_completo':
                eventos.append({
                    'id':        f"bloqueo_{b.id}",
                    'title':     b.motivo or 'Bloqueado',
                    'start':     str(b.fecha_inicio),
                    'end':       str(b.fecha_fin) if b.fecha_fin else str(b.fecha_inicio),
                    'display':   'background',
                    'color':     '#ef4444',
                    'extendedProps': {
                        'tipo':        b.tipo,
                        'recurrencia': b.recurrencia,
                        'bloqueo':     True,
                    }
                })
            else:
                eventos.append({
                    'id':        f"bloqueo_{b.id}",
                    'title':     b.motivo or 'No disponible',
                    'start':     f"{b.fecha_inicio}T{b.hora_inicio}",
                    'end':       f"{b.fecha_inicio}T{b.hora_fin}",
                    'display':   'background',
                    'color':     '#f97316',
                    'extendedProps': {
                        'tipo':             b.tipo,
                        'recurrencia':      b.recurrencia,
                        'capacidad_maxima': b.capacidad_maxima,
                        'bloqueo':          True,
                    }
                })

        return eventos

    @staticmethod
    def _parse_fecha(fecha_str):
        try:
            return datetime.strptime(fecha_str, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError('Formato de fecha inválido. Use YYYY-MM-DD.')

    @staticmethod
    def _parse_hora(hora_str):
        try:
            return datetime.strptime(hora_str, '%H:%M').time()
        except ValueError:
            raise ValueError('Formato de hora inválido. Use HH:MM.')
