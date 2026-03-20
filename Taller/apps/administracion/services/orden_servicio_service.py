from decimal import Decimal, InvalidOperation

from ..models.orden import Orden
from ..models.orden_servicio import OrdenServicio
from ..models.servicio import Servicio
from .utils import get_required_instance


class OrdenServicioService:

    @staticmethod
    def _parse_cantidad(cantidad):
        try:
            cantidad_valor = int(cantidad)
        except (TypeError, ValueError):
            raise ValueError('La cantidad debe ser un numero entero valido.')

        if cantidad_valor <= 0:
            raise ValueError('La cantidad debe ser mayor a cero.')

        return cantidad_valor

    @staticmethod
    def _parse_precio(precio, precio_base):
        if precio in (None, ''):
            return precio_base

        try:
            precio_valor = Decimal(str(precio))
        except (InvalidOperation, ValueError):
            raise ValueError('El precio debe ser un numero valido.')

        if precio_valor < 0:
            raise ValueError('El precio no puede ser negativo.')

        return precio_valor

    @staticmethod
    def get_detalles_by_orden(orden_id):
        return OrdenServicio.objects.select_related('servicio').filter(orden_id=orden_id).order_by('-id')

    @staticmethod
    def get_detalle_by_id(detalle_id):
        try:
            return OrdenServicio.objects.select_related('servicio', 'orden').get(id=detalle_id)
        except OrdenServicio.DoesNotExist:
            return None

    @staticmethod
    def get_total_by_orden(orden_id):
        detalles = OrdenServicioService.get_detalles_by_orden(orden_id)
        total = Decimal('0.00')
        for detalle in detalles:
            total += detalle.precio * detalle.cantidad
        return total

    @staticmethod
    def create_detalle(orden_id, servicio_id, cantidad, precio=None, observaciones=''):
        orden = get_required_instance(Orden, orden_id, 'La orden no existe.')
        servicio = get_required_instance(Servicio, servicio_id, 'El servicio no existe.')

        detalle = OrdenServicio(
            orden=orden,
            servicio=servicio,
            cantidad=OrdenServicioService._parse_cantidad(cantidad),
            precio=OrdenServicioService._parse_precio(precio, servicio.precio_base),
            observaciones=(observaciones or '').strip() or None,
        )
        detalle.save()
        return detalle

    @staticmethod
    def update_detalle(detalle_id, cantidad=None, precio=None, observaciones=None):
        detalle = OrdenServicioService.get_detalle_by_id(detalle_id)
        if not detalle:
            raise ValueError('El detalle de servicio no existe.')

        if cantidad is not None:
            detalle.cantidad = OrdenServicioService._parse_cantidad(cantidad)

        if precio is not None:
            detalle.precio = OrdenServicioService._parse_precio(precio, detalle.servicio.precio_base)

        if observaciones is not None:
            detalle.observaciones = (observaciones or '').strip() or None

        detalle.save()
        return detalle

    @staticmethod
    def delete_detalle(detalle_id, orden_id=None):
        detalle = get_required_instance(OrdenServicio, detalle_id, 'El detalle de servicio no existe.')

        if orden_id:
            try:
                orden_id_value = int(orden_id)
            except (TypeError, ValueError):
                raise ValueError('El id de la orden no es valido.')

            if detalle.orden_id != orden_id_value:
                raise ValueError('El detalle no pertenece a la orden seleccionada.')

        detalle.delete()

