from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .permissions import IsAdmin
from .serializers import (UserSignupSerializer, GetTokenSerializer,
                          EditForUserSerializer, AdminUserEditSerializer,)
from reviews.models import User


class UserSignupOrTokenViewSet(mixins.CreateModelMixin,
                               viewsets.GenericViewSet,):
    """Вьюсет используемый для регистрации пользователя и получения токена"""
    permission_classes = (permissions.AllowAny,)

    def get_serializer_class(self):
        """Определяет необходимый сериализатор в зависимости
        от содержания запроса"""
        if self.request.data.get('email') and self.request.data.get('username'):
            return UserSignupSerializer
        else:
            if (self.request.data.get('username')
                    and self.request.data.get('confirmation_code')):
                return GetTokenSerializer


    def create(self, request, *args, **kwargs):
        """Определяет порядок действий: создание нового пользователя или
        проверка кода подтверждения и отправка токена пользователю"""
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
                return Response({'token': str(token)},
                                status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        """Создает пользователя и отправляет ему письмо с
        кодом подтверждения"""
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
                         mixins.UpdateModelMixin,
                         viewsets.GenericViewSet,):
    """Вьюсет для получения и изменения информации о себе"""
    serializer_class = EditForUserSerializer

    def get_object(self):
        return self.request.user


class AdminUserEditViewSet(viewsets.ModelViewSet):
    """Вьюсет для получения списка пользователей, их регистрации
    и редактирования"""
    queryset = User.objects.all()
    serializer_class = AdminUserEditSerializer
    permission_classes = [IsAdmin, ]
