from django.shortcuts import render


def index(request):
    return render(request, 'blog/index.html')


def get_category(request):
    return render(request, 'blog/category.html')


def get_post(request):
    return render(request, 'blog/post.html')
