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
    def create_cita(vehiculo_id, cliente_id, servicio_id, usuario_id, fecha, hora_inicio, estado_id, anotaciones=None):

        fecha = CitaService.date_format(fecha)
        hora_inicio = CitaService.time_format(hora_inicio)

        vehiculo = Vehiculo.objects.filter(id=vehiculo_id).first() if vehiculo_id else None
        cliente = Cliente.objects.filter(id=cliente_id).first() if cliente_id else None
        servicio = Servicio.objects.filter(id=servicio_id).first() if servicio_id else None
       
        usuario = Usuario.objects.filter(id=usuario_id).first()
        estado = Estado.objects.filter(id=estado_id).first()

       
        if vehiculo_id and not vehiculo:
            raise ValueError("Vehículo no encontrado.")
        if cliente_id and not cliente:
            raise ValueError("Cliente no encontrado.")
        if servicio_id and not servicio:
            raise ValueError("Servicio no encontrado.")
        

        if not vehiculo and not cliente:
            raise ValueError("Debe asignar al menos un cliente o un vehículo a la cita.")

        cita = Cita(
            vehiculo=vehiculo,
            cliente=cliente,
            servicio=servicio,
            usuario= usuario,
            fecha=fecha.date_format(),
            hora_inicio=hora_inicio.time_format(),
            estado=estado,
            anotaciones=anotaciones
        )
        cita.save()
        return cita


    @staticmethod
    def update_cita(cita_id, vehiculo_id=None, cliente_id=None, servicio_id=None, usuario_id=None, fecha=None, hora_inicio=None, estado_id=None, anotaciones=None):
      
        cita = CitaService.get_cita_by_id(cita_id)
        if not cita:
            raise ValueError("Cita no encontrada.")
        
        if vehiculo_id:
            vehiculo = get_required_instance(Vehiculo, vehiculo_id, "Vehículo no encontrado.")
            cita.vehiculo = vehiculo
        if cliente_id:
            cliente = get_required_instance(Cliente, cliente_id, "Cliente no encontrado.")
            cita.cliente = cliente
        if servicio_id:
            servicio = get_required_instance(Servicio, servicio_id, "Servicio no encontrado.")
            cita.servicio = servicio
        if usuario_id:
            usuario = get_required_instance(Usuario, usuario_id, "Usuario no encontrado.")
            cita.usuario = usuario
        if fecha:
            cita.fecha = CitaService.date_format(fecha)
        if hora_inicio:
            cita.hora_inicio = CitaService.time_format(hora_inicio)
        if estado_id:
            estado = get_required_instance(Estado, estado_id, "Estado no encontrado.")
            cita.estado = estado
        if anotaciones is not None:
            cita.anotaciones = anotaciones

        cita.save()
        return cita     

    @staticmethod
    def delete_cita(cita_id):
        cita = CitaService.get_cita_by_id(cita_id)
        if not cita:
            raise ValueError("Cita no encontrada.")
        cita.delete()   


    

                    
       

            
       

  

  


 