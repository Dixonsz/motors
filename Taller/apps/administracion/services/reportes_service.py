from decimal import Decimal

from ..models import Cliente
from ..models import Vehiculo


class ReportesService:
    @staticmethod
    def generar_reporte_clientes(fecha_inicio=None, fecha_fin=None):
        clientes = (
            Cliente.objects
            .order_by('nombre')
            .prefetch_related(
                'vehiculos__citas',
                'vehiculos__recepciones__ordenes__ordenes_servicio',
            )
        )

        filas = []
        total_vehiculos = 0
        total_citas = 0
        total_recepciones = 0
        total_ordenes = 0
        total_facturado = Decimal('0.00')
        clientes_con_actividad = 0

        for cliente in clientes:
            vehiculos = list(cliente.vehiculos.all())

            cantidad_vehiculos = len(vehiculos)
            cantidad_citas = 0
            cantidad_recepciones = 0
            cantidad_ordenes = 0
            facturado_cliente = Decimal('0.00')

            for vehiculo in vehiculos:
                for cita in vehiculo.citas.all():
                    if ReportesService._fecha_en_rango(cita.fecha, fecha_inicio, fecha_fin):
                        cantidad_citas += 1

                for recepcion in vehiculo.recepciones.all():
                    fecha_recepcion = recepcion.fecha_ingreso.date()
                    if not ReportesService._fecha_en_rango(fecha_recepcion, fecha_inicio, fecha_fin):
                        continue

                    cantidad_recepciones += 1

                    ordenes = list(recepcion.ordenes.all())
                    cantidad_ordenes += len(ordenes)

                    for orden in ordenes:
                        for detalle in orden.ordenes_servicio.all():
                            facturado_cliente += detalle.precio * detalle.cantidad

            total_vehiculos += cantidad_vehiculos
            total_citas += cantidad_citas
            total_recepciones += cantidad_recepciones
            total_ordenes += cantidad_ordenes
            total_facturado += facturado_cliente

            tiene_actividad = any([
                cantidad_vehiculos,
                cantidad_citas,
                cantidad_recepciones,
                cantidad_ordenes,
                facturado_cliente > 0,
            ])
            if tiene_actividad:
                clientes_con_actividad += 1

            filas.append({
                'id': cliente.id,
                'nombre': cliente.nombre,
                'correo': cliente.correo,
                'telefono': cliente.telefono,
                'cedula': cliente.cedula,
                'direccion': cliente.direccion,
                'vehiculos': cantidad_vehiculos,
                'citas': cantidad_citas,
                'recepciones': cantidad_recepciones,
                'ordenes': cantidad_ordenes,
                'facturado': facturado_cliente,
            })

        return {
            'filas': filas,
            'resumen': {
                'clientes_totales': len(filas),
                'clientes_con_actividad': clientes_con_actividad,
                'total_vehiculos': total_vehiculos,
                'total_citas': total_citas,
                'total_recepciones': total_recepciones,
                'total_ordenes': total_ordenes,
                'total_facturado': total_facturado,
            },
        }

    @staticmethod
    def _fecha_en_rango(fecha_obj, fecha_inicio=None, fecha_fin=None):
        if fecha_inicio and fecha_obj < fecha_inicio:
            return False
        if fecha_fin and fecha_obj > fecha_fin:
            return False
        return True
    
    @staticmethod
    def generar_reporte_vehiculos( fecha_inicio=None, fecha_fin=None):
        vehiculos = (
            Vehiculo.objects
            .order_by('marca', 'modelo')
            .select_related('cliente')
            .prefetch_related(
                'citas',
                'recepciones__ordenes__ordenes_servicio',
            )
        )

        filas = []
        for vehiculo in vehiculos:
            cantidad_citas = 0
            cantidad_recepciones = 0
            cantidad_ordenes = 0
            facturado_vehiculo = Decimal('0.00')

            for cita in vehiculo.citas.all():
                cantidad_citas += 1

            for recepcion in vehiculo.recepciones.all():
                cantidad_recepciones += 1

                ordenes = list(recepcion.ordenes.all())
                cantidad_ordenes += len(ordenes)

                for orden in ordenes:
                    for detalle in orden.ordenes_servicio.all():
                        facturado_vehiculo += detalle.precio * detalle.cantidad

            filas.append({
                'id': vehiculo.id,
                'cliente': vehiculo.cliente.nombre,
                'marca': vehiculo.marca,
                'modelo': vehiculo.modelo,
                'anio': vehiculo.anio,
                'placa': vehiculo.placa,
                'citas': cantidad_citas,
                'recepciones': cantidad_recepciones,
                'ordenes': cantidad_ordenes,
                'facturado': facturado_vehiculo,
            })

        return filas