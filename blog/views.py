import os
import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from django.http import HttpResponseNotAllowed

from .models import Post, Category, Tag, Comment, Subscriber
from .forms import CommentForm
from .services import click_like, _like


class PostList(ListView):
    model = Post
    paginate_by = 12
    allow_empty = False
    extra_context = {'title': 'Головна'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object_list:
            context['random_post'] = random.choice(self.object_list)
        return context


class PostsByCategory(PostList):
    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug']).title
        return context


class PostsByTag(PostList):
    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Tag.objects.get(slug=self.kwargs['slug']).title
        return context


class Search(PostList):
    allow_empty = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Результати пошуку'
        context['q'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET.get('q'))


class SinglePost(FormMixin, DetailView):
    model = Post
    form_class = CommentForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        _list = Comment.objects.filter(post__slug=self.kwargs.get('slug'), parent__isnull=True)
        paginator = Paginator(_list, 10)
        page = self.request.GET.get('page')
        context['comments'] = paginator.get_page(page)
        context['title'] = self.object.title
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
        return redirect(post.get_absolute_url() + '#comments')

    def get_success_url(self):
        return reverse_lazy('post', kwargs={'slug': self.kwargs['slug']})


def contact(request):
    context = {'title': 'Контактна інформація'}
    return render(request, 'blog/contacts.html', context)


@login_required
def like_post(request):
    return _like(request, Post)


@login_required
def like_comment(request):
    return _like(request, Comment)


def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('subscribe-email', None)
        if email:
            subscriber, created = Subscriber.objects.get_or_create(email=email)
            if created:
                messages.success(request, 'Підписка на розсилку новин успішно оформлена!')
                subject = "Підписка на розсилку"
                from_email = os.getenv('EMAIL_HOST_USER')
                recipient_list = [email]
                context = {'admin_email': os.getenv('EMAIL_HOST_USER')}
                html_message = get_template('blog/email/subscribe_email.html').render(context)
                send_mail(subject=subject, message='', from_email=from_email, recipient_list=recipient_list,
                          html_message=html_message)
            else:
                messages.warning(request, 'Вказана електронна адреса вже берете участь у розсилці новин!')
        return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return HttpResponseNotAllowed
