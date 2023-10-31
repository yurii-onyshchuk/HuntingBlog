import os
import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.db.models import F, Q
from django.http import HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin

from .forms import CommentForm
from .models import Post, Category, Tag, Comment, Subscriber
from .services.likes_system import click_like


class PostList(ListView):
    """List view for blog posts."""

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
    """List view for blog posts filtered by category."""

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug']).title
        return context


class PostsByTag(PostList):
    """List view for blog posts filtered by tag."""

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Tag.objects.get(slug=self.kwargs['slug']).title
        return context


class Search(PostList):
    """List view for blog posts filtered by search query."""

    allow_empty = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Результати пошуку'
        context['q'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        q = self.request.GET.get('q')
        return Post.objects.filter(Q(title__icontains=q) | Q(content__icontains=q))


class SinglePost(FormMixin, DetailView):
    """Detail view for a single blog post."""

    model = Post
    form_class = CommentForm

    def get_context_data(self, *, object_list=None, **kwargs):
        """Get the context data for the single blog post.

        This method is extended to update a post's view count and
        pass post comments to the context
        """

        context = super().get_context_data()
        context['title'] = self.object.title

        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()

        _list = Comment.objects.filter(post__slug=self.kwargs.get('slug'), parent__isnull=True)
        paginator = Paginator(_list, 10)
        page = self.request.GET.get('page')
        context['comments'] = paginator.get_page(page)

        return context

    def post(self, request, *args, **kwargs):
        """Handle the HTTP POST request to add a comment to the blog post.
        Redirect to the current blog post with the comment anchor.
        """
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
        """Get the URL to redirect to after successfully submitting a comment."""
        return reverse_lazy('post', kwargs={'slug': self.kwargs['slug']})


def contact(request):
    """View for page with a contact information."""
    context = {'title': 'Контактна інформація'}
    return render(request, 'blog/contacts.html', context)


@login_required
def like_post(request):
    """View for liking/unliking a post."""
    return click_like(request, Post)


@login_required
def like_comment(request):
    """View for liking/unliking a comment."""
    return click_like(request, Comment)


def subscribe(request):
    """View function for subscribing to a newsletter."""
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
