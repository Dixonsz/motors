from ..models import Recepcion, Vehiculo, Usuario, Cita
from django.db import transaction
from .evidencia_service import EvidenciaService
from .utils import get_required_instance
from datetime import date

class RecepcionService:

    @staticmethod
    def get_all_recepciones():
        return Recepcion.objects.all()
    
    @staticmethod
    def get_recepcion_by_id(recepcion_id):
        try:
            return Recepcion.objects.get(id=recepcion_id)
        except Recepcion.DoesNotExist:
            return None
        

    @staticmethod
    def _rules_kilomatraje(vehiculo, kilometraje):
        ultimo_registro = Recepcion.objects.filter(vehiculo=vehiculo).order_by('-fecha_ingreso').first()
        if ultimo_registro:
            if kilometraje < ultimo_registro.kilometraje:
                raise ValueError(f"El kilometraje ingresado ({kilometraje}) es menor que el último registro para este vehículo. Por favor, inspeccione el vehículo."
                                 f" Último registro: {ultimo_registro.kilometraje} km. Posible error en el odómetro o manipulación del vehículo.")

            if kilometraje == ultimo_registro.kilometraje:
                raise ValueError(f"El kilometraje ingresado ({kilometraje}) es igual al último registro para este vehículo. Por favor, inspeccione el vehículo.")
                                 
    @staticmethod
    def _nivel_combustible_valido(nivel):
       if not (0 <= nivel <= 100):
           raise ValueError("El nivel de combustible debe estar entre 0 y 100.")
       

    @staticmethod
    def create_recepcion(vehiculo_id, usuario_id, observaciones, kilometraje, nivel_combustible):
        vehiculo = get_required_instance(Vehiculo, vehiculo_id, "El vehiculo no existe.")
        usuario = get_required_instance(Usuario, usuario_id, "El usuario no existe.")

        cita = Cita.objects.filter(vehiculo=vehiculo, fecha=date.today()).first()
       
            

        RecepcionService._rules_kilomatraje(vehiculo, kilometraje)
        RecepcionService._nivel_combustible_valido(nivel_combustible)

        recepcion = Recepcion.objects.create(
            vehiculo=vehiculo,
            usuario=usuario,
            cita=cita,
            observaciones=observaciones,
            kilometraje=kilometraje,
            nivel_combustible=nivel_combustible
        )
        return recepcion
    
    @staticmethod
    def delete_recepcion(recepcion_id):
        recepcion = RecepcionService.get_recepcion_by_id(recepcion_id)
        if not recepcion:
            raise ValueError("La recepcion no existe.")

        with transaction.atomic():
            evidencias = recepcion.evidencias.all()
            for evidencia in evidencias:
                EvidenciaService.delete_evidencia(evidencia.id)

            recepcion.delete()