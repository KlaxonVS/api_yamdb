from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import User


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


class EditForUserSerializer(serializers.ModelSerializer):
    """Сериализатор для получения пользователем информации о себе
    и её редактирования"""
    first_name = serializers.CharField(allow_null=True, allow_blank=True,)
    last_name = serializers.CharField(allow_null=True, allow_blank=True,)
    bio = serializers.CharField(allow_null=True, allow_blank=True,)
    role = serializers.ChoiceField(default=User.USER,)

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
    first_name = serializers.CharField(allow_null=True, allow_blank=True, )
    last_name = serializers.CharField(allow_null=True, allow_blank=True, )
    bio = serializers.CharField(allow_null=True, allow_blank=True,)
    role = serializers.ChoiceField(default=User.USER,)

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User


