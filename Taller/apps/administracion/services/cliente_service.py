from ..models.cliente import Cliente

class ClienteService:
    @staticmethod
    def get_all_clientes():
        return Cliente.objects.all()
    
    @staticmethod
    def get_cliente_by_id(cliente_id):
        try:
            return Cliente.objects.get(id=cliente_id)
        except Cliente.DoesNotExist:
            return None
        
    @staticmethod
    def create_cliente(nombre, correo, telefono, cedula, direccion):
        if Cliente.objects.filter(correo=correo).exists():
            raise ValueError("El correo del cliente ya existe.")
        if Cliente.objects.filter(cedula=cedula).exists():
            raise ValueError("La cédula del cliente ya existe.")
        cliente = Cliente(nombre=nombre, correo=correo, telefono=telefono, cedula=cedula, direccion=direccion)
        cliente.save()
        return cliente
    
    @staticmethod
    def update_cliente(cliente_id, nombre=None, correo=None, telefono=None, cedula=None, direccion=None):
        cliente = ClienteService.get_cliente_by_id(cliente_id)
        if not cliente:
            raise ValueError("El cliente no existe.")
        
        if correo:
            if Cliente.objects.filter(correo=correo).exclude(id=cliente_id).exists():
                raise ValueError("El correo del cliente ya existe.")
            cliente.correo = correo
        
        if cedula:
            if Cliente.objects.filter(cedula=cedula).exclude(id=cliente_id).exists():
                raise ValueError("La cédula del cliente ya existe.")
            cliente.cedula = cedula
        
        if nombre is not None:
            cliente.nombre = nombre
        if telefono is not None:
            cliente.telefono = telefono
        if direccion is not None:
            cliente.direccion = direccion
        
        cliente.save()
        return cliente
    
    @staticmethod
    def delete_cliente(cliente_id):
        cliente = ClienteService.get_cliente_by_id(cliente_id)
        if not cliente:
            raise ValueError("El cliente no existe.")
        cliente.delete()
        return cliente.nombre