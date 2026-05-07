from ..models.usuario import Usuario
from ..models.rol import Rol
from .utils import get_required_instance


class UsuarioService:

    @staticmethod
    def get_all_usuarios():
        return Usuario.objects.all()

    @staticmethod
    def get_usuario_by_id(usuario_id):
        try:
            return Usuario.objects.get(id=usuario_id)
        except Usuario.DoesNotExist:
            return None

    @staticmethod
    def create_usuario(username,email, password, nombre, apellido, cedula, telefono, direccion, rol_id, especialidad=None):
        
        if Usuario.objects.filter(username=username).exists():
            raise ValueError(f"Ya existe un usuario con el username '{username}'.")
        
        if Usuario.objects.filter(email=email).exists():
            raise ValueError(f"Ya existe un usuario con el email '{email}'.")
        
        if Usuario.objects.filter(cedula=cedula).exists():
            raise ValueError(f"Ya existe un usuario con la cédula '{cedula}'.")

        rol = get_required_instance(Rol, rol_id, "Rol no encontrado.")

        usuario = Usuario(
            username=username,
            email=email,
            nombre=nombre,
            apellido=apellido,
            cedula=cedula,
            telefono=telefono,
            direccion=direccion,
            especialidad=especialidad,
            rol=rol
        )
        usuario.set_password(password) 
        usuario.save()
        return usuario

    @staticmethod
    def update_usuario(usuario_id,username, email, nombre=None, apellido=None,cedula=None,telefono=None, direccion=None, especialidad=None, rol_id=None):
        usuario = UsuarioService.get_usuario_by_id(usuario_id)
        if not usuario:
            raise ValueError("Usuario no encontrado.")

        if username != usuario.username:
            if Usuario.objects.filter(username=username).exists():
                raise ValueError(f"Ya existe un usuario con el username '{username}'.")
            usuario.username = username

        if email != usuario.email:
            if Usuario.objects.filter(email=email).exists():
                raise ValueError(f"Ya existe un usuario con el email '{email}'.")
            usuario.email = email
        if cedula and cedula != usuario.cedula:
            if Usuario.objects.filter(cedula=cedula).exists():
                raise ValueError(f"Ya existe un usuario con la cédula '{cedula}'.")
            usuario.cedula = cedula

        if nombre is not None:
            usuario.nombre = nombre
        if apellido is not None:
            usuario.apellido = apellido
        if cedula is not None:
            usuario.cedula = cedula
        if telefono is not None:
            usuario.telefono = telefono
        if direccion is not None:
            usuario.direccion = direccion
        if especialidad is not None:
            usuario.especialidad = especialidad
        if rol_id:
            usuario.rol = get_required_instance(Rol, rol_id, "Rol no encontrado.")

        usuario.save()
        return usuario

    @staticmethod
    def cambiar_password(usuario_id, password, new_password):
        usuario = UsuarioService.get_usuario_by_id(usuario_id)
        if not usuario:
            raise ValueError("Usuario no encontrado.")

        if not usuario.check_password(password):
            raise ValueError("La contraseña actual es incorrecta.")

        usuario.set_password(new_password)
        usuario.save()
        return usuario

    @staticmethod
    def activar_desactivar_usuario(usuario_id):
        usuario = UsuarioService.get_usuario_by_id(usuario_id)
        if not usuario:
            raise ValueError("Usuario no encontrado.")

        usuario.estado = not usuario.estado
        usuario.is_active = usuario.estado  
        usuario.save()
        return usuario
