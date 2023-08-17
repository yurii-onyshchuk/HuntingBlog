"""ToDo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include, re_path

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register('posts', views.PostAPIViewSet, basename='posts')
router.register('categories', views.CategoryAPIViewSet, basename='categories')
router.register('tags', views.TagAPIViewSet, basename='tags')
router.register('comments', views.CommentsAPIViewSet, basename='comments')
router.register('subscribers', views.SubscriberAPIViewSet, basename='subscribers')

urlpatterns = [
    path('', include(router.urls)),
    path('category/<int:pk>/', views.PostByCategoryAPIView.as_view()),
    path('tag/<int:pk>/', views.PostByTagAPIView.as_view()),
    path('posts/<int:pk>/comments', views.PostCommentsAPIView.as_view()),
    # Session-based authentication
    path('drf-auth/', include('rest_framework.urls')),
    # Token-based authentication
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
