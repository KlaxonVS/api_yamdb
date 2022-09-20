from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import forbidden_username_check


class User(AbstractUser):

    ADMIN = 0
    MODER = 1
    USER = 2

    ROLE_CHOICES = (
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
    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True,
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True,
        validators=[forbidden_username_check]
    )

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
