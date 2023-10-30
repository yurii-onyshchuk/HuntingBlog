from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework import viewsets

from blog.models import Post, Category, Tag, Comment, Subscriber
from .permissions import SubscribePermission
from .serializers import PostSerializer, CategorySerializer, TagSerializer, CommentSerializer, SubscriberSerializer

User = get_user_model()


class PostAPIViewSet(viewsets.ModelViewSet):
    """API endpoint for Posts."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'


class CategoryAPIViewSet(viewsets.ModelViewSet):
    """API endpoint for Categories."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class TagAPIViewSet(viewsets.ModelViewSet):
    """API endpoint for Tags."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'slug'


class SubscriberAPIViewSet(viewsets.ModelViewSet):
    """API endpoint for Subscribers."""

    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
    permission_classes = [IsAdminUser | SubscribePermission, ]


class PostByCategoryAPIView(generics.ListAPIView):
    """API endpoint for retrieving Posts by Category."""

    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['slug'])


class PostByTagAPIView(generics.ListAPIView):
    """API endpoint for retrieving Posts by Tag."""

    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(tag__slug=self.kwargs['slug'])


class PostCommentsAPIView(generics.ListCreateAPIView):
    """API endpoint for retrieving and creating Comments for a Post."""

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def get_queryset(self):
        return Comment.objects.filter(post__slug=self.kwargs['slug'])
