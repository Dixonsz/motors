from ..models.cita import Cita
from ..models.cliente import Cliente
from ..models.vehiculo import Vehiculo
from ..models.estado import Estado
from ..models.servicio import Servicio
from ..models.usuario import Usuario


def get_todas_las_citas():
    return Cita.objects.select_related('cliente', 'vehiculo', 'estado').all()


def get_todos_los_clientes():
    return Cliente.objects.values('id', 'nombre')


def get_todos_los_estados():
    return Estado.objects.values('id', 'nombre')


def get_todos_los_servicios():
    return Servicio.objects.values('id', 'nombre')


def get_todos_los_usuarios():
    return Usuario.objects.values('id', 'nombre')


def get_vehiculos_por_cliente(cliente_id: int):
    return Vehiculo.objects.filter(cliente_id=cliente_id).values('id', 'placa')