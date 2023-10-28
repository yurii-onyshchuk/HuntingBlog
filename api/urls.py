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
from .yasg import urlpatterns as doc_urls

router = DefaultRouter()

router.register('posts', views.PostAPIViewSet, basename='posts')
router.register('categories', views.CategoryAPIViewSet, basename='categories')
router.register('tags', views.TagAPIViewSet, basename='tags')
router.register('subscribers', views.SubscriberAPIViewSet, basename='subscribers')

urlpatterns = [
    path('', include(router.urls)),
    path('category/<str:slug>/', views.PostByCategoryAPIView.as_view(), name='posts_by_category'),
    path('tag/<str:slug>/', views.PostByTagAPIView.as_view(), name='posts_by_tag'),
    path('post/<str:slug>/comments/', views.PostCommentsAPIView.as_view(), name='post_comments'),

    # Session-based authentication
    path('drf-auth/', include('rest_framework.urls')),

    # Token-based authentication
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include(('djoser.urls.authtoken', 'authtoken'))),
]

# API documentation
urlpatterns += doc_urls
