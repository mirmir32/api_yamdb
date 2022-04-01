from django.conf import settings
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from rest_framework import serializers, status
from rest_framework.relations import SlugRelatedField
from reviews.models import Categories, Comment, Genre, Review, Title

RANK = settings.RANKS


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Categories


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    """
    Cериализует данные Title.
    """
    genre = GenreSerializer(read_only=True, many=True)
    categories = CategoriesSerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description',
                  'genre', 'categories', 'rating')
        read_only_fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
            'rating')


class TitleDeSerializer(serializers.ModelSerializer):
    """
    Десериализует данные Title.
    """
    categories = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username',
                              read_only=True,
                              allow_null=False)
    score = serializers.IntegerField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['text', 'author', 'score', 'pub_date', 'rating']

    def get_rating(self, obj):
        return Avg(obj.score.all())

    def validate_score(self, score):
        """
        Validator for checking if a field 'score' has required type of data
        for ranks - integer. The digit must be from the tuple RANK (1-10).
        """
        if score is not int and score not in RANK:
            raise serializers.ValidationError(
                'Type of data is not integer.'
            )
        return score

    def validate_review(self, data):
        """
        Validator for blocking other attempts for reviewing if
        a user has already left one review on the exact title.
        """
        author = self.context['request'].user
        title = self.context['title_id'].review_title.pk
        review = get_object_or_404(Review, title_id=title, author=author)
        if self.context['request'].method == 'POST':
            if review.exists():
                raise serializers.ValidationError(
                    detail='Вы уже оставили свой отзыв к данному произведению.',
                    code=status.HTTP_400_BAD_REQUEST
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username',
                              read_only=True,
                              allow_null=False)

    class Meta:
        model = Comment
        fields = ['text', 'author', 'pub_date']
