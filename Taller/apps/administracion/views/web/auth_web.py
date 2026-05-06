from django.shortcuts import render, redirect
from ...forms import LoginForm
from ...services.auth_service import AuthService
from ...security import access_required


def login_view(request):

    form = LoginForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        service = AuthService.login(
            request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        if service["success"]:
            return redirect('citas_calendario')
        else:
            form.add_error(None, service["message"])
    return render(request, 'auth/login.html', {'form': form})

@access_required()
def logout_view(request):
    AuthService.logout_user(request)
    return redirect('login')


def recover_account_view(request):
    return render(request, 'auth/recover_account.html')

def reset_password_view(request):
    return render(request, 'auth/reset_password.html')