from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from titles.models import Title
from users.models import User


class Review(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name='reviews')
    text = models.TextField(verbose_name='Отзыв', help_text='Напишите отзыв')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)
    score = models.PositiveSmallIntegerField(validators=[MinValueValidator(1),
                                             MaxValueValidator(10)])

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date', 'score')
        constraints = [
            models.UniqueConstraint(fields=['title', 'author'],
                                    name='unique review')
        ]


class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               related_name='comments')
    text = models.TextField(verbose_name='Комментарий',
                            help_text='Введите текст комментария')
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)
