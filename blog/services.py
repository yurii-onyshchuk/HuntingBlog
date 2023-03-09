from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from .models import Like

User = get_user_model()


def click_like(obj, user):
    obj_type = ContentType.objects.get_for_model(obj)
    like_obj, is_created = Like.objects.get_or_create(content_type=obj_type, object_id=obj.id, user=user)
    if is_created:
        action_result = 'added'
    else:
        like_obj.delete()
        action_result = 'removed'
    return action_result
