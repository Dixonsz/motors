from django.shortcuts import render, redirect
from ...forms import LoginForm, ResetPasswordForm, ConfirmResetPasswordForm
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

    form = ResetPasswordForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        result = AuthService.reset_password(request, email=form.cleaned_data['email'])
        if result['success']:
            return render(request, 'auth/recover_account.html',{
                          'form': form,
                          'success': True,
                          'message': result['message']
                          })
        else:
            form.add_error(None, result['message'])
    return render(request, 'auth/recover_account.html')

def reset_password_view(request, uidb64, token):
    form = ConfirmResetPasswordForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        result = AuthService.confirm_reset_password(uidb64, token, form.cleaned_data['new_password'])
        if result['success']:
            return redirect('login')
        else:
            form.add_error(None, result['message'])

    return render(request, 'auth/reset_password.html', {'form': form, 'uid': uidb64,'token': token })