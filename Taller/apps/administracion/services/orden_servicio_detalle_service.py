from ..models.orden_servicio_detalle import OrdenServicioDetalle
from ..models.orden_servicio import OrdenServicio
from ..models.servicio import Servicio
from .utils import get_required_instance


class OrdenServicioDetalleService:

    @staticmethod
    def get_detalle_by_id(detalle_id):
        try:
            return OrdenServicioDetalle.objects.get(id=detalle_id)
        except OrdenServicioDetalle.DoesNotExist:
            return None

    @staticmethod
    def get_detalles_by_orden(orden_id):
        return OrdenServicioDetalle.objects.filter(orden_id=orden_id)

    @staticmethod
    def create_detalle(orden_id, servicio_id, precio, cantidad=1, observaciones=None):

        orden    = get_required_instance(OrdenServicio, orden_id, "Orden de servicio no encontrada.")
        servicio = get_required_instance(Servicio, servicio_id, "Servicio no encontrado.")

        if OrdenServicioDetalle.objects.filter(orden=orden, servicio=servicio).exists():
            raise ValueError(f"El servicio '{servicio.nombre}' ya está agregado a esta orden.")

        detalle = OrdenServicioDetalle(
            orden=orden,
            servicio=servicio,
            precio=precio,
            cantidad=cantidad,
            observaciones=observaciones
        )
        detalle.save()
        return detalle

    @staticmethod
    def update_detalle(detalle_id, precio=None, cantidad=None, observaciones=None):

        detalle = OrdenServicioDetalleService.get_detalle_by_id(detalle_id)
        if not detalle:
            raise ValueError("Detalle no encontrado.")

        if precio is not None:
            detalle.precio = precio
        if cantidad is not None:
            detalle.cantidad = cantidad
        if observaciones is not None:
            detalle.observaciones = observaciones

        detalle.save()
        return detalle

    @staticmethod
    def delete_detalle(detalle_id):
        detalle = OrdenServicioDetalleService.get_detalle_by_id(detalle_id)
        if not detalle:
            raise ValueError("Detalle no encontrado.")
        detalle.delete()