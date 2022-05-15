from django import template
from ..models import Post

register = template.Library()


@register.simple_tag
def total_post():
    return Post.objects.filter(status="published").count()


@register.inclusion_tag('blog/post/latest_post.html')
def show_latest_post(count=3):
    latest_post=Post.objects.filter(status="published").order_by("-publish")[:count]
    return {"latest_post":latest_post}