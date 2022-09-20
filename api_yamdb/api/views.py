from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import User
from .serializers import (UserSignupSerializer, GetTokenSerializer,
                          EditForUserSerializer, AdminUserEditSerializer,)


class UserSignupOrTokenViewSet(mixins.CreateModelMixin,):
    permission_classes = (permissions.AllowAny,)

    def get_serializer_class(self):
        if self.request.data['email'] and self.request.data['username']:
                return UserSignupSerializer
        else:
            if (self.request.data['username']
                and self.request.data['confirmation_code']):
                return GetTokenSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if 'email' and 'username' in serializer.validated_data:
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if 'username' and 'confirmation_code' in serializer.validated_data:
            user = get_object_or_404(
                User,
                username=serializer.validated_data["username"]
            )
            if default_token_generator.check_token(
                    user, serializer.validated_data["confirmation_code"]
            ):
                token = AccessToken.for_user(user)
                return Response({"token": str(token)},
                                status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save()
        user = get_object_or_404(User, serializer.validated_data['username'])
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Вы зарегистрировались на YaMDb',
            message=(
                f'Код подтверждения(confirmation_code): {confirmation_code}'
                'Используйте его для получения своего токена'
            ),
            from_email=None,
            recipient_list=[user.email],
        )


class EditForUserViewSet(mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,):
    pass


class AdminUserEditViewSet():
    pass