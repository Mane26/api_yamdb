from rest_framework import serializers

from reviews.models import Review, Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = (
            'id',
            'author',
            'text',
            'score',
            'pub_date'
        )

    def validate(self, data):
        """На одно произведение пользователь
        может оставить только один отзыв."""
        if self.context.get('request').method == 'POST':
            author = self.context.get('request').user
            title_id = self.context.get('view').kwargs.get('title_id')
            if Review.objects.filter(author=author, title=title_id).exists:
                raise serializers.ValidationError(
                    'Вы можете оставить только один комментарий'
                )
            return data
        else:
            return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = (
            'id',
            'author',
            'text',
            'pub_date'
        )
