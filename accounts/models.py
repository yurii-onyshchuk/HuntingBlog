from django.db import models
from autoslug import AutoSlugField
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from PIL import Image


class User(AbstractUser):
    email = models.EmailField(_("email address"), blank=False)
    slug = AutoSlugField(populate_from='username', verbose_name='URL', unique=True)
    photo = models.ImageField(upload_to='photos/accounts/%Y/%m', blank=False, verbose_name='Основна світлина')

    class Meta:
        verbose_name = 'Користувач'
        verbose_name_plural = 'Користувачі'

    def __str__(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        else:
            return str(self.username)

    def save_thumbnail(self):
        super().save()
        photo = Image.open(self.photo.path)
        if photo.height > 200 or photo.width > 200:
            output_size = (200, 200)
            photo.thumbnail(output_size)
            photo.save(self.photo.path)
