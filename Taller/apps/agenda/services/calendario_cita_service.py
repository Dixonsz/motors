from ..models.cita import Cita
from ..models.configuracion_calendario import ConfiguracionCalendario
from ..models.categoria_servicio import CategoriaServicio
from ..models.servicio import Servicio
from ...vehiculos.models.estado import Estado
from ...autenticacion.models.usuario import Usuario
from ...taller.models.cliente import Cliente
from ...vehiculos.models.vehiculo import Vehiculo


COLORES_ESTADO = {
    'Pendiente':  '#FFC300',
    'Confirmada': '#33C1FF',
    'Cancelada':  '#FF5733',
    'Completada': '#28A745',
}
COLOR_DEFAULT = '#6b7280'


class CalendarioService:

    @staticmethod
    def get_eventos_calendario():
        citas = Cita.objects.select_related('cliente', 'vehiculo', 'estado').all()
        return [CalendarioService._cita_a_evento(cita) for cita in citas]

    @staticmethod
    def _cita_a_evento(cita) -> dict:
        nombre = cita.cliente.nombre if cita.cliente else cita.vehiculo.placa
        return {
            'id':    cita.id,
            'title': f"{nombre} - {cita.estado.nombre}",
            'start': f"{cita.fecha}T{cita.hora_inicio}",
            'color': COLORES_ESTADO.get(cita.estado.nombre, COLOR_DEFAULT),
            'extendedProps': {
                'estado':   cita.estado.nombre,
                'vehiculo': cita.vehiculo.placa if cita.vehiculo else 'Sin vehículo',
                'cliente':  cita.cliente.nombre if cita.cliente else 'Sin cliente',
            },
        }

    @staticmethod
    def get_form_data() -> dict:
        return {
            'clientes':  list(Cliente.objects.values('id', 'nombre')),
            'estados':   list(Estado.objects.values('id', 'nombre')),
            'servicios': list(Servicio.objects.values('id', 'nombre')),
            'usuarios':  list(Usuario.objects.values('id', 'nombre')),
        }

    @staticmethod
    def get_vehiculos_por_cliente(cliente_id: int) -> list:
        return list(
            Vehiculo.objects.filter(cliente_id=cliente_id).values('id', 'placa')
        )
