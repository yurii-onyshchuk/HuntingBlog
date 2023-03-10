"""HuntingBlog URL Configuration

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
from django.urls import path

from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('category/<str:slug>', views.PostsByCategory.as_view(), name='category'),
    path('tag/<str:slug>', views.PostsByTag.as_view(), name='tag'),
    path('post/<str:slug>', views.SinglePost.as_view(), name='post'),
    path('search/', views.Search.as_view(), name='search'),
    path('contact/', views.contact, name='contact'),
    path('like-post/', views.like_post, name='like_post'),
    path('like-comment/', views.like_comment, name='like_comment'),
    path('subscribe/', views.subscribe, name='subscribe'),
]
