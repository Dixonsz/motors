from ..models import Usuario, Rol
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
    def create_usuario(nombre,apellido, telefono,correo, rol_id, password):
        if Usuario.objects.filter(email=correo).exists():
            raise ValueError("El correo ya está registrado.")

        rol = get_required_instance(Rol, rol_id, "El rol no existe.")

        usuario = Usuario(nombre=nombre,
                          apellido=apellido,
                          email=correo,
                          telefono=telefono,
                          rol = rol,
                          username=correo)
        usuario.set_password(password)
        usuario.save()
        return usuario
    
    @staticmethod
    def update_usuario(usuario_id, nombre=None, apellido=None, telefono=None, correo=None, rol_id=None, password=None):
        usuario = UsuarioService.get_usuario_by_id(usuario_id)
        if not usuario:
            raise ValueError("El usuario no existe.")
        
        if nombre:
            usuario.nombre = nombre
        if apellido:
            usuario.apellido = apellido
        if telefono:
            usuario.telefono = telefono
        if correo:
            if Usuario.objects.filter(email=correo).exclude(id=usuario_id).exists():
                raise ValueError("El correo ya está registrado.")
            usuario.email = correo
        if rol_id:
            rol = get_required_instance(Rol, rol_id, "El rol no existe.")
            usuario.rol = rol
        if password:
            usuario.set_password(password)
        
        usuario.save()
        return usuario
    
    @staticmethod
    def delete_usuario(usuario_id):
        usuario = UsuarioService.get_usuario_by_id(usuario_id)
        if not usuario:
            raise ValueError("El usuario no existe.")
        usuario.delete()
