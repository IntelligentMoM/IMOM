"""myapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.conf.urls import url,include
from imom import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.sign, name="sign"),
    url(r'^upload_audio/', views.upload_audio, name="upload_audio"),
    url(r'^history/', views.history, name="history"),
    url(r'^preview/$', views.preview, name="preview"),
    url(r'^preview/(?P<id>\d+)/(?P<id1>\d+)/$', views.preview, name="preview"),
    url(r'^myaccount/', views.myaccount, name="myaccount"),
    url(r'^logout/', views.logout, name="logout"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
