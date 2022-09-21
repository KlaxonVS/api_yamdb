from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .permissions import IsAdmin, IsAdminOrAuthorOrReadOnly
from .serializers import (UserSignupSerializer, GetTokenSerializer,
                          AdminUserEditSerializer, ReviewSerializer)
from reviews.models import User, Review, Title


def send_confirmation_code(user):
    """Функция для отправки кода подтверждения"""
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Hallo from YaMDb',
        message=(
            f'Код подтверждения(confirmation_code): {confirmation_code}\n'
            'Используйте его для получения своего токена'
        ),
        from_email=None,
        recipient_list=[user.email],
    )


@api_view(['post'])
@permission_classes([permissions.AllowAny])
def register_or_confirm_code(request):
    """API-функция для регистрации новых пользователей
    и запроса кода подтверждения"""
    if User.objects.filter(
            email=request.data.get('email'),
            username=request.data.get('username')
    ).exists():
        send_confirmation_code(
            User.objects.get(
                email=request.data.get('email'),
                username=request.data.get('username'))
        )
        return Response(request.data, status=status.HTTP_200_OK)
    serializer = UserSignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = get_object_or_404(
        User,
        email=serializer.validated_data.get('email')
    )
    send_confirmation_code(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['post'])
@permission_classes([permissions.AllowAny])
def get_token(request):
    """API-фунуция для проверки кода подтверждения и отправки токена"""
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
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


class AdminUserEditViewSet(viewsets.ModelViewSet):
    """Вьюсет для получения списка пользователей, их регистрации
    и редактирования"""
    queryset = User.objects.all()
    serializer_class = AdminUserEditSerializer
    permission_classes = [IsAdmin]


class ReviewViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAdminOrAuthorOrReadOnly]
    serializer_class = ReviewSerializer

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs['title_id'])

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())
