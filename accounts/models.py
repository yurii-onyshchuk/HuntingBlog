from django.db import models
from autoslug import AutoSlugField
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(_("email address"), blank=False)
    slug = AutoSlugField(populate_from='username', verbose_name='URL', unique=True)
    photo = models.ImageField(upload_to='photos/accounts/%Y/%m', blank=True, verbose_name='Основна світлина')

    class Meta:
        verbose_name = 'Користувач'
        verbose_name_plural = 'Користувачі'

    def __str__(self):
        return str(self.username)

