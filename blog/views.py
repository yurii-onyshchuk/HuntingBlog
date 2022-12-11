import random

from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin

from .models import Post, Category, Tag, Comment
from .forms import CommentForm


class Home(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 8

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Головна'
        context['random_post'] = random.choice(self.get_queryset())
        return context


class PostsByCategory(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 8
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        context['random_post'] = random.choice(self.get_queryset())
        return context


class PostsByTag(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 8
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Tag.objects.get(slug=self.kwargs['slug'])
        context['random_post'] = random.choice(self.get_queryset())
        return context


class SinglePost(FormMixin, DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    form_class = CommentForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['title'] = Post.objects.get(slug=self.kwargs['slug'])
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        post = self.get_object()
        if form.is_valid():
            if request.POST.get('parent', None):
                form.instance.parent_id = int(request.POST.get('parent'))
            form.instance.post = post
            form.instance.user = self.request.user
            form.save()
        return redirect(post.get_absolute_url())

    def get_success_url(self):
        return reverse_lazy('post', kwargs={'slug': self.kwargs['slug']})


class Search(ListView):
    template_name = 'blog/search.html'
    context_object_name = 'posts'
    paginate_by = 8

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET.get('s'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = f"s={self.request.GET.get('s')}&"
        context['title'] = 'Результати пошуку'
        return context


def contact(request):
    context = {'title': 'Контактна інформація'}
    return render(request, 'blog/contacts.html', context)


@login_required
def like_comment(request):
    comment = get_object_or_404(Comment, id=request.POST['comment_id'])
    if comment.users_like.filter(username=request.user.username).exists():
        comment.users_like.remove(request.user)
        action_result = 'removed'
    else:
        comment.users_like.add(request.user)
        action_result = 'added'
    like_total = comment.users_like.count()
    return JsonResponse({'like_total': like_total, 'action_result': action_result})
