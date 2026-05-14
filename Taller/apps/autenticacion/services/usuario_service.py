from ..models.usuario import Usuario
from ..models.rol import Rol
from  utils import get_required_instance

USUARIO_NO_ENCONTRADO = "Usuario no encontrado."
ROL_NO_ENCONTRADO = "Rol no encontrado."


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
    def _get_usuario_or_raise(usuario_id):
        usuario = UsuarioService.get_usuario_by_id(usuario_id)
        if not usuario:
            raise ValueError(USUARIO_NO_ENCONTRADO)
        return usuario

    @staticmethod
    def create_usuario(username, email, password, nombre, apellido, cedula, telefono, direccion, rol_id, especialidad=None):
        if Usuario.objects.filter(username=username).exists():
            raise ValueError(f"Ya existe un usuario con el username '{username}'.")
        if Usuario.objects.filter(email=email).exists():
            raise ValueError(f"Ya existe un usuario con el email '{email}'.")
        if Usuario.objects.filter(cedula=cedula).exists():
            raise ValueError(f"Ya existe un usuario con la cédula '{cedula}'.")

        rol = get_required_instance(Rol, rol_id, ROL_NO_ENCONTRADO)
        usuario = Usuario(
            username=username, email=email, nombre=nombre,
            apellido=apellido, cedula=cedula, telefono=telefono,
            direccion=direccion, especialidad=especialidad, rol=rol
        )
        usuario.set_password(password)
        usuario.save()
        return usuario

    @staticmethod
    def _validar_campos_unicos(usuario, username, email, cedula):
        if username != usuario.username and Usuario.objects.filter(username=username).exists():
            raise ValueError(f"Ya existe un usuario con el username '{username}'.")
        if email != usuario.email and Usuario.objects.filter(email=email).exists():
            raise ValueError(f"Ya existe un usuario con el email '{email}'.")
        if cedula and cedula != usuario.cedula and Usuario.objects.filter(cedula=cedula).exists():
            raise ValueError(f"Ya existe un usuario con la cédula '{cedula}'.")

    @staticmethod
    def _aplicar_cambios(usuario, username, email, nombre, apellido, cedula, telefono, direccion, especialidad, rol_id):
        usuario.username = username
        usuario.email = email
        campos = {"nombre": nombre, "apellido": apellido, "cedula": cedula,
                  "telefono": telefono, "direccion": direccion, "especialidad": especialidad}
        for campo, valor in campos.items():
            if valor is not None:
                setattr(usuario, campo, valor)
        if rol_id:
            usuario.rol = get_required_instance(Rol, rol_id, ROL_NO_ENCONTRADO)

    @staticmethod
    def update_usuario(usuario_id, username, email, nombre=None, apellido=None, cedula=None,
                       telefono=None, direccion=None, especialidad=None, rol_id=None):
        usuario = UsuarioService._get_usuario_or_raise(usuario_id)
        UsuarioService._validar_campos_unicos(usuario, username, email, cedula)
        UsuarioService._aplicar_cambios(usuario, username, email, nombre, apellido, cedula, telefono, direccion, especialidad, rol_id)
        usuario.save()
        return usuario

    @staticmethod
    def cambiar_password(usuario_id, password, new_password):
        usuario = UsuarioService._get_usuario_or_raise(usuario_id)
        if not usuario.check_password(password):
            raise ValueError("La contraseña actual es incorrecta.")
        usuario.set_password(new_password)
        usuario.save()
        return usuario

    @staticmethod
    def activar_desactivar_usuario(usuario_id):
        usuario = UsuarioService._get_usuario_or_raise(usuario_id)
        usuario.estado = not usuario.estado
        usuario.is_active = usuario.estado
        usuario.save()
        return usuario