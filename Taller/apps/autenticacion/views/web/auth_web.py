from django.shortcuts import render, redirect
from django.conf import settings
import requests
from django_ratelimit.decorators import ratelimit
from ...forms import LoginForm, ResetPasswordForm, ConfirmResetPasswordForm
from ...services.auth_service import AuthService
from config.security import access_required

# Constantes
TURNSTILE_VERIFY_URL = settings.TURNSTILE_VERIFY_URL
MSG_SEGURIDAD_FALLIDA = "Verificación de seguridad fallida. Por favor, inténtalo de nuevo."
TEMPLATE_LOGIN = "auth/login.html"
TEMPLATE_RECOVER = "auth/recover_account.html"
TEMPLATE_RESET = "auth/reset_password.html"


def _verify_turnstile(token):
    """Verifica el token de Cloudflare Turnstile."""
    resp = requests.post(
        TURNSTILE_VERIFY_URL,
        data={"secret": settings.TURNSTILE_SECRET_KEY, "response": token},
    )
    return resp.json().get("success", False)

@ratelimit(key='ip', rate='30/m', method='POST', block=True)
def login_view(request):
    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        if not _verify_turnstile(request.POST.get("cf-turnstile-response")):
            form.add_error(None, MSG_SEGURIDAD_FALLIDA)
            return render(request, TEMPLATE_LOGIN, {"form": form, "site_key": settings.TURNSTILE_SITE_KEY})

        service = AuthService.login(
            request,
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
        )
        if service["success"]:
            return redirect("calendario_citas")
        else:
            form.add_error(None, service["message"])

    return render(request, TEMPLATE_LOGIN, {"form": form, "site_key": settings.TURNSTILE_SITE_KEY})


@access_required()
def logout_view(request):
    AuthService.logout_user(request)
    return redirect("login")

@ratelimit(key='ip', rate='20/m', method='POST', block=True)
def recover_account_view(request):
    form = ResetPasswordForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        if not _verify_turnstile(request.POST.get("cf-turnstile-response")):
            form.add_error(None, MSG_SEGURIDAD_FALLIDA)
            return render(request, TEMPLATE_RECOVER, {"form": form, "site_key": settings.TURNSTILE_SITE_KEY})

        result = AuthService.reset_password(request, email=form.cleaned_data["email"])
        if result["success"]:
            return render(request, TEMPLATE_RECOVER, {
                "form": form,
                "site_key": settings.TURNSTILE_SITE_KEY,
                "success": True,
                "message": result["message"],
            })
        else:
            form.add_error(None, result["message"])

    return render(request, TEMPLATE_RECOVER, {"form": form, "site_key": settings.TURNSTILE_SITE_KEY})


@ratelimit(key='ip', rate='20/m', method='POST', block=True)
def reset_password_view(request, uidb64, token):
    form = ConfirmResetPasswordForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        if not _verify_turnstile(request.POST.get("cf-turnstile-response")):
            form.add_error(None, MSG_SEGURIDAD_FALLIDA)
            return render(request, TEMPLATE_RESET, {
                "form": form,
                "uid": uidb64,
                "token": token,
                "site_key": settings.TURNSTILE_SITE_KEY,
            })

        result = AuthService.confirm_reset_password(
            uidb64, token, form.cleaned_data["new_password"]
        )
        if result["success"]:
            return redirect("login")
        else:
            form.add_error(None, result["message"])

    return render(request, TEMPLATE_RESET, {
        "form": form,
        "uid": uidb64,
        "token": token,
        "site_key": settings.TURNSTILE_SITE_KEY,
    })