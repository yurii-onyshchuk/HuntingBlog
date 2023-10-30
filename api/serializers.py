from django.contrib.auth import get_user_model

from rest_framework import serializers

from blog.models import Post, Category, Tag, Comment, Subscriber

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model."""

    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag model."""

    class Meta:
        model = Tag
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    """Serializer for Post model."""

    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model."""

    class Meta:
        model = Comment
        fields = '__all__'


class SubscriberSerializer(serializers.ModelSerializer):
    """Serializer for Subscriber model."""

    class Meta:
        model = Subscriber
        fields = '__all__'
