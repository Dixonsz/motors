from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import redirect


class LoginRequiredMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)


class ProtectedErrorMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            return self.get_response(request)
        except ProtectedError:
            if not _is_web_request(request):
                raise
            message = "No se puede eliminar el registro porque esta asociado a otros datos."
            messages.error(request, message)
            return redirect(request.META.get("HTTP_REFERER", "/"))


def _is_web_request(request):
    accept_header = request.headers.get("Accept", "")
    if "text/html" in accept_header or "application/xhtml+xml" in accept_header:
        return True
    content_type = (request.content_type or "").lower()
    return content_type in {"application/x-www-form-urlencoded", "multipart/form-data"}
