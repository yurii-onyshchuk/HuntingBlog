from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

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


def _like(request, model):
    obj = get_object_or_404(model, id=request.POST['obj_id'])
    action_result = click_like(obj, request.user)
    total_like = obj.total_like
    return JsonResponse({'action_result': action_result, 'total_like': total_like})
