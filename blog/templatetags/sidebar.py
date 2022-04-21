from django import template
from blog.models import Post, Tag

register = template.Library()


@register.inclusion_tag('blog/popular_posts_tpl.html')
def show_posts_list(count=5):
    posts = Post.objects.order_by('-views')[:count]
    return {'posts': posts}


@register.simple_tag()
def show_tag_list():
    return Tag.objects.all()
