from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated


class SecureApiViewSet(viewsets.ViewSet):

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
