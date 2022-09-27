from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.shortcuts import get_object_or_404
from django.core.validators import MaxValueValidator, MinValueValidator

from reviews.models import (Comments, User, Review, Title, Genre,
                            Category)
from reviews.validators import validate_username


class AdminUserEditSerializer(serializers.ModelSerializer):
    """Сериализатор для получения администратором информации о пользователях
        и её редактирования."""
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all()),
                    validate_username],
    )

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role',)
        model = User


class UserSignupSerializer(AdminUserEditSerializer):
    """Сериализатор для регистрации нового пользователя, отправки им и
    зарегистрированным администратором confirmation_code."""
    email = serializers.EmailField()
    username = serializers.CharField(validators=[validate_username])

    class Meta:
        fields = ('email', 'username')
        model = User


class GetTokenSerializer(UserSignupSerializer):
    """Сериализатор для получения токена."""
    confirmation_code = serializers.CharField()

    class Meta:
        fields = ('username', 'confirmation_code')
        model = User


class EditForUserSerializer(AdminUserEditSerializer):
    """Сериализатор для получения пользователем информации о себе
    и её редактирования."""

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User
        read_only_fields = ('role',)


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор для работы с объектами Review.
    Использует кастомный метод validate().
    """

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )
    score = serializers.IntegerField(
        validators=[
            MinValueValidator(1, message='Оценка не может быть меньше 1!'),
            MaxValueValidator(10, message='Оценка не может быть больше 10!')
        ]
    )

    class Meta:
        fields = ('id', 'text', 'title',
                  'author', 'score', 'pub_date')
        model = Review
        read_only_fields = ('title',)

    def validate(self, data):
        """
        Не допускает создания 2 отзывов одним автором
        на одно произведение.
        """
        if self.context.get('request').method == 'POST':
            title_id = self.context['view'].kwargs.get('title_id')
            author = self.context.get('request').user
            title = get_object_or_404(Title, id=title_id)
            if title.reviews.filter(author=author).exists():
                raise serializers.ValidationError(
                    'Вы уже оставляли отзыв на это произведение!'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с объектами Review."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date', 'review')
        model = Comments
        read_only_fields = ('review',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class CreateUpdateTitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )
        model = Title


class GetTitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(
        source='reviews__score__avg',
        read_only=True
    )

    class Meta:
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category',
            'rating')
        read_only_fields = ('rating',)
        model = Title
