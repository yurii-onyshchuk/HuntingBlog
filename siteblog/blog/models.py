from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=250, verbose_name='Назва категорії')
    slug = models.SlugField(max_length=100, verbose_name='URL', unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'
        ordering = ['title']


class Tag(models.Model):
    title = models.CharField(max_length=50, verbose_name='Назва тегу')
    slug = models.SlugField(max_length=100, verbose_name='URL', unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['title']


class Post(models.Model):
    title = models.CharField(max_length=250, verbose_name='Заголовок посту')
    slug = models.SlugField(max_length=100, verbose_name='URL', unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts')
    author = models.CharField(max_length=100, verbose_name='Автор посту')
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публікації')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, verbose_name='Фото')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    views = models.IntegerField(default=0, verbose_name='Кількість переглядів')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Пости'
        ordering = ['-created_at']
