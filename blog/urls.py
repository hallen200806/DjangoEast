from django.urls import path
from . import views
from django.conf import settings
# import debug_toolbar
app_name="blog"
urlpatterns = [
    path('', views.index, name='index'),

    path('archives/', views.archives,name='archives'),
    path('post/<int:pk>', views.article, name='article'),

    path('category/<int:pk>', views.category, name='category'),
    path('categories/', views.categories, name='categories'),

    path('tags/', views.tags,name='tags'),
    path('tag_list/<int:pk>', views.tag_list, name='tag_list'),

    path('books/', views.books, name='books'),
    path('book_detail/<int:pk>', views.book_detail, name='book_detail'),
    path('book_list/<int:pk>', views.book_list, name='book_list'),

    path('movies/', views.movies, name ='movies' ),
    path('movie_detail/<int:pk>', views.movie_detail, name='movie_detail'),
    path('movie_list/<int:pk>', views.movie_list, name='movie_list'),
]
