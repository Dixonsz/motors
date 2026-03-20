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

        UsuarioService.create_usuario(nombre, apellido, telefono, correo, rol_id, password)
        return redirect('usuarios_lista')
    
    roles = RolService.get_all_roles()
    return render(request, 'usuarios/usuarios_crear.html', {'roles': roles})    


def usuario_editar(request, usuario_id):
    usuario = UsuarioService.get_usuario_by_id(usuario_id)
    roles = RolService.get_all_roles()

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        telefono = request.POST.get('telefono')
        correo = request.POST.get('correo')
        rol_id = request.POST.get('rol_id')
        password = request.POST.get('password')

        UsuarioService.update_usuario(usuario_id, nombre, apellido, telefono, correo, rol_id, password)
        return redirect('usuarios_lista')

    return render(request, 'usuarios/usuarios_editar.html', {'usuario': usuario, 'roles': roles})

def usuario_eliminar(request, usuario_id):
    if request.method == 'POST':
        UsuarioService.delete_usuario(usuario_id)
        return redirect('usuarios_lista')

    return render(request, 'usuarios/usuarios_eliminar.html', {'usuario_id': usuario_id})

