# usuario_web.py (Templates)
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from ...services.usuario_service import UsuarioService
from ...services.rol_service import RolService
from config.security import access_required


@access_required("Usuarios", "ver")
def usuario_lista(request):
    nombre = request.GET.get('nombre', '').strip()
    email = request.GET.get('email', '').strip()
    cedula = request.GET.get('cedula', '').strip()

    usuarios = UsuarioService.get_usuarios_filtrados(nombre=nombre, email=email, cedula=cedula)
    paginator = Paginator(usuarios, 10)
    page_number = request.GET.get('page')
    usuarios = paginator.get_page(page_number)
    filtros_query = request.GET.copy()
    filtros_query.pop('page', None)
    return render(request, 'usuarios/usuarios_lista.html', {'usuarios': usuarios, 'filtros': {
        'nombre': nombre,
        'email': email,
        'cedula': cedula
    }, 'filtros_query': filtros_query.urlencode()
    })


@access_required("Usuarios", "crear")
def usuario_create(request):
    if request.method == 'POST':
        try:
            UsuarioService.create_usuario(
                username=request.POST.get('username'),
                email=request.POST.get('email'),
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


@access_required("Usuarios", "editar")
def usuario_editar(request, usuario_id):
    usuario = UsuarioService.get_usuario_by_id(usuario_id)
    if not usuario:
        messages.error(request, 'El usuario no existe.')
        return redirect('usuarios_lista')

    if request.method == 'POST':
        try:
            UsuarioService.update_usuario(
                usuario_id,
                username=request.POST.get('username'),
                email=request.POST.get('email'),
                nombre=request.POST.get('nombre'),
                apellido=request.POST.get('apellido'),
                cedula=request.POST.get('cedula'),
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


@access_required("Usuarios", "editar")
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


@access_required("Usuarios", "editar")
def usuario_activar_desactivar(request, usuario_id):
    try:
        usuario = UsuarioService.activar_desactivar_usuario(usuario_id)
        estado = 'activado' if usuario.estado else 'desactivado'
        messages.success(request, f'Usuario {estado} correctamente.')
    except ValueError as exc:
        messages.error(request, str(exc))
    return redirect('usuarios_lista')


