from datetime import datetime
from ..models import Cita, Vehiculo, Servicio, Estado, Usuario, Cliente
from ..models.configuracion_calendario import ConfiguracionCalendario
from .utils import get_required_instance

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
            if bloqueo.tipo == 'dia_completo':
                fecha_fin = bloqueo.fecha_fin or bloqueo.fecha_inicio
                return bloqueo.fecha_inicio <= fecha <= fecha_fin
            else:  # franja
                return fecha == bloqueo.fecha_inicio
 
        elif recurrencia == 'diaria':
            return fecha >= bloqueo.fecha_inicio
 
        elif recurrencia == 'semanal':
            return (
                fecha >= bloqueo.fecha_inicio
                and fecha.weekday() == bloqueo.fecha_inicio.weekday()
            )
 
        elif recurrencia == 'mensual':
            return (
                fecha >= bloqueo.fecha_inicio
                and fecha.day == bloqueo.fecha_inicio.day
            )
 
        return False
    
    @staticmethod
    def _validar_disponibilidad(fecha, hora_inicio, cita_id=None):
      
        bloqueos_activos = ConfiguracionCalendario.objects.filter(activo=True)
 
        for bloqueo in bloqueos_activos:
 
            if not CitaService._fecha_aplica_al_bloqueo(fecha, bloqueo):
                continue 
 
            motivo = bloqueo.motivo or 'sin motivo especificado'
 
            if bloqueo.tipo == 'dia_completo':
                raise ValueError(
                    f"La fecha {fecha} no está disponible: {motivo}."
                )
 
            elif bloqueo.tipo == 'franja':
                if not (bloqueo.hora_inicio <= hora_inicio < bloqueo.hora_fin):
                    continue  
 
                if bloqueo.capacidad_maxima is None:
                    raise ValueError(
                        f"El horario {hora_inicio} del {fecha} no está disponible: "
                        f"{motivo}."
                    )
 
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
                        f"capacidad máxima de {bloqueo.capacidad_maxima} cita(s): "
                        f"{motivo}."
                    )

    @staticmethod
    def create_cita(vehiculo_id, cliente_id, servicios_id, usuario_id,
                    fecha, hora_inicio, estado_id, anotaciones=None):
 
        fecha       = CitaService.date_format(fecha)
        hora_inicio = CitaService.time_format(hora_inicio)
 
        # Validar contra bloqueos ANTES de tocar la BD
        CitaService._validar_disponibilidad(fecha, hora_inicio)
 
        vehiculo = Vehiculo.objects.filter(id=vehiculo_id).first() if vehiculo_id else None
        cliente  = Cliente.objects.filter(id=cliente_id).first()   if cliente_id  else None
        usuario  = Usuario.objects.filter(id=usuario_id).first()
        estado   = Estado.objects.filter(id=estado_id).first()
 
        if vehiculo_id and not vehiculo:
            raise ValueError("Vehículo no encontrado.")
        if cliente_id and not cliente:
            raise ValueError("Cliente no encontrado.")
        if not usuario:
            raise ValueError("Usuario no encontrado.")
        if not estado:
            raise ValueError("Estado no encontrado.")
        if not vehiculo and not cliente:
            raise ValueError("Debe asignar al menos un cliente o un vehículo a la cita.")
 
        servicios = []
        if servicios_id:
            servicios = list(Servicio.objects.filter(id__in=servicios_id))
            if len(servicios) != len(servicios_id):
                raise ValueError("Uno o más servicios no fueron encontrados.")
 
        cita = Cita(
            vehiculo    = vehiculo,
            cliente     = cliente,
            usuario     = usuario,
            fecha       = fecha,
            hora_inicio = hora_inicio,
            estado      = estado,
            anotaciones = anotaciones,
        )
        cita.save()
 
        if servicios:
            cita.servicio.set(servicios)
 
        return cita
 
    @staticmethod
    def update_cita(cita_id, vehiculo_id=None, cliente_id=None, servicios_id=None,
                    usuario_id=None, fecha=None, hora_inicio=None,
                    estado_id=None, anotaciones=None):
 
        cita = CitaService.get_cita_by_id(cita_id)
        if not cita:
            raise ValueError("Cita no encontrada.")
 
        fecha_final       = CitaService.date_format(fecha) if fecha else cita.fecha
        hora_inicio_final = CitaService.time_format(hora_inicio) if hora_inicio else cita.hora_inicio
 
        if fecha or hora_inicio:
            CitaService._validar_disponibilidad(fecha_final, hora_inicio_final, cita_id=cita_id)
 
        if vehiculo_id:
            cita.vehiculo = get_required_instance(Vehiculo, vehiculo_id, "Vehículo no encontrado.")
        if cliente_id:
            cita.cliente  = get_required_instance(Cliente,  cliente_id,  "Cliente no encontrado.")
        if usuario_id:
            cita.usuario  = get_required_instance(Usuario,  usuario_id,  "Usuario no encontrado.")
 
        cita.fecha       = fecha_final
        cita.hora_inicio = hora_inicio_final
 
        if estado_id:
            cita.estado = get_required_instance(Estado, estado_id, "Estado no encontrado.")
        if anotaciones is not None:
            cita.anotaciones = anotaciones
 
        cita.save()
 
        if servicios_id:
            servicios = Servicio.objects.filter(id__in=servicios_id)
            if len(servicios) != len(servicios_id):
                raise ValueError("Uno o más servicios no fueron encontrados.")
            cita.servicio.set(servicios)
 
        return cita
 
    @staticmethod
    def delete_cita(cita_id):
        cita = CitaService.get_cita_by_id(cita_id)
        if not cita:
            raise ValueError("Cita no encontrada.")
        cita.delete()


    

                    
       

            
       

  

  


 
