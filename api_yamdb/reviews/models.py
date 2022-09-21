from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import forbidden_username_check, validate_score_range


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
        return self.role == self.MODER

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


class Review(models.Model):

    text = models.TextField(verbose_name='текст отзыва')
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
        verbose_name='оценка',
        validators=[validate_score_range]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['title', 'pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


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
    text = models.TextField(verbose_name='текст комментария')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['review', 'pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
