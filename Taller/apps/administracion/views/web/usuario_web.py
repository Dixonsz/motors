from django.contrib import messages
from django.shortcuts import redirect, render
from ...services.usuario_service import UsuarioService
from ...services.rol_service import RolService

def usuario_lista(request):
    usuarios = UsuarioService.get_all_usuarios()

    return render(request, 'usuarios/usuarios_lista.html', {'usuarios': usuarios})

def usuario_create(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        telefono = request.POST.get('telefono')
        correo = request.POST.get('correo')
        rol_id = request.POST.get('rol_id')
        password = request.POST.get('password')

        try:
            UsuarioService.create_usuario(nombre, apellido, telefono, correo, rol_id, password)
            messages.success(request, 'Usuario creado correctamente.')
            return redirect('usuarios_lista')
        except ValueError as exc:
            messages.error(request, str(exc))
    
    roles = RolService.get_all_roles()
    return render(request, 'usuarios/usuarios_crear.html', {'roles': roles})    


def usuario_editar(request, usuario_id):
    usuario = UsuarioService.get_usuario_by_id(usuario_id)
    roles = RolService.get_all_roles()
    if not usuario:
        messages.error(request, 'El usuario no existe.')
        return redirect('usuarios_lista')

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        telefono = request.POST.get('telefono')
        correo = request.POST.get('correo')
        rol_id = request.POST.get('rol_id')
        password = request.POST.get('password')

        try:
            UsuarioService.update_usuario(usuario_id, nombre, apellido, telefono, correo, rol_id, password)
            messages.success(request, 'Usuario actualizado correctamente.')
            return redirect('usuarios_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'usuarios/usuarios_editar.html', {'usuario': usuario, 'roles': roles})

def usuario_eliminar(request, usuario_id):
    usuario = UsuarioService.get_usuario_by_id(usuario_id)
    if not usuario:
        messages.error(request, 'El usuario no existe.')
        return redirect('usuarios_lista')

    if request.method == 'POST':
        try:
            UsuarioService.delete_usuario(usuario_id)
            messages.success(request, 'Usuario eliminado correctamente.')
            return redirect('usuarios_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'usuarios/usuarios_eliminar.html', {'usuario_id': usuario_id})

