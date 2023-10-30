import re

from django import template
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from blog.models import Like

register = template.Library()


@register.simple_tag()
def liked_users_ids(obj):
    """A template tag that retrieves the IDs of users who have liked a specific object.

    Args:
        obj: The object for which you want to retrieve the user IDs who liked it.
    Returns:
        list: A list of user IDs who liked the object.
    """
    content_type = ContentType.objects.get_for_model(obj)
    user_ids = Like.objects.filter(content_type=content_type, object_id=obj.id).values_list('user_id', flat=True)
    return user_ids


@register.inclusion_tag('blog/inc/_like_tpl.html', takes_context=True)
def like_button(context, obj, url):
    """An inclusion tag that renders a like button for a specific object.

    Args:
        context (Context): The template context.
        obj: The object for which you want to render the like button.
        url (str): The URL pattern name for the like action.
    Returns:
        dict: A dictionary containing the object, URL, and user in the context.
    """
    url = reverse(f'like_{url}')
    user = context['request'].user
    return {'obj': obj, 'url': url, 'user': user}


@register.filter()
def remove_iframe(content):
    """A template filter that removes iframe tags from the content.

    Args:
        content (str): The content containing HTML tags.
    Returns:
        str: The content with iframe tags removed.
    """
    return re.sub("(<iframe.*?>)", "", content)
