from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import forbidden_username_check, validate_score_range


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


class Review(models.Model):

    text = models.TextField(verbose_name='review text')
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField(
        verbose_name='review score',
        validators=[validate_score_range]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )


class Comments(models.Model):

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(verbose_name='comment text')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )
