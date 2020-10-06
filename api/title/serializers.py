from django.db.models import Avg
from rest_framework import serializers

from api.review.models import Review

from .models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CustomSlugRelatedField(serializers.SlugRelatedField):
    def to_representation(self, obj):
        return {'name': obj.name, 'slug': obj.slug}


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField(read_only=True)
    category = CustomSlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = CustomSlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug', many=True
    )

    class Meta:
        fields = (
            'id', 'name', 'year',
            'rating', 'description',
            'genre', 'category'
        )
        model = Title

    def get_rating(self, title):
        scores = Review.objects.filter(
            title_id=title.id).aggregate(Avg('score')
        )
        if scores:
            return scores['score__avg']
        return None
