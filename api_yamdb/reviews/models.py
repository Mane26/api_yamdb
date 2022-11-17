from django.db import models
from django.contrib.auth import get_user_model
from django.core import validators

User = get_user_model()


class Review(models.Model):
    """Ресурс reviews: отзывы, привязанные к произведениям."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор отзыва',
        related_name='reviews'
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
    )
    title = models.ForeignKey(
        # Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
        related_name='reviews'
    )
    score = models.IntegerField(
        validators=[
            validators.MinValueValidator(1, 'Минимальный балл - 1'),
            validators.MaxValueValidator(10, 'Максимальный балл - 10')
        ],
        verbose_name='Оценка произведения'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата'
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=[
                    'author',
                    'title'
                ],
                name='unique_author_title'
            )
        )
        ordering = ('-pub_date',)
        verbose_name = 'Отзыв'

    def __str__(self):
        return self.text[:25]


class Comment(models.Model):
    """ Ресурс comments: комментарии к отзывам, привязанные к отзывам."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария',
        related_name='comments'
    )
    text = models.TextField(
        verbose_name='Текст комментария',
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Комментируемый отзыв',
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата'
    )

    class Meta:
        verbose_name = 'Комментарий к отзыву'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:25]
