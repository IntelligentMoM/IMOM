from django.contrib import admin

# Register your models here.
from imom.models import Userinfo, Audiofiles

admin.site.register(Userinfo)
admin.site.register(Audiofiles)
