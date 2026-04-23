from datetime import datetime, timedelta
import unicodedata

from django.db.models import Q

from ..models import Cita, Vehiculo, Servicio, Estado, Usuario

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
        
    def date_format(self, date_str):
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Formato de fecha inválido. Use YYYY-MM-DD.")
    
    @staticmethod
    def create_cita(vehiculo_id, cliente_id, servicio_id, usuario_id, fecha, hora_inicio, hora_fin, estado_id, anotaciones=None):
       
       if Usuario.objects.filter(id=usuario_id).exists():
            usuario = Usuario.objects.get(id=usuario_id)


       cita = Cita(
            vehiculo = vehiculo,
            cliente = cliente,
            servicio = servicio,
            usuario = usuario ,
            fecha=fecha,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            estado_id=estado_id,
            anotaciones=anotaciones
        )
        cita.save()
        return cita


  

  


 