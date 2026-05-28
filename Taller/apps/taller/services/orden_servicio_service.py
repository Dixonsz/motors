
from datetime import date
from ..models.orden_servicio import OrdenServicio
from ..models.recepcion import Recepcion
from ...autenticacion.models.usuario import Usuario
from ...vehiculos.models.estado import Estado
from utils import get_required_instance

ORDEN_SERVICIO_ERROR_MESSAGES = "Orden de servicio no encontrada."


class OrdenServicioService:

    @staticmethod
    def is_orden_cerrada(orden):
        if not orden or not orden.estado_id:
            return False
        return orden.estado.nombre.strip().lower() == "completado"

    @staticmethod
    def get_orden_servicio_by_id(orden_servicio_id):
        try:
            return OrdenServicio.objects.get(id=orden_servicio_id)
        except OrdenServicio.DoesNotExist:
            return None
        
    @staticmethod
    def get_all_ordenes_servicio():
         return OrdenServicio.objects.order_by('-fecha_creacion', '-id')

    @staticmethod
    def get_ordenes_filtradas(placa=None, cliente=None, fecha=None, usuario_id=None, estado_id=None):
        ordenes = OrdenServicio.objects.all()

        if placa:
            ordenes = ordenes.filter(recepcion__vehiculo__placa__icontains=placa.strip())
        if cliente:
            ordenes = ordenes.filter(recepcion__vehiculo__cliente__nombre__icontains=cliente.strip())
        if fecha:
            ordenes = ordenes.filter(fecha_creacion__date=fecha)
        if usuario_id:
            ordenes = ordenes.filter(usuario_id=usuario_id)
        if estado_id:
            ordenes = ordenes.filter(estado_id=estado_id)

        return ordenes.order_by('-fecha_creacion', '-id')
    

    @staticmethod
    def cerrar_orden_servicio(orden_servicio_id):

        orden = OrdenServicioService.get_orden_servicio_by_id(orden_servicio_id)
        if not orden:
            raise ValueError(ORDEN_SERVICIO_ERROR_MESSAGES)
        
        if not orden.ordenes_detalle.exists():
            raise ValueError("No se puede cerrar la orden de servicio sin detalles.")
        
        if OrdenServicioService.is_orden_cerrada(orden):
            raise ValueError("La orden de servicio ya está cerrada.")

        estado_completado = Estado.objects.filter(nombre__iexact="Completado").first()
        if not estado_completado:
            raise ValueError("Estado 'Completado' no encontrado.")
        
        orden.estado = estado_completado
        orden.fecha_entrega = date.today()
        orden.save()
        return orden
    


    @staticmethod
    def create_orden_servicio(recepcion_id, usuario_id, estado_id, diagnostico=None, observaciones=None):

        recepcion = get_required_instance(Recepcion, recepcion_id, "Recepción no encontrada.")
        usuario = get_required_instance(Usuario, usuario_id, "Usuario no encontrado.")
        estado = get_required_instance(Estado, estado_id, "Estado no encontrado.")

        if OrdenServicio.objects.filter(recepcion=recepcion).exists():
            raise ValueError("Ya existe una orden de servicio para esta recepción.") 

        if OrdenServicio.objects.filter(recepcion=recepcion, estado__nombre__iexact="Completado").exists():
            raise ValueError("La recepción tiene una orden de servicio cerrada.")


        orden_servicio = OrdenServicio(
            recepcion=recepcion,
            usuario=usuario,
            diagnostico=diagnostico,
            estado=estado,
            observaciones=observaciones
        )
        orden_servicio.save()

        return orden_servicio

    @staticmethod
    def update_orden_servicio(orden_servicio_id, recepcion_id=None, usuario_id=None, estado_id=None, diagnostico=None, observaciones=None):

        orden_servicio = OrdenServicioService.get_orden_servicio_by_id(orden_servicio_id)
        if not orden_servicio:
            raise ValueError(ORDEN_SERVICIO_ERROR_MESSAGES)

        if OrdenServicioService.is_orden_cerrada(orden_servicio):
            raise ValueError("La orden de servicio está cerrada y no se puede modificar.")
        
        if recepcion_id:
            orden_servicio.recepcion = get_required_instance(Recepcion, recepcion_id, "Recepción no encontrada.")
        if usuario_id:
            orden_servicio.usuario = get_required_instance(Usuario, usuario_id, "Usuario no encontrado.")
        if estado_id:
            orden_servicio.estado = get_required_instance(Estado, estado_id, "Estado no encontrado.")
        if diagnostico is not None:
            orden_servicio.diagnostico = diagnostico
        if observaciones is not None:
            orden_servicio.observaciones = observaciones

        orden_servicio.save()

        return orden_servicio
    

    
    @staticmethod
    def delete_orden_servicio(orden_servicio_id):
        orden_servicio = OrdenServicioService.get_orden_servicio_by_id(orden_servicio_id)
        if not orden_servicio:
            raise ValueError(ORDEN_SERVICIO_ERROR_MESSAGES)
        if OrdenServicioService.is_orden_cerrada(orden_servicio):
            raise ValueError("La orden de servicio está cerrada y no se puede eliminar.")
        orden_servicio.delete()
       
