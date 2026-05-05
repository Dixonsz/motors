from django.shortcuts import render


def login_view(request):
    return render(request, 'auth/login.html')

def recover_account_view(request):
    return render(request, 'auth/recover_account.html')

def reset_password_view(request):
    return render(request, 'auth/reset_password.html')