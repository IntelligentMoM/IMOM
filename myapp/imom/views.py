from django.shortcuts import render
from imom.models import User,Userinfo,Audiofiles
from django.contrib.auth.models import auth
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse


# Create your views here.

def sign(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        print(email, password)

        # FOR SIGN UP
        if 'signup' in request.POST:
            try:
                user_already_exist_or_not = User.objects.get(username=email)
            except User.DoesNotExist:
                user_already_exist_or_not = None
            if user_already_exist_or_not is None:
                user_created = User.objects.create_user(username=email, password=password)
                user_created.save()
                userinfo_obj = Userinfo()
                userinfo_obj.user = user_created
                userinfo_obj.save()
            else:
                alertvar = 1
                return render(request, "imom/Sign-in.html", context={'alertvar': alertvar})

        # FOR LOGIN IN
        auth_obj = auth.authenticate(username=email, password=password)
        if auth_obj is not None:
            auth.login(request,auth_obj)
            return HttpResponseRedirect(reverse('upload_audio'))
        else:
            alertvar = 2
            return render(request, "imom/Sign-in.html", context={'alertvar': alertvar})

    else:
        return render(request, "imom/Sign-in.html")

def upload_audio(request):
    if request.method == 'POST':
        audiofile = request.FILES['audiofile']
        print(request.user,audiofile)
        audiopath = "media/"+audiofile.name
        try:
            audio_existed_or_not = Audiofiles.objects.get(user=request.user, audio=audiopath)
        except Audiofiles.DoesNotExist:
            audio_existed_or_not = None
            print(audio_existed_or_not)
        if audio_existed_or_not is not None:
            localvar = 2
        else:
            audio_obj = Audiofiles(user=request.user)
            audio_obj.audio = audiofile
            audio_obj.save()
            localvar = 1
        latest_audio = Audiofiles.objects.last()
        print(latest_audio.audio)
        return render(request, "imom/upload_audio.html", context={'localvar':localvar,'audiopath':latest_audio.audio})
    else:
        localvar = 0
        return render(request, "imom/upload_audio.html", context={'localvar':localvar})


def history(request):
    return render(request, "imom/history.html")

def myaccount(request):
    return render(request,"imom/myaccount.html")

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return HttpResponseRedirect(reverse('sign'))
