from rest_framework import viewsets
from rest_framework.permissions import AllowAny


class SecureApiViewSet(viewsets.ViewSet):

    permission_classes = [AllowAny]
