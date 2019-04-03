"""djangoblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from blog import views
from . import views
import xadmin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path,include
urlpatterns = [
    path('admin/', xadmin.site.urls,name="admin"),
    path('', include('blog.urls')),
    path('search/', include('haystack.urls')),
    path('mdeditor/', include('mdeditor.urls')),
    path('comment/', include('comment.urls')),
]

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # import debug_toolbar
    # urlpatterns.append(url(r'^__debug__/', include(debug_toolbar.urls)))
