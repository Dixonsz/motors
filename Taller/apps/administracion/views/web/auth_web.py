from django.shortcuts import render, redirect
from django.conf import settings
import requests
from ...forms import LoginForm, ResetPasswordForm, ConfirmResetPasswordForm
from ...services.auth_service import AuthService
from ...security import access_required


def login_view(request):

    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        token = request.POST.get("cf-turnstile-response")
        resp = requests.post(
            "https://challenges.cloudflare.com/turnstile/v0/siteverify",
            data={"secret": settings.TURNSTILE_SECRET_KEY, "response": token},
        )
        turnstile_result = resp.json().get("success", False)

        if not turnstile_result:
            form.add_error(
                None,
                "Verificación de seguridad fallida. Por favor, inténtalo de nuevo.",
            )
            return render(
                request,
                "auth/login.html",
                {
                    "form": form,
                    "site_key": settings.TURNSTILE_SITE_KEY,
                },
            )
        service = AuthService.login(
            request,
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
        )
        if service["success"]:
            return redirect("citas_calendario")
        else:
            form.add_error(None, service["message"])

    return render(
        request,
        "auth/login.html",
        {
            "form": form,
            "site_key": settings.TURNSTILE_SITE_KEY,
        },
    )


@access_required()
def logout_view(request):
    AuthService.logout_user(request)
    return redirect("login")


def recover_account_view(request):
    form = ResetPasswordForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        turnstile_token = request.POST.get("cf-turnstile-response")
        resp = requests.post(
            "https://challenges.cloudflare.com/turnstile/v0/siteverify",
            data={"secret": settings.TURNSTILE_SECRET_KEY, "response": turnstile_token},
        )
        turnstile_result = resp.json().get("success", False)

        if not turnstile_result:
            form.add_error(
                None,
                "Verificación de seguridad fallida. Por favor, inténtalo de nuevo.",
            )
            return render(
                request,
                "auth/recover_account.html",
                {
                    "form": form,
                    "site_key": settings.TURNSTILE_SITE_KEY,
                },
            )

        result = AuthService.reset_password(request, email=form.cleaned_data["email"])
        if result["success"]:
            return render(
                request,
                "auth/recover_account.html",
                {
                    "form": form,
                    "site_key": settings.TURNSTILE_SITE_KEY,
                    "success": True,
                    "message": result["message"],
                },
            )
        else:
            form.add_error(None, result["message"])

    return render(
        request,
        "auth/recover_account.html",
        {
            "form": form,
            "site_key": settings.TURNSTILE_SITE_KEY,
        },
    )


def reset_password_view(request, uidb64, token):
    form = ConfirmResetPasswordForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        turnstile_token = request.POST.get("cf-turnstile-response")
        resp = requests.post(
            "https://challenges.cloudflare.com/turnstile/v0/siteverify",
            data={"secret": settings.TURNSTILE_SECRET_KEY, "response": turnstile_token},
        )
        turnstile_result = resp.json().get("success", False)

        if not turnstile_result:
            form.add_error(
                None,
                "Verificación de seguridad fallida. Por favor, inténtalo de nuevo.",
            )
            return render(
                request,
                "auth/reset_password.html",
                {
                    "form": form,
                    "uid": uidb64,
                    "token": token,
                    "site_key": settings.TURNSTILE_SITE_KEY,
                },
            )

        result = AuthService.confirm_reset_password(
            uidb64, token, form.cleaned_data["new_password"]
        )
        if result["success"]:
            return redirect("login")
        else:
            form.add_error(None, result["message"])

    return render(
        request,
        "auth/reset_password.html",
        {
            "form": form,
            "uid": uidb64,
            "token": token,
            "site_key": settings.TURNSTILE_SITE_KEY,
        },
    )