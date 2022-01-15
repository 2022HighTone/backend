from django.contrib.auth import get_user_model
from rest_framework.generics import GenericAPIView
from rest_framework import permissions, status
from rest_framework.response import Response

from domains.auth.serializer import (
    SignUpSerializer, GetTokenSerializer, LoginSerializer,
    DefaultSchoolSettingSerializer
)


User = get_user_model()


class SignUpView(GenericAPIView):
    serializer_class = SignUpSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        token = GetTokenSerializer(user).data

        return Response(token, status=status.HTTP_200_OK)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        token = GetTokenSerializer(user).data

        return Response(token, status=status.HTTP_200_OK)


class DefaultSchoolSettingView(GenericAPIView):
    serializer_class = DefaultSchoolSettingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'success': 'default school is set'})