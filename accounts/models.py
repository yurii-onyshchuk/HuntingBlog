from PIL import Image

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from autoslug import AutoSlugField

from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

username_validator = UnicodeUsernameValidator()


class User(AbstractUser):
    """Custom user model with email and additional fields.

    This user model extends the AbstractUser and replaces the username
    with email as the unique identifier.
    """

    username = models.CharField(_("username"), max_length=150, unique=True, validators=[username_validator],
                                error_messages={"unique": _("A user with that username already exists."), })
    slug = AutoSlugField(populate_from='username', verbose_name='Slug', unique=True)
    email = models.EmailField(_("email"), unique=True)
    photo = models.ImageField(upload_to='photos/accounts/%Y/%m', blank=True, verbose_name='Основна світлина')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Користувач'
        verbose_name_plural = 'Користувачі'

    def __str__(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        else:
            return self.email

    def save_thumbnail(self):
        """Resizes and saves the user's profile photo as a thumbnail."""
        super().save()
        photo = Image.open(self.photo.path)
        if photo.height > 200 or photo.width > 200:
            output_size = (200, 200)
            photo.thumbnail(output_size)
            photo.save(self.photo.path)
