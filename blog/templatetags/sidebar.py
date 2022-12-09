from django import template
from blog.models import Post, Tag, Category

register = template.Library()


@register.inclusion_tag('blog/popular_posts_tpl.html')
def show_posts_list(count=5):
    popular_posts = Post.objects.order_by('-views')[:count]
    recent_posts = Post.objects.order_by('-created_at')[:count]
    return {'popular_posts': popular_posts, 'recent_posts': recent_posts}


@register.simple_tag()
def show_tag_list():
    return Tag.objects.all()


@register.simple_tag()
def get_categories():
    return Category.objects.all()
