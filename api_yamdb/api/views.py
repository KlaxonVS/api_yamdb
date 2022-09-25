from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, status, filters, mixins
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .permissions import (IsAdmin, IsAdminOrReadOnly,
                          IsAdminModerAuthorOrReadOnly)
from .serializers import (CommentSerializer, UserSignupSerializer,
                          GetTokenSerializer, AdminUserEditSerializer,
                          EditForUserSerializer, ReviewSerializer,
                          GetTitleSerializer, CreateUpdateTitleSerializer,
                          CategorySerializer, GenreSerializer)
from .utils import calculate_rating, send_confirmation_code
from .filters import TitlesFilter
from reviews.models import User, Review, Title, Genre, Category, Comments



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
    """API-функция для проверки кода подтверждения и отправки токена"""
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


class UserEditViewSet(viewsets.ModelViewSet):
    """Вьюсет для получения списка пользователей, их регистрации
    и редактирования, а также для получения пользователем данных о себе и их
    изменение"""
    queryset = User.objects.all()
    serializer_class = AdminUserEditSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'username'
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(methods=['get', 'patch'], detail=False, url_path='me',
            serializer_class=EditForUserSerializer,
            permission_classes=[permissions.IsAuthenticated])
    def user_me_view(self, request):
        """Метод дающий доступ пользователю к данным о себе и их изменение"""
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = self.get_serializer(user, data=request.data,
                                             partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminModerAuthorOrReadOnly]
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs['title_id'])

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())
        calculate_rating(self.get_title())

    def perform_update(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())
        calculate_rating(self.get_title())

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        calculate_rating(self.get_title())


class CommentsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminModerAuthorOrReadOnly]
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs['review_id'])

    def get_queryset(self):
        review = self.get_review()
        return review.comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class CategoryViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                      mixins.CreateModelMixin, mixins.DestroyModelMixin):
    queryset = Category.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                   mixins.CreateModelMixin, mixins.DestroyModelMixin):
    queryset = Genre.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetTitleSerializer
        return CreateUpdateTitleSerializer
