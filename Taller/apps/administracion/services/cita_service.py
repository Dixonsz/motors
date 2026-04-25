from datetime import datetime
from ..models import Cita, Vehiculo, Servicio, Estado, Usuario, Cliente
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
    def create_cita(vehiculo_id, cliente_id, servicios_id, usuario_id, fecha, hora_inicio, estado_id, anotaciones=None):

        fecha = CitaService.date_format(fecha)
        hora_inicio = CitaService.time_format(hora_inicio)

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
            servicios = Servicio.objects.filter(id__in=servicios_id)
            if len(servicios) != len(servicios_id):
                raise ValueError("Uno o más servicios no fueron encontrados.")

        cita = Cita(
            vehiculo=vehiculo,
            cliente=cliente,
            usuario=usuario,
            fecha=fecha,
            hora_inicio=hora_inicio,
            estado=estado,
            anotaciones=anotaciones
        )
        cita.save()

        if servicios:
            cita.servicios.set(servicios)

        return cita


    @staticmethod
    def update_cita(cita_id, vehiculo_id=None, cliente_id=None, servicios_id=None, usuario_id=None, fecha=None, hora_inicio=None, estado_id=None, anotaciones=None):

        cita = CitaService.get_cita_by_id(cita_id)
        if not cita:
            raise ValueError("Cita no encontrada.")

        if vehiculo_id:
            cita.vehiculo = get_required_instance(Vehiculo, vehiculo_id, "Vehículo no encontrado.")
        if cliente_id:
            cita.cliente = get_required_instance(Cliente, cliente_id, "Cliente no encontrado.")
        if usuario_id:
            cita.usuario = get_required_instance(Usuario, usuario_id, "Usuario no encontrado.")
        if fecha:
            cita.fecha = CitaService.date_format(fecha)
        if hora_inicio:
            cita.hora_inicio = CitaService.time_format(hora_inicio)
        if estado_id:
            cita.estado = get_required_instance(Estado, estado_id, "Estado no encontrado.")
        if anotaciones is not None:
            cita.anotaciones = anotaciones

        cita.save()

        if servicios_id:
            servicios = Servicio.objects.filter(id__in=servicios_id)
            if len(servicios) != len(servicios_id):
                raise ValueError("Uno o más servicios no fueron encontrados.")
            cita.servicios.set(servicios)
        return cita

    @staticmethod
    def delete_cita(cita_id):
        cita = CitaService.get_cita_by_id(cita_id)
        if not cita:
            raise ValueError("Cita no encontrada.")
        cita.delete()   


    

                    
       

            
       

  

  


 