from django.contrib import admin

# Register your models here.
from imom.models import Userinfo, Audiofiles, transcript_summary, User_All_Details

admin.site.register(Userinfo)
admin.site.register(Audiofiles)
admin.site.register(transcript_summary)
admin.site.register(User_All_Details)
