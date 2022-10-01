from django.contrib.auth.tokens import default_token_generator
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .filters import TitlesFilter
from .mixins import GenreCategoryViewSetMixin
from .permissions import (IsAdmin, IsAdminModerAuthorOrReadOnly,
                          IsAdminOrReadOnly)
from .serializers import (AdminUserEditSerializer, CategorySerializer,
                          CommentSerializer, CreateUpdateTitleSerializer,
                          EditForUserSerializer, GenreSerializer,
                          GetTitleSerializer, GetTokenSerializer,
                          ReviewSerializer, UserSignupSerializer)
from .utils import send_confirmation_code
from reviews.models import Category, Genre, Review, Title, User


@api_view(['post'])
def register_or_confirm_code(request):
    """API-функция для регистрации новых пользователей
    и запроса кода подтверждения."""
    serializer = UserSignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user, created = User.objects.get_or_create(
            email=serializer.validated_data.get('email'),
            username=serializer.validated_data.get('username'),
        )
    except IntegrityError as error:
        messages = (('email', 'Электронная почта уже занята!'),
                    ('username', 'Имя пользователя уже занято!'))
        for field, message in messages:
            if field in str(error):
                return Response(
                    {f'{field}': f'{message}'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
    send_confirmation_code(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['post'])
def get_token(request):
    """API-функция для проверки кода подтверждения и отправки токена."""
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data.get('username')
    )
    if default_token_generator.check_token(
            user, serializer.validated_data.get('confirmation_code')
    ):
        token = AccessToken.for_user(user)
        return Response({'token': str(token)},
                        status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserEditViewSet(viewsets.ModelViewSet):
    """Вьюсет для получения списка пользователей, их регистрации
    и редактирования, а также для получения пользователем данных о себе и их
    изменение."""
    queryset = User.objects.all()
    serializer_class = AdminUserEditSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(methods=['get', 'patch'], detail=False, url_path='me',
            serializer_class=EditForUserSerializer,
            permission_classes=[permissions.IsAuthenticated])
    def user_me_view(self, request):
        """Метод дающий доступ пользователю к данным о себе и их изменение."""
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(user, data=request.data,
                                         partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для работы с объектами Review.
    Методы perform_create, perform_update и perform_destroy
    переопределены для автоматического рассчета рейтинга связанного
    объекта Title.
    """

    permission_classes = [IsAdminModerAuthorOrReadOnly]
    serializer_class = ReviewSerializer

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs['title_id'])

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentsViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с объектами Comment."""

    permission_classes = [IsAdminModerAuthorOrReadOnly]
    serializer_class = CommentSerializer

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs['review_id'])

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class CategoryViewSet(GenreCategoryViewSetMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(GenreCategoryViewSetMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)
    filterset_class = TitlesFilter
    ordering_fields = ('name',)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetTitleSerializer

        return CreateUpdateTitleSerializer
