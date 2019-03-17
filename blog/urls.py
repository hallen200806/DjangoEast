from django.conf.urls import url,include
from . import views
from django.conf import settings
# import debug_toolbar
app_name="blog"
urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^archives/', views.archives,name='archives'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.article, name='article'),

    url(r'^category/(?P<pk>[0-9]+)/$', views.category, name='category'),
    url(r'^categories/', views.categories, name='categories'),

    url(r'^tags/', views.tags,name='tags'),
    url(r'^tag_list/(?P<pk>[0-9]+)/$', views.tag_list, name='tag_list'),

    url(r'^books/', views.books, name='books'),
    url(r'^book_detail/(?P<pk>[0-9]+)/$', views.book_detail, name='book_detail'),
    url(r'^book_list/(?P<pk>[0-9]+)/$', views.book_list, name='book_list'),

    url(r'movies/', views.movies, name ='movies' ),
    url(r'^movie_detail/(?P<pk>[0-9]+)/$', views.movie_detail, name='movie_detail'),
    url(r'^movie_list/(?P<pk>[0-9]+)/$', views.movie_list, name='movie_list'),
]
