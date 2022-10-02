from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_username, validate_year


class User(AbstractUser):
    """Модель юзера с добавлением полей роль и биография."""
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
        max_length=max(len(role_en) for role_en, role_ru in ROLE_CHOICES),
        choices=ROLE_CHOICES,
        default=USER
    )
    bio = models.TextField('Биография', null=True, blank=True)
    email = models.EmailField(
        'Электронная почта',
        max_length=settings.EMAIL_M_LENGTH,
        unique=True,
    )
    username = models.CharField(
        'Имя пользователя',
        max_length=settings.USERNAME_M_LENGTH,
        unique=True,
        validators=[validate_username],
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_moderator(self):
        """Проверяет что пользователь модератор"""
        return self.role == self.MODER

    @property
    def is_admin(self):
        """Проверяет что пользователь администратор"""
        return self.role == self.ADMIN or self.is_staff

    def __str__(self):
        return self.email


class GenreCategory(models.Model):
    """Родительская модель жанра и категории."""
    name = models.CharField(
        'Название',
        max_length=settings.NAME_M_LENGTH
    )
    slug = models.SlugField(
        'Метка',
        max_length=settings.SLUG_M_LENGTH,
        unique=True
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name


class Category(GenreCategory):
    """Модель категорий произведений."""
    class Meta(GenreCategory.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(GenreCategory):
    """Модель жанров произведений."""
    class Meta(GenreCategory.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Модель произведения."""
    name = models.TextField(
        'Название',
    )
    year = models.PositiveSmallIntegerField(
        'Дата выхода',
        validators=[validate_year],
        db_index=True
    )
    description = models.TextField(
        'Описание',
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        related_name='titles'
    )

    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name


class ReviewComment(models.Model):
    """Родительская модель отзывов и комментариев."""
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата публикации'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    text = models.TextField('Текст')

    class Meta:
        ordering = ('pub_date',)
        abstract = True

    def __str__(self):
        return self.text


class Review(ReviewComment):
    """Модель отзывов к произведениям."""
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
    )
    score = models.PositiveSmallIntegerField(
        'Оценка',
        validators=[
            MinValueValidator(1, message='Оценка не может быть меньше 1!'),
            MaxValueValidator(10, message='Оценка не может быть больше 10!')
        ],
    )

    class Meta(ReviewComment.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            )
        ]
        default_related_name = 'reviews'


class Comments(ReviewComment):
    """Модель комментариев к отзывам."""
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
    )

    class Meta(ReviewComment.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
