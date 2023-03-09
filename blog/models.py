from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

User = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=250, verbose_name='Заголовок')
    slug = models.SlugField(max_length=100, verbose_name='URL', unique=True)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts', verbose_name='Категорія')
    author = models.CharField(max_length=100, verbose_name='Автор')
    content = models.TextField(blank=True, verbose_name='Вміст')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публікації')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, verbose_name='Фото')
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts', verbose_name='Теги')
    views = models.IntegerField(default=0, verbose_name='Перегляди')
    notify_subscribers = models.BooleanField(verbose_name='Сповістити підписників', default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'slug': self.slug})

    def get_comment_count(self):
        return Comment.objects.filter(post=self, parent__isnull=True).count()

    class Meta:
        verbose_name = 'Стаття(ю)'
        verbose_name_plural = 'Статті'
        ordering = ['-created_at']


class Category(models.Model):
    title = models.CharField(max_length=250, verbose_name='Назва категорії')
    slug = models.SlugField(max_length=100, verbose_name='URL', unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'
        ordering = ['title']


class Tag(models.Model):
    title = models.CharField(max_length=50, verbose_name='Назва тегу')
    slug = models.SlugField(max_length=100, verbose_name='URL', unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tag', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['title']


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments', verbose_name='Пост')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                             related_name='user_comments', verbose_name='Користувач')
    body = models.TextField(verbose_name='Коментар')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата додавання')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies',
                               verbose_name='До коментаря')
    likes = GenericRelation('Like')

    def __str__(self):
        return self.body

    class Meta:
        verbose_name = 'Коментар'
        verbose_name_plural = 'Коментарі'
        ordering = ['-created_at']

    def get_user(self):
        if self.user:
            return self.user
        else:
            return "Видалений користувач"

    @property
    def children(self):
        return Comment.objects.filter(parent=self).reverse()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False

    @property
    def total_like(self):
        return self.likes.count()


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='likes', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Subscriber(models.Model):
    email = models.EmailField(unique=True, verbose_name='Електронна адреса')
    subscribed_at = models.DateTimeField(auto_now_add=True, verbose_name='Час підписки')

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Підписка на розсилку'
        verbose_name_plural = 'Підписки на розсилку'
        ordering = ['-subscribed_at']
