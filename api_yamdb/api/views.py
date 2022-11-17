from rest_framework import viewsets
from django.shortcuts import get_object_or_404

from reviews.models import Review, Title
from api.serializers import ReviewSerializer, CommentSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Для модели Review: отзывы на произведения."""
    serializer_class = ReviewSerializer
    # permission_classes = (...)

    def get_title(self):
        """ Получение произведения. """
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)

    def get_all_reviews(self):
        """ Получение списка всех отзывов на произведение. """
        return self.get_title().reviews.all()

    def review_add(self, serializer):
        """ Добавление нового отзыва на произведение. """
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    """Для модели Comment: комментарии к отзывам."""
    serializer_class = CommentSerializer
    # permission_classes = (...)

    def get_review(self):
        """ Получение отзыва на произведение."""
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, pk=review_id)

    def get_all_comments(self):
        """ Получение списка всех комментариев к отзыву."""
        return self.get_review().comments.all()

    def comment_add(self, serializer):
        """ Добавление нового комментария к отзыву. """
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )
