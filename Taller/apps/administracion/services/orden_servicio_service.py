from decimal import Decimal, InvalidOperation

from django.core.exceptions import ObjectDoesNotExist

from ..models.orden import Orden
from ..models.orden_servicio import OrdenServicio
from ..models.servicio import Servicio


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
        except ObjectDoesNotExist:
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
        try:
            orden = Orden.objects.get(id=orden_id)
            servicio = Servicio.objects.get(id=servicio_id)
        except (Orden.DoesNotExist, Servicio.DoesNotExist):
            raise ValueError('La orden o el servicio no existen.')

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
        try:
            detalle = OrdenServicio.objects.get(id=detalle_id)
        except ObjectDoesNotExist:
            raise ValueError('El detalle de servicio no existe.')

        if orden_id and detalle.orden_id != int(orden_id):
            raise ValueError('El detalle no pertenece a la orden seleccionada.')

        detalle.delete()
