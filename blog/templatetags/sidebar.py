from django import template
from django.db.models import Count

from blog.models import Post, Tag, Category

register = template.Library()


@register.inclusion_tag('blog/inc/_sidebar_posts_tpl.html')
def show_posts_list(count=5):
    """An inclusion tag that displays popular and recent blog posts in the sidebar.

    Args:
        count (int): The number of posts to display in each section (popular and recent). Default is 5.
    """
    popular_posts = Post.objects.order_by('-views')[:count]
    recent_posts = Post.objects.order_by('-created_at')[:count]
    return {'popular_posts': popular_posts, 'recent_posts': recent_posts}


@register.simple_tag()
def show_tag_list():
    """A simple tag that retrieves and displays tags
    that are associated with one or more blog posts.
    """
    return Tag.objects.annotate(num_posts=Count('posts')).filter(num_posts__gt=0)


@register.simple_tag()
def get_categories():
    """A simple tag that retrieves and displays categories
    that are associated with one or more blog posts.
    """
    return Category.objects.annotate(num_posts=Count('posts')).filter(num_posts__gt=0)
