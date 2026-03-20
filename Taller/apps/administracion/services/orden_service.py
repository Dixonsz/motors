from ..models.orden import Orden
from ..models.recepcion import Recepcion
from ..models.usuario import Usuario
from ..models.estado import Estado
from .utils import get_required_instance

class OrdenService:

    @staticmethod
    def _normalizar_diagnostico(diagnostico):
        if diagnostico is None:
            return ''
        return str(diagnostico).strip()

    @staticmethod
    def get_recepciones_disponibles(orden_id_excluir=None):
        recepciones_asignadas = Orden.objects.all()
        if orden_id_excluir:
            recepciones_asignadas = recepciones_asignadas.exclude(id=orden_id_excluir)

        recepciones_asignadas_ids = recepciones_asignadas.values_list('recepcion_id', flat=True)
        return Recepcion.objects.exclude(id__in=recepciones_asignadas_ids)

    @staticmethod
    def _validar_recepcion_disponible(recepcion_id, orden_id_excluir=None):
        existe_orden = Orden.objects.filter(recepcion_id=recepcion_id)
        if orden_id_excluir:
            existe_orden = existe_orden.exclude(id=orden_id_excluir)

        if existe_orden.exists():
            raise ValueError('La recepcion seleccionada ya fue asignada a otra orden de trabajo.')

    @staticmethod
    def get_all_ordenes():
        return Orden.objects.select_related('recepcion', 'usuario', 'estado').all()
    
    @staticmethod
    def get_orden_by_id(orden_id):
        try:
            return Orden.objects.select_related('recepcion', 'usuario', 'estado').get(id=orden_id)
        except Orden.DoesNotExist:
            return None
       
        
    @staticmethod
    def create_orden(recepcion_id, usuario_id, diagnostico, estado_id):
        if not recepcion_id or not usuario_id or not estado_id:
            raise ValueError('Recepcion, usuario y estado son obligatorios.')

        recepcion = get_required_instance(Recepcion, recepcion_id, 'La recepcion no existe.')
        usuario = get_required_instance(Usuario, usuario_id, 'El usuario no existe.')
        estado = get_required_instance(Estado, estado_id, 'El estado no existe.')

        OrdenService._validar_recepcion_disponible(recepcion.id)

        orden = Orden(
            recepcion=recepcion,
            usuario=usuario,
            dignostico=OrdenService._normalizar_diagnostico(diagnostico),
            estado=estado,
        )
        orden.save()
        return orden
    
    @staticmethod
    def update_orden(orden_id, recepcion_id=None, usuario_id=None, diagnostico=None, estado_id=None):
        orden = OrdenService.get_orden_by_id(orden_id)
        if not orden:
            raise ValueError("La orden no existe.")
        
        if recepcion_id:
            recepcion = get_required_instance(Recepcion, recepcion_id, 'La recepcion indicada no existe.')

            OrdenService._validar_recepcion_disponible(recepcion.id, orden_id_excluir=orden.id)
            orden.recepcion = recepcion

        if usuario_id:
            usuario = get_required_instance(Usuario, usuario_id, 'El usuario indicado no existe.')
            orden.usuario = usuario

        if diagnostico is not None:
            orden.dignostico = OrdenService._normalizar_diagnostico(diagnostico)

        if estado_id is not None and str(estado_id).strip() != '':
            estado = get_required_instance(Estado, estado_id, 'El estado indicado no existe.')
            orden.estado = estado

        orden.save()
        return orden
    
    @staticmethod
    def delete_orden(orden_id):
        orden = OrdenService.get_orden_by_id(orden_id)
        if not orden:
            raise ValueError("La orden no existe.")
        orden.delete()
        return orden
        
    

        