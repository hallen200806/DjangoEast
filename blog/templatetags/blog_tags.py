from ..models import *
from django import template

register = template.Library()

# 返回文章总量
@register.simple_tag
def get_total_posts():
    posts = Post.objects.all()
    posts_number = posts.count()
    return posts_number

# 返回分类总量
@register.simple_tag
def get_total_categories():
    categories = Category.objects.all()
    category_number = categories.count()
    return category_number

# 返回标签总量
@register.simple_tag
def get_total_tags():
    tags = Tag.objects.all()
    tags_number = tags.count()
    return tags_number

@register.simple_tag
def base_url():
    base_url = 'http://127.0.0.1:8000'
    return base_url