from django.db import transaction
from ..models import InventarioHerramienta, EstadoHerramienta, Herramienta
from .utils import get_required_instance


class InventarioHerramientaService:


    @staticmethod
    def _validar_cantidad(cantidad):
        if cantidad is None:
            raise ValueError("La cantidad es obligatoria.")
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a 0.")

   
    @staticmethod
    def get_all_inventario():
        return InventarioHerramienta.objects.select_related('herramienta', 'estado')

    @staticmethod
    def get_inventario_by_id(inventario_id):
        try:
            return InventarioHerramienta.objects.select_related('herramienta', 'estado').get(id=inventario_id)
        except InventarioHerramienta.DoesNotExist:
            return None

    @staticmethod
    def get_stock_por_herramienta(herramienta_id):
        return InventarioHerramienta.objects.filter(herramienta_id=herramienta_id)

    @staticmethod
    def get_stock_por_estado(herramienta_id, estado_id):
        return InventarioHerramienta.objects.filter(
            herramienta_id=herramienta_id,
            estado_id=estado_id
        ).first()


    @staticmethod
    @transaction.atomic
    def agregar_stock(herramienta_id, cantidad, estado_nombre="Disponible"):
        herramienta = get_required_instance(Herramienta, herramienta_id, "La herramienta no existe.")
        try:
            estado = EstadoHerramienta.objects.get(nombre=estado_nombre)
        except EstadoHerramienta.DoesNotExist as exc:
            raise ValueError("El estado de herramienta no existe.") from exc

        InventarioHerramientaService._validar_cantidad(cantidad)

        inventario, _ = InventarioHerramienta.objects.get_or_create(
            herramienta=herramienta,
            estado=estado,
            defaults={'cantidad_total': 0}
        )

        inventario.cantidad_total += cantidad
        inventario.save()

        return inventario

    @staticmethod
    @transaction.atomic
    def mover_herramienta(herramienta_id, estado_origen_id, estado_destino_id, cantidad):
        InventarioHerramientaService._validar_cantidad(cantidad)

        herramienta = get_required_instance(Herramienta, herramienta_id, "La herramienta no existe.")

        origen = InventarioHerramienta.objects.select_for_update().filter(
            herramienta=herramienta,
            estado_id=estado_origen_id
        ).first()

        if not origen or origen.cantidad_total < cantidad:
            raise ValueError("No hay suficientes herramientas en el estado origen.")

        destino, _ = InventarioHerramienta.objects.get_or_create(
            herramienta=herramienta,
            estado_id=estado_destino_id,
            defaults={'cantidad_total': 0}
        )

        origen.cantidad_total -= cantidad
        destino.cantidad_total += cantidad

        origen.save()
        destino.save()

        return {
            "origen": origen,
            "destino": destino
        }

    @staticmethod
    def prestar_herramienta(herramienta_id, cantidad=1):
        estado_disponible = EstadoHerramienta.objects.get(nombre="Disponible")
        estado_en_uso = EstadoHerramienta.objects.get(nombre="En uso")

        return InventarioHerramientaService.mover_herramienta(
            herramienta_id,
            estado_disponible.id,
            estado_en_uso.id,
            cantidad
        )

    @staticmethod
    def devolver_herramienta(herramienta_id, cantidad=1):
        estado_en_uso = EstadoHerramienta.objects.get(nombre="En uso")
        estado_disponible = EstadoHerramienta.objects.get(nombre="Disponible")

        return InventarioHerramientaService.mover_herramienta(
            herramienta_id,
            estado_en_uso.id,
            estado_disponible.id,
            cantidad
        )

    @staticmethod
    def marcar_danada(herramienta_id, cantidad=1):
        estado_disponible = EstadoHerramienta.objects.get(nombre="Disponible")
        estado_danada = EstadoHerramienta.objects.get(nombre="Dañada")

        return InventarioHerramientaService.mover_herramienta(
            herramienta_id,
            estado_disponible.id,
            estado_danada.id,
            cantidad
        )

    @staticmethod
    def delete_inventario(inventario_id):
        inventario = InventarioHerramientaService.get_inventario_by_id(inventario_id)
        if not inventario:
            raise ValueError("El inventario no existe.")
        inventario.delete()