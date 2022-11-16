import datetime

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, RegexValidator
from django.db import models

User = get_user_model()

NUM_OF_CHAR = 15


class Category(models.Model):
    name = models.CharField(verbose_name='Название', max_length=256)
    slug = models.SlugField(verbose_name='Slug категории',
                            max_length=50, unique=True,
                            validators=[RegexValidator(
                                regex=r'^[-a-zA-Z0-9_]+$',
                                message='Некорректный slug'
                            )])

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.name[:NUM_OF_CHAR]


class Genre(models.Model):
    name = models.CharField(verbose_name='Название', max_length=256)
    slug = models.SlugField(verbose_name='Slug жанра',
                            max_length=50, unique=True,
                            validators=[RegexValidator(
                                regex=r'^[-a-zA-Z0-9_]+$',
                                message='Некорректный slug'
                            )])

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self) -> str:
        return self.name[:NUM_OF_CHAR]


class Title(models.Model):
    name = models.TextField(verbose_name='Название')
    year = models.IntegerField(verbose_name='Год выпуска',
                               validators=[MaxValueValidator(
                                   limit_value=datetime.datetime.now().year,
                                   message='Нельзя добавлять произведения, '
                                           'которые еще не вышли'
                               )])
    description = models.TextField(null=True, blank=True)
    genre = models.ManyToManyField(
        Genre
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_DEFAULT,
        related_name="title", default=0
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self) -> str:
        return self.name[:NUM_OF_CHAR]
