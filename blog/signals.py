import os

from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.template.loader import get_template

from .models import Post, Subscriber


@receiver(post_save, sender=Post)
def notification(sender, instance, created, **kwargs):
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
