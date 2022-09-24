from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .validators import validate_username
from reviews.models import Comments, User, Review, Title, Genre, Category


class UserSignupSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации нового пользователя"""
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    class Meta:
        fields = ('email', 'username')
        model = User


class GetTokenSerializer(serializers.ModelSerializer):
    """Сериализатор для получения токена"""
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        fields = ('username', 'confirmation_code')
        model = User


class EditForUserSerializer(serializers.ModelSerializer):
    """Сериализатор для получения пользователем информации о себе
    и её редактирования"""
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all()),
                    validate_username],
    )

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User
        read_only_fields = ('role',)


class AdminUserEditSerializer(serializers.ModelSerializer):
    """Сериализатор для получения администратором информации о пользователях
        и её редактирования"""
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all()),
                    validate_username],
    )

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User


class ReviewSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text',
                  'author', 'score', 'pub_date')
        model = Review


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comments


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category', 'rating')
        read_only_fields = ('rating', )
        model = Title


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category
