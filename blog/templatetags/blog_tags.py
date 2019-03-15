from ..models import *
from django import template
from django.db.models import Count

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
    base_url = 'http://www.eastnotes.com'
    return base_url

@register.simple_tag
def get_posts_tags():
    tags = Tag.objects.annotate(posts_count=Count('post')).order_by('-posts_count')
    return tags

@register.simple_tag
def get_books_tags():
    tags = BookTag.objects.annotate(books_count=Count('book')).order_by('-books_count')
    return tags