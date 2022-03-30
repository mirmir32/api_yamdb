from django.conf import settings
from rest_framework import serializers
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
    genre = GenreSerializer(read_only=True, many=True)
    categories = CategoriesSerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description',
                  'genre', 'categories', 'rating')
        read_only_fields = ('id',)


class CreateTitleSerializer(serializers.ModelSerializer):
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

    class Meta:
        model = Review
        fields = ['text', 'author', 'score', 'pub_date']

    def validate(self, data):
        """
        Validator for checking if a field 'score' has required type of data
        for ranks - integer. The digit must be from the tuple RANK (1-10).
        """
        if data['score'] is not int or data['score'] not in RANK:
            raise serializers.ValidationError(
                'Type of data is not integer.'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username',
                              read_only=True,
                              allow_null=False)

    class Meta:
        model = Comment
        fields = ['text', 'author', 'pub_date']
