from django.shortcuts import render,get_object_or_404,HttpResponse,HttpResponseRedirect
from .models import *
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage
import markdown
from django.db.models import Count

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

    return render(request, 'blog/index.html', {'posts': posts,'boxposts':boxposts,})

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
    return render(request, 'blog/article.html', {'post': post,'author': author,'category': category,'relativa_posts':relative_posts})

def archives(request):
    posts = Post.objects.all().order_by('-created_time')
    post_count = Post.objects.all().count()
    category_count = Category.objects.all().count()
    tag_count = Tag.objects.all().count()
    return render(request,'blog/archives.html',{'posts':posts,'post_count':post_count,'category_count':category_count,'tag_count':tag_count,})

#全站所有的标签
def tags(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tags.html', {'tags':tags})

#每个标签下的所有文章
def tag_list(request,pk):
    tag = get_object_or_404(Tag, pk=pk)
    posts = Post.objects.filter(tag=tag).order_by('-created_time')
    tag_name = tag.name
    #分页
    paginator = Paginator(posts, 5)  # 每页显示1条数据
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)  # 1是指当前现实的是第一页
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)  # paginator.num_pages为分页后的总页数
    return render(request,'blog/tag_list.html',{'posts':posts,'tag_name':tag_name})

#分类下的所有文章
def category(request,pk):
    cate = get_object_or_404(Category, pk=pk)
    cat_name = cate.name
    posts = Post.objects.filter(category=cate).order_by('created_time')
    paginator = Paginator(posts, 5)  # 每页显示1条数据
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)  # 1是指当前现实的是第一页
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)  # paginator.num_pages为分页后的总页数
    return render(request,'blog/category.html',{'posts':posts,'cate_name':cat_name})


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
    return render(request,'blog/categories.html',{'posts':posts,})

def books(request):
    books = Book.objects.all()
    tags = BookTag.objects.annotate(posts_count = Count('book')).order_by('-posts_count')
    return render(request,'blog/books.html',{'books':books,'tags':tags})

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
    tags = BookTag.objects.annotate(posts_count = Count('book')).order_by('-posts_count')
    return render(request,'blog/book_detail.html',{'book':book,'tags':tags,})

def book_list(request,pk):
    tag = get_object_or_404(BookTag,pk=pk)
    books = Book.objects.filter(tag = tag)
    tag_name = tag.name
    return render(request,'blog/book_list.html',{"books":books,'tag_name':tag_name,})


def movies(request):
    movies = Movie.objects.all()
    tags = MovieTag.objects.annotate(movies_count = Count('movie')).order_by("-movies_count")
    return render(request,'blog/movies.html',{'movies':movies,'tags':tags,})

def movie_list(request,pk):
    tag = get_object_or_404(MovieTag,pk=pk)
    movies = Movie.objects.filter(tag=tag)
    tag_name = tag.name
    return render(request,'blog/movie_list.html',{'movies':movies,'tag_name':tag_name,})

def movie_detail(request,pk):
    movie = get_object_or_404(Movie,pk=pk)
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    movie.detail = md.convert(movie.detail)
    movie.toc = md.toc
    movie.increase_views()  # 阅读量加1

    tags = MovieTag.objects.annotate(movies_count = Count('movie')).order_by('-movies_count')
    return render(request,'blog/movie_detail.html',{'movie':movie,'tags':tags,})

