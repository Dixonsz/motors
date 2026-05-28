from django.shortcuts import render


def permission_denied_view(request, exception=None):
    back_url = request.META.get("HTTP_REFERER") or "/"
    return render(request, "403.html", {"back_url": back_url}, status=403)
