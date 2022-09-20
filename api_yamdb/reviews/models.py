from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    SUPERUSER = 0
    ADMIN = 1
    MODER = 2
    USER = 3

    ROLE_CHOICES = (
        (SUPERUSER, 'superuser'),
        (ADMIN, 'administrator'),
        (MODER, 'moderator'),
        (USER, 'user'),
    )

    role = models.PositiveSmallIntegerField(
        'Роль',
        choices=ROLE_CHOICES,
        default=USER
    )
    bio = models.TextField('Биография', blank=True,)
    email = models.Email.Field(
        verbose_name='Электронная почта',
        unique=True,
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True,
        validators=['forbidden_username_check']
    )

    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
