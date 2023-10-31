from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from blog.models import Like

User = get_user_model()


def click_like(request, model):
    """Process a user's like or unlike action on an object and return the updated like count."""
    obj = get_object_or_404(model, id=request.POST['obj_id'])
    obj_type = ContentType.objects.get_for_model(obj)
    like_obj, is_created = Like.objects.get_or_create(content_type=obj_type, object_id=obj.id, user=request.user)
    if is_created:
        action_result = 'added'
    else:
        like_obj.delete()
        action_result = 'removed'
    total_like = obj.total_like
    return JsonResponse({'action_result': action_result, 'total_like': total_like})
