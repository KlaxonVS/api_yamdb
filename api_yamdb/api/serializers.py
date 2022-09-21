from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import User, Review


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
        validators=[UniqueValidator(queryset=User.objects.all())],
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
        validators=[UniqueValidator(queryset=User.objects.all())],
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
    title = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    class Meta:
        fields = ('id', 'text', 'title',
                  'author', 'score', 'pub_date')
        model = Review
