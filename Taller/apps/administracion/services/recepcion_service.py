from ..models import Recepcion, Vehiculo, Usuario
from django.db import transaction
from .evidencia_service import EvidenciaService
from .utils import get_required_instance

class RecepcionService:

    @staticmethod
    def _parse_kilometraje(kilometraje):
        try:
            km = int(kilometraje)
        except (TypeError, ValueError):
            raise ValueError("El kilometraje debe ser un numero valido.")

        if km < 0:
            raise ValueError("El kilometraje no puede ser negativo.")

        return km

    @staticmethod
    def _validar_kilometraje_no_menor(vehiculo_id, kilometraje, recepcion_id_excluir=None):
        km_actual = RecepcionService._parse_kilometraje(kilometraje)

        recepciones = Recepcion.objects.filter(vehiculo_id=vehiculo_id)
        if recepcion_id_excluir:
            recepciones = recepciones.exclude(id=recepcion_id_excluir)

        ultima_recepcion = recepciones.order_by('-fecha_ingreso', '-id').first()
        if ultima_recepcion and km_actual < ultima_recepcion.kilometraje:
            raise ValueError(
                f"El kilometraje ({km_actual}) no puede ser menor al ultimo registrado "
                f"para este vehiculo ({ultima_recepcion.kilometraje})."
            )

        return km_actual

    @staticmethod
    def _parse_nivel_combustible(nivel_combustible):
        try:
            nivel = int(nivel_combustible)
        except (TypeError, ValueError):
            raise ValueError("El nivel de combustible debe ser un numero valido.")

        if nivel < 1 or nivel > 100:
            raise ValueError("El nivel de combustible debe estar entre 1 y 100.")

        return nivel

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
    def create_recepcion(vehiculo_id, usuario_id, fecha_ingreso, observaciones, kilometraje, nivel_combustible):
        km_actual = RecepcionService._validar_kilometraje_no_menor(vehiculo_id, kilometraje)
        nivel_actual = RecepcionService._parse_nivel_combustible(nivel_combustible)

        vehiculo = get_required_instance(Vehiculo, vehiculo_id, "El vehiculo no existe.")
        usuario = get_required_instance(Usuario, usuario_id, "El usuario no existe.")

        recepcion = Recepcion.objects.create(
            vehiculo=vehiculo,
            usuario=usuario,
            fecha_ingreso=fecha_ingreso,
            observaciones=observaciones,
            kilometraje=km_actual,
            nivel_combustible=nivel_actual
        )
        return recepcion
    
    @staticmethod
    def update_recepcion(recepcion_id, vehiculo_id = None, usuario_id =None, fecha_ingreso =None, observaciones = None, kilometraje = None, nivel_combustible = None):
        recepcion = RecepcionService.get_recepcion_by_id(recepcion_id)
        if not recepcion:
            raise ValueError("La recepcion no existe.")

        vehiculo_objetivo_id = vehiculo_id if vehiculo_id else recepcion.vehiculo_id
        km_objetivo = kilometraje if kilometraje is not None else recepcion.kilometraje
        km_validado = RecepcionService._validar_kilometraje_no_menor(
            vehiculo_objetivo_id,
            km_objetivo,
            recepcion_id_excluir=recepcion.id
        )
        nivel_objetivo = nivel_combustible if nivel_combustible is not None else recepcion.nivel_combustible
        nivel_validado = RecepcionService._parse_nivel_combustible(nivel_objetivo)

        if vehiculo_id:
            vehiculo = get_required_instance(Vehiculo, vehiculo_id, "El vehiculo no existe.")
            recepcion.vehiculo = vehiculo
        if usuario_id:
            usuario = get_required_instance(Usuario, usuario_id, "El usuario no existe.")
            recepcion.usuario = usuario
        if fecha_ingreso:
            recepcion.fecha_ingreso = fecha_ingreso
        if observaciones:
            recepcion.observaciones = observaciones
        recepcion.kilometraje = km_validado
        recepcion.nivel_combustible = nivel_validado
        
        recepcion.save()
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