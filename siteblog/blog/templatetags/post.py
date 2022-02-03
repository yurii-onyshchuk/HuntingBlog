from django import template
from blog.models import Post

register = template.Library()


@register.inclusion_tag('blog/post_tpl.html')
def show_post():
    posts = Post.objects.all()
    return {'posts': posts}
