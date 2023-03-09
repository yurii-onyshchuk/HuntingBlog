from django import template
from django.contrib.contenttypes.models import ContentType

from blog.models import Like

register = template.Library()


@register.simple_tag()
def liked_users_ids(obj):
    content_type = ContentType.objects.get_for_model(obj)
    user_ids = Like.objects.filter(content_type=content_type, object_id=obj.id).values_list('user_id', flat=True)
    return user_ids
