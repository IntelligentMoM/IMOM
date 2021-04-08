from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.conf.urls import url,include
from main_app import views

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

