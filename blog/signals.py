import os

from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.template.loader import get_template

from .models import Post, Subscriber


@receiver(post_save, sender=Post)
def notification(sender, instance, created, **kwargs):
    """Send email notifications to subscribers when a new post is created, if the post is set to notify subscribers.

    Args:
        sender: The sender of the signal.
        instance (Post): The instance of the Post model that was saved.
        created (bool): A boolean indicating if the instance was just created.
        kwargs: Additional keyword arguments.

    When a new post is created and the `notify_subscribers` field of the post is set to `True`, this signal handler sends
    email notifications to all subscribers. The email contains a subject and an HTML message rendered from a template.

    The email is sent from the email address specified in the environment variable 'EMAIL_HOST_USER' to all subscribers
    listed in the database. The context for rendering the HTML message includes the admin email address and the new post.
    """

    if created and instance.notify_subscribers:
        subscribers = Subscriber.objects.all()
        subject = 'Новий допис у нашому блозі'
        from_email = os.getenv('EMAIL_HOST_USER')
        recipient_list = [subscriber.email for subscriber in subscribers]
        context = {'admin_email': os.getenv('EMAIL_HOST_USER'),
                   'post': instance}
        html_message = get_template('blog/email/newsletter.html').render(context)
        send_mail(subject=subject, message='', from_email=from_email, recipient_list=recipient_list,
                  html_message=html_message)
