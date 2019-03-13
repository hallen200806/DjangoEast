from django.shortcuts import render,get_object_or_404
from .models import *
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage
import markdown
from django.views.decorators.cache import cache_page

def index(request):
    posts = Post.objects.all().order_by('-created_time')
    boxposts = posts.filter(category_id__in=[1,2]).order_by('category_id') #首页文章框中的文章聚合
    paginator = Paginator(posts,5) #每页显示几条数据
    page = request.GET.get('page')
    try:
        posts = paginator.page(page) # 1是指当前现实的是第一页
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages) #paginator.num_pages为分页后的总页数
    return render(request, 'blog/index.html', context={'posts': posts,'boxposts':boxposts})

def article(request, pk):
    post = get_object_or_404(Post, pk=pk)
    author = User.objects.get(id=post.author_id)
    category = Category.objects.get(id=post.category_id)
    post.increase_views() # 阅读量加1
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    post.body = md.convert(post.body)
    post.toc = md.toc

    #获取相关文章
    relative_posts = Post.objects.filter(category_id=post.category_id).exclude(pk = pk).order_by('?')[:4]
    return render(request, 'blog/article.html', context={'post': post,'author': author,'category': category,'relativa_posts':relative_posts})

def archives(request):
    posts = Post.objects.all().order_by('-created_time')
    post_count = Post.objects.all().count()
    category_count = Category.objects.all().count()
    tag_count = Tag.objects.all().count()
    return render(request,'blog/archives.html',context={'posts':posts,'post_count':post_count,'category_count':category_count,'tag_count':tag_count})

#全站所有的标签
def tags(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tags.html', context={'tags':tags})

#每个标签下的所有文章
def tag_list(request,pk):
    tag = get_object_or_404(Tag, pk=pk)
    posts = Post.objects.filter(tag=tag).order_by('-created_time')

    #分页
    paginator = Paginator(posts, 5)  # 每页显示1条数据
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)  # 1是指当前现实的是第一页
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)  # paginator.num_pages为分页后的总页数
    return render(request,'blog/tag_list.html',context={'posts':posts})

#分类下的所有文章
def category(request,pk):
    cate = get_object_or_404(Category, pk=pk)
    posts = Post.objects.filter(category=cate).order_by('created_time')
    paginator = Paginator(posts, 5)  # 每页显示1条数据
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)  # 1是指当前现实的是第一页
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)  # paginator.num_pages为分页后的总页数
    return render(request,'blog/category.html',context={'posts':posts})


def categories(request):
    posts = Post.objects.all()
    # paginator = Paginator(posts, 1000)  # 每页显示1条数据
    # page = request.GET.get('page')
    # try:
    #     posts = paginator.page(page)  # 1是指当前现实的是第一页
    # except PageNotAnInteger:
    #     posts = paginator.page(1)
    # except EmptyPage:
    #     posts = paginator.page(paginator.num_pages)  # paginator.num_pages为分页后的总页数
    return render(request,'blog/categories.html',context={'posts':posts})

def books(request):
    books = Book.objects.all()
    return render(request,'blog/books.html',context={'books':books})

def book_detail(request,pk):
    book = get_object_or_404(Book,pk=pk)
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    book.detail = md.convert(book.detail)
    book.toc = md.toc
    book.increase_views()  # 阅读量加1

    return render(request,'blog/book_detail.html',context={'book':book})
