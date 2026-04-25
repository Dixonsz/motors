# usuario_web.py (Templates)
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from ...services.usuario_service import UsuarioService
from ...services.rol_service import RolService


def usuario_lista(request):
    usuarios = UsuarioService.get_all_usuarios()
    paginator = Paginator(usuarios, 10)
    page_number = request.GET.get('page')
    usuarios = paginator.get_page(page_number)
    return render(request, 'usuarios/usuarios_lista.html', {'usuarios': usuarios})


def usuario_create(request):
    if request.method == 'POST':
        try:
            UsuarioService.create_usuario(
                username=request.POST.get('username'),
                password=request.POST.get('password'),
                nombre=request.POST.get('nombre'),
                apellido=request.POST.get('apellido'),
                cedula=request.POST.get('cedula'),
                telefono=request.POST.get('telefono'),
                direccion=request.POST.get('direccion'),
                rol_id=request.POST.get('rol_id'),
                especialidad=request.POST.get('especialidad')
            )
            messages.success(request, 'Usuario creado correctamente.')
            return redirect('usuarios_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    roles = RolService.get_all_roles()
    return render(request, 'usuarios/usuarios_crear.html', {'roles': roles})


def usuario_editar(request, usuario_id):
    usuario = UsuarioService.get_usuario_by_id(usuario_id)
    if not usuario:
        messages.error(request, 'El usuario no existe.')
        return redirect('usuarios_lista')

    if request.method == 'POST':
        try:
            UsuarioService.update_usuario(
                usuario_id,
                nombre=request.POST.get('nombre'),
                apellido=request.POST.get('apellido'),
                telefono=request.POST.get('telefono'),
                direccion=request.POST.get('direccion'),
                especialidad=request.POST.get('especialidad'),
                rol_id=request.POST.get('rol_id')
            )
            messages.success(request, 'Usuario actualizado correctamente.')
            return redirect('usuarios_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    roles = RolService.get_all_roles()
    return render(request, 'usuarios/usuarios_editar.html', {
        'usuario': usuario,
        'roles': roles
    })


def usuario_cambiar_password(request, usuario_id):
    usuario = UsuarioService.get_usuario_by_id(usuario_id)
    if not usuario:
        messages.error(request, 'El usuario no existe.')
        return redirect('usuarios_lista')

    if request.method == 'POST':
        try:
            UsuarioService.cambiar_password(
                usuario_id,
                password_actual=request.POST.get('password_actual'),
                password_nueva=request.POST.get('password_nueva')
            )
            messages.success(request, 'Contraseña actualizada correctamente.')
            return redirect('usuarios_lista')
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'usuarios/usuarios_cambiar_password.html', {'usuario': usuario})


def usuario_activar_desactivar(request, usuario_id):
    try:
        usuario = UsuarioService.activar_desactivar_usuario(usuario_id)
        estado = 'activado' if usuario.estado else 'desactivado'
        messages.success(request, f'Usuario {estado} correctamente.')
    except ValueError as exc:
        messages.error(request, str(exc))
    return redirect('usuarios_lista')


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

    return render(request, 'usuarios/usuarios_eliminar.html', {'usuario': usuario})