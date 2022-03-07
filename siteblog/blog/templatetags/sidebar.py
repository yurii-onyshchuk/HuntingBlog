from django import template
from blog.models import Post

register = template.Library()


@register.inclusion_tag('blog/popular_posts_tpl.html')
def show_posts_list(count=5):
    posts = Post.objects.order_by('-views')[:count]
    return {'posts': posts}
