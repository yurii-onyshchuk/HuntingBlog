from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework import viewsets

from blog.models import Post, Category, Tag, Comment, Subscriber
from .serializers import PostSerializer, CategorySerializer, TagSerializer, CommentSerializer, SubscriberSerializer

User = get_user_model()


class PostAPIViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CategoryAPIViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagAPIViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class PostByCategoryAPIView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(category__pk=self.kwargs['pk'])


class PostByTagAPIView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(tag__pk=self.kwargs['pk'])


class PostCommentsAPIView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(post__pk=self.kwargs['pk'])


class CommentsAPIViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class SubscriberAPIViewSet(viewsets.ModelViewSet):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
