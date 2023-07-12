import re

from django import template
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from blog.models import Like

register = template.Library()


@register.simple_tag()
def liked_users_ids(obj):
    content_type = ContentType.objects.get_for_model(obj)
    user_ids = Like.objects.filter(content_type=content_type, object_id=obj.id).values_list('user_id', flat=True)
    return user_ids


@register.inclusion_tag('blog/inc/_like_tpl.html', takes_context=True)
def like_button(context, obj, url):
    url = reverse(f'like_{url}')
    user = context['request'].user
    return {'obj': obj, 'url': url, 'user': user}


@register.filter()
def remove_iframe(content):
    return re.sub("(<iframe.*?>)", "", content)
