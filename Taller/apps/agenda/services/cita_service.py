from datetime import datetime
from apps.agenda.models.cita import Cita
from apps.agenda.models.servicio import Servicio
from apps.agenda.models.configuracion_calendario import ConfiguracionCalendario
from apps.autenticacion.models.usuario import Usuario
from apps.vehiculos.models.vehiculo import Vehiculo
from apps.vehiculos.models.estado import Estado
from apps.taller.models.cliente import Cliente
from utils import get_required_instance

CITA_NO_ENCONTRADA = "Cita no encontrada."
VEHICULO_NO_ENCONTRADO = "Vehículo no encontrado."
CLIENTE_NO_ENCONTRADO = "Cliente no encontrado."
USUARIO_NO_ENCONTRADO = "Usuario no encontrado."
ESTADO_NO_ENCONTRADO = "Estado no encontrado."


class CitaService:

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
    def _get_cita_or_raise(cita_id):
        cita = CitaService.get_cita_by_id(cita_id)
        if not cita:
            raise ValueError(CITA_NO_ENCONTRADA)
        return cita

    @staticmethod
    def date_format(date_str):
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Formato de fecha inválido. Use YYYY-MM-DD.")

    @staticmethod
    def time_format(time_str):
        try:
            return datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            raise ValueError("Formato de hora inválido. Use HH:MM (24 horas).")

    @staticmethod
    def _fecha_aplica_al_bloqueo(fecha, bloqueo) -> bool:
        recurrencia = bloqueo.recurrencia
        if recurrencia == 'ninguna':
            fecha_fin = bloqueo.fecha_fin or bloqueo.fecha_inicio
            return bloqueo.fecha_inicio <= fecha <= fecha_fin
        if recurrencia == 'diaria':
            return fecha >= bloqueo.fecha_inicio
        if recurrencia == 'semanal':
            return fecha >= bloqueo.fecha_inicio and fecha.weekday() == bloqueo.fecha_inicio.weekday()
        if recurrencia == 'mensual':
            return fecha >= bloqueo.fecha_inicio and fecha.day == bloqueo.fecha_inicio.day
        return False

    @staticmethod
    def _validar_bloqueo_franja(fecha, hora_inicio, bloqueo, cita_id=None):
        if not (bloqueo.hora_inicio <= hora_inicio < bloqueo.hora_fin):
            return
        motivo = bloqueo.motivo or 'sin motivo especificado'
        if bloqueo.capacidad_maxima is None:
            raise ValueError(f"El horario {hora_inicio} del {fecha} no está disponible: {motivo}.")
        citas_en_franja = Cita.objects.filter(
            fecha=fecha,
            hora_inicio__gte=bloqueo.hora_inicio,
            hora_inicio__lt=bloqueo.hora_fin,
        )
        if cita_id:
            citas_en_franja = citas_en_franja.exclude(id=cita_id)
        if citas_en_franja.count() >= bloqueo.capacidad_maxima:
            raise ValueError(
                f"El horario {hora_inicio} del {fecha} ha alcanzado su "
                f"capacidad máxima de {bloqueo.capacidad_maxima} cita(s): {motivo}."
            )

    @staticmethod
    def _validar_disponibilidad(fecha, hora_inicio, cita_id=None):
        for bloqueo in ConfiguracionCalendario.objects.filter(activo=True):
            if not CitaService._fecha_aplica_al_bloqueo(fecha, bloqueo):
                continue
            motivo = bloqueo.motivo or 'sin motivo especificado'
            if bloqueo.tipo == 'dia_completo':
                raise ValueError(f"La fecha {fecha} no está disponible: {motivo}.")
            if bloqueo.tipo == 'franja':
                CitaService._validar_bloqueo_franja(fecha, hora_inicio, bloqueo, cita_id)

    @staticmethod
    def _resolver_entidades_create(vehiculo_id, cliente_id, usuario_id, estado_id):
        vehiculo = Vehiculo.objects.filter(id=vehiculo_id).first() if vehiculo_id else None
        cliente  = Cliente.objects.filter(id=cliente_id).first()   if cliente_id  else None
        usuario  = Usuario.objects.filter(id=usuario_id).first()
        estado   = Estado.objects.filter(id=estado_id).first()

        if vehiculo_id and not vehiculo:
            raise ValueError(VEHICULO_NO_ENCONTRADO)
        if cliente_id and not cliente:
            raise ValueError(CLIENTE_NO_ENCONTRADO)
        if not usuario:
            raise ValueError(USUARIO_NO_ENCONTRADO)
        if not estado:
            raise ValueError(ESTADO_NO_ENCONTRADO)
        if not vehiculo and not cliente:
            raise ValueError("Debe asignar al menos un cliente o un vehículo a la cita.")
        return vehiculo, cliente, usuario, estado

    @staticmethod
    def _resolver_servicios(servicios_id):
        if not servicios_id:
            return []
        servicios = list(Servicio.objects.filter(id__in=servicios_id))
        if len(servicios) != len(servicios_id):
            raise ValueError("Uno o más servicios no fueron encontrados.")
        return servicios

    @staticmethod
    def create_cita(vehiculo_id, cliente_id, servicios_id, usuario_id,
                    fecha, hora_inicio, estado_id, anotaciones=None):
        fecha       = CitaService.date_format(fecha)
        hora_inicio = CitaService.time_format(hora_inicio)
        CitaService._validar_disponibilidad(fecha, hora_inicio)

        vehiculo, cliente, usuario, estado = CitaService._resolver_entidades_create(
            vehiculo_id, cliente_id, usuario_id, estado_id
        )
        servicios = CitaService._resolver_servicios(servicios_id)

        cita = Cita(
            vehiculo=vehiculo, cliente=cliente, usuario=usuario,
            fecha=fecha, hora_inicio=hora_inicio, estado=estado,
            anotaciones=anotaciones,
        )
        cita.save()
        if servicios:
            cita.servicio.set(servicios)
        return cita

    @staticmethod
    def update_cita(cita_id, vehiculo_id=None, cliente_id=None, servicios_id=None,
                    usuario_id=None, fecha=None, hora_inicio=None,
                    estado_id=None, anotaciones=None):
        cita = CitaService._get_cita_or_raise(cita_id)

        fecha_final       = CitaService.date_format(fecha) if fecha else cita.fecha
        hora_inicio_final = CitaService.time_format(hora_inicio) if hora_inicio else cita.hora_inicio

        if fecha or hora_inicio:
            CitaService._validar_disponibilidad(fecha_final, hora_inicio_final, cita_id=cita_id)

        if vehiculo_id:
            cita.vehiculo = get_required_instance(Vehiculo, vehiculo_id, VEHICULO_NO_ENCONTRADO)
        if cliente_id:
            cita.cliente  = get_required_instance(Cliente,  cliente_id,  CLIENTE_NO_ENCONTRADO)
        if usuario_id:
            cita.usuario  = get_required_instance(Usuario,  usuario_id,  USUARIO_NO_ENCONTRADO)
        if estado_id:
            cita.estado   = get_required_instance(Estado,   estado_id,   ESTADO_NO_ENCONTRADO)
        if anotaciones is not None:
            cita.anotaciones = anotaciones

        cita.fecha       = fecha_final
        cita.hora_inicio = hora_inicio_final
        cita.save()

        servicios = CitaService._resolver_servicios(servicios_id)
        if servicios:
            cita.servicio.set(servicios)

        return cita

    @staticmethod
    def delete_cita(cita_id):
        cita = CitaService._get_cita_or_raise(cita_id)
        cita.delete()