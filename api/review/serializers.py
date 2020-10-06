from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import (
    ValidationError,
    PermissionDenied,
    AuthenticationFailed
)

from api.title.models import Category, Genre, Title
from api.users.models import User

from .models import Review, Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    score = serializers.IntegerField(min_value=1, max_value=10)

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def create(self, validated_data):
        author = self.context['request'].user
        request = self.context.get('request')
        title_id = request.parser_context['kwargs']['title_id']
        method = request.method
        title = get_object_or_404(Title, pk=title_id)
        review = Review.objects.filter(title_id=title_id, author=author)
        if method == 'POST' and review:
            raise ValidationError('Только один отзыв на одно произведение.')
        return Review.objects.create(
            author=author,
            title_id=title_id,
            **validated_data
        )

    def update(self, instance, validated_data):
        author = self.context['request'].user
        if not author.is_authenticated:
            raise AuthenticationFailed()
        if instance.author != author:
            raise PermissionDenied()
        instance.text = validated_data.get('text', instance.text)
        instance.score = validated_data.get('score', instance.score)
        instance.pub_date = validated_data.get('pub_date', instance.pub_date)
        instance.save()
        return instance


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'author', 'text', 'pub_date')
        model = Comment

    def create(self, validated_data):
        author = self.context['request'].user
        request = self.context.get('request')
        review_id = request.parser_context['kwargs']['review_id']
        review = get_object_or_404(Review, pk=review_id)
        return Comment.objects.create(
            author=author,
            review_id=review_id,
            **validated_data
        )

    def update(self, instance, validated_data):
        author = self.context['request'].user
        if not author.is_authenticated:
            raise AuthenticationFailed()
        if instance.author != author:
            raise PermissionDenied()
        instance.text = validated_data.get('text', instance.text)
        instance.pub_date = validated_data.get('pub_date', instance.pub_date)
        instance.save()
        return instance
