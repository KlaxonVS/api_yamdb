from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import forbidden_username_check


class User(AbstractUser):

    ADMIN = 'admin'
    MODER = 'moderator'
    USER = 'user'

    ROLE_CHOICES = (
        (ADMIN, 'Администратор'),
        (MODER, 'Модератор'),
        (USER, 'Пользователь'),
    )

    role = models.CharField(
        'Роль',
        max_length=10,
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
        """Проверяет что пользователь модератор"""
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        """Проверяет что пользователь администратор"""
        return self.role == self.ADMIN

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
