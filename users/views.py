from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CustomUser


class APIKeysView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = CustomUser.objects.get(id=request.user.id)
        if user:
            return Response(data={"api_key": user.api_key}, status=status.HTTP_200_OK)

    def post(self, request):
        user = CustomUser.objects.get(id=request.user.id)
        if user:
            api_key = get_random_string(
                32, allowed_chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
            api_secret = get_random_string(
                64, allowed_chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
            user.api_key = api_key
            user.api_secret = api_secret
            user.save()
            return Response(data={"api_key": api_key, "api_secret": api_secret}, status=status.HTTP_200_OK)


class ValidateAPIKeysView(APIView):
    def post(self, request):
        api_key = request.headers.get("api-key")
        api_secret = request.headers.get("api-secret")
        user = CustomUser.objects.get(api_key=api_key)
        if user:
            if user.api_key == api_key and user.has_valid_api_secret(api_secret):
                return Response(data={"valid": True}, status=status.HTTP_200_OK)
            return Response(data={"valid": False}, status=status.HTTP_200_OK)
