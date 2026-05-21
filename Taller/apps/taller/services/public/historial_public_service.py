from apps.vehiculos.models.vehiculo import Vehiculo
from apps.taller.models.cliente import Cliente


class HistorialPublicService:

    @staticmethod
    def obtener_historial_por_placa(placa):

        try:
            vehiculo = Vehiculo.objects.select_related(
                'marca',
                'modelo',
                'combustible',
            ).get(placa__iexact=placa)
        except Vehiculo.DoesNotExist:
            raise ValueError("No se encontró ningún vehículo con esa placa.")

        ordenes = HistorialPublicService._get_ordenes(vehiculo)
        return {
            'vehiculo': vehiculo,
            'ordenes': ordenes,
        }

    @staticmethod
    def obtener_historial_por_cedula(cedula):

        try:
            cliente = Cliente.objects.get(cedula=cedula)
        except Cliente.DoesNotExist:
            raise ValueError("No se encontró ningún cliente con esa cédula.")

        vehiculos = Vehiculo.objects.select_related(
            'marca',
            'modelo',
            'combustible',
        ).filter(cliente=cliente)

        resultado = []
        for vehiculo in vehiculos:
            ordenes = HistorialPublicService._get_ordenes(vehiculo)
            resultado.append({
                'vehiculo': vehiculo,
                'ordenes': ordenes,
            })

        return {
            'cliente': cliente,
            'vehiculos': resultado,
        }

    @staticmethod
    def _get_ordenes(vehiculo):
    
        from apps.taller.models.orden_servicio import OrdenServicio

        return OrdenServicio.objects.select_related(
            'estado',
            'recepcion',
        ).prefetch_related(
            'ordenes_detalle__servicio',
            'recepcion__evidencias',
        ).filter(
            recepcion__vehiculo=vehiculo
        ).order_by('-fecha_creacion')