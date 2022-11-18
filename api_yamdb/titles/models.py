from django.contrib.auth import get_user_model
from django.db import models

from .validators import year_validation

User = get_user_model()


class Category(models.Model):
    """Модель категории."""
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=256, db_index=True,
                            verbose_name='Название категории',
                            help_text='Укажите название для категории')
    slug = models.SlugField(max_length=256, unique=True,
                            verbose_name='URL категории',
                            help_text='Задайте уникальный URL адрес категории.'
                                      ' Используйте только латиницу, цифры,'
                                      ' дефисы и знаки подчёркивания')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанра."""
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=256, db_index=True,
                            verbose_name='Название жанра',
                            help_text='Укажите название жанра')
    slug = models.SlugField(unique=True, verbose_name='URL жанра',
                            help_text='Задайте уникальный URL адрес жанра. '
                                      'Используйте только латиницу, цифры, '
                                      'дефисы и знаки подчёркивания')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведения."""
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=256, db_index=True,
                            verbose_name='Название произведения',
                            help_text='Укажите название произведения')
    year = models.PositiveSmallIntegerField(verbose_name='Год выпуска',
                                            validators=[year_validation],
                                            help_text='Задайте год выпуска')
    description = models.TextField(null=True, blank=True,
                                   verbose_name='Описание')
    category = models.ForeignKey(Category, verbose_name='Категория',
                                 on_delete=models.SET_NULL,
                                 related_name="titles", blank=True, null=True)
    genre = models.ManyToManyField(Genre, verbose_name='Жанр',
                                   related_name="titles", blank=True)
    rating = models.IntegerField(null=True, default=None)

    class Meta:
        ordering = ('-year',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name
