from django.apps import AppConfig


class BlogConfig(AppConfig):
    """Configuration class for the 'blog' app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    verbose_name = 'Блог'

    def ready(self):
        """Connecting signals for the 'blog' app."""
        from . import signals
