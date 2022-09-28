from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import (validate_username,
                         validate_year)
from api_yamdb.settings import USERNAME_M_LENGTH, EMAIL_M_LENGTH


class User(AbstractUser):

    ADMIN = 'admin'
    MODER = 'moderator'
    USER = 'user'

    ROLE_CHOICES = (
        (ADMIN, 'Администратор'),
        (MODER, 'Модератор'),
        (USER, 'Пользователь'),
    )

    role_length = 0
    for role in ROLE_CHOICES:
        if len(role[0]) > role_length:
            role_length = len(role[0])

    role = models.CharField(
        'Роль',
        max_length=role_length,
        choices=ROLE_CHOICES,
        default=USER
    )
    bio = models.TextField('Биография', null=True, blank=True)
    email = models.EmailField(
        max_length=EMAIL_M_LENGTH,
        verbose_name='Электронная почта',
        unique=True,
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=USERNAME_M_LENGTH,
        unique=True,
        validators=[validate_username],
    )

    @property
    def is_moderator(self):
        """Проверяет что пользователь модератор"""
        return self.role == self.MODER

    @property
    def is_admin(self):
        """Проверяет что пользователь администратор"""
        return self.role == self.ADMIN or self.is_staff

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class GenreCategory(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='Метка',
        max_length=50,
        unique=True
    )

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(GenreCategory):
    class Meta(GenreCategory.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(GenreCategory):
    class Meta(GenreCategory.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=200
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Дата выхода',
        validators=[validate_year]
    )
    # Слишком большой тип данных для такого маленького числа.
    # Плюс чтобы ускорить поиск произведений по году, лучше добавить индекс.
    description = models.TextField(
        verbose_name='Описание',
        max_length=400,
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        through='GenreTitle'
    )
    # Лишняя строка, и лишняя промежуточная модель.
    # У нас в промежуточной модели ничего не меняется,
    #  можно её не писать, в БД записи сами создадутся даже без модели.
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
        ordering = ['name']

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE)
    genre = models.ForeignKey(
        Genre,
        verbose_name='Жанр',
        on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Произведение и жанр'
        verbose_name_plural = 'Произведения и жанры'

    def __str__(self):
        return f'{self.title}, жанр - {self.genre}'


class ReviewComment(models.Model):

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

    class Meta:
        ordering = ('pub_date',)
        abstract = True


class Review(ReviewComment):

    text = models.TextField(verbose_name='Текст отзыва')
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
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

    def __str__(self):
        return self.text[:15]


class Comments(ReviewComment):

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
    )
    text = models.TextField(verbose_name='Текст комментария')

    class Meta(ReviewComment.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'

    def __str__(self):
        return self.text
