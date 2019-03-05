from django.conf.urls import url,include
from . import views
app_name="blog"
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^archives/', views.archives,name='archives'),
    url(r'^tags/', views.tags,name='tags'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.article, name='article'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.category, name='category'),
    url(r'^categories/', views.categories, name='categories'),
    url(r'^tag_list/(?P<pk>[0-9]+)/$', views.tag_list, name='tag_list'),

]