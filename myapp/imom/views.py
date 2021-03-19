from django.shortcuts import render
from imom.models import User, Userinfo, Audiofiles, transcript_summary
from django.contrib.auth.models import auth
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from gensim.summarization.summarizer import summarize
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from fpdf import FPDF


# Create your views here.

global_audiopath = ""

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
                auth_obj = auth.authenticate(username=email, password=password)
                auth.login(request, auth_obj)
                return HttpResponseRedirect(reverse('myaccount'))
            else:
                alertvar = 1
                return render(request, "imom/Sign-in.html", context={'alertvar': alertvar})

        # FOR LOGIN IN
        if 'signin' in request.POST:
            auth_obj = auth.authenticate(username=email, password=password)
            if auth_obj is not None:
                auth.login(request, auth_obj)
                return HttpResponseRedirect(reverse('upload_audio'))
            else:
                alertvar = 2
                return render(request, "imom/Sign-in.html", context={'alertvar': alertvar})

    else:
        global global_audiopath
        global_audiopath=""
        return render(request, "imom/Sign-in.html")

def upload_audio(request):
    if request.method == 'POST':
        if 'uploadbtn' in request.POST:
            audiofile = request.FILES['audiofile']
            # print(request.user,audiofile)
            audiopath = "media/" + audiofile.name
            print("audiopath", audiopath)
            try:
                audio_existed_or_not = Audiofiles.objects.get(user=request.user, audio=audiopath)
            except Audiofiles.DoesNotExist:
                audio_existed_or_not = None
                global global_audiopath
                global_audiopath = audiopath
                print(audio_existed_or_not)
            if audio_existed_or_not is not None:
                localvar = 2
                return render(request, "imom/upload_audio.html", context={'localvar': localvar, 'audiopath': None})
            else:
                audio_obj = Audiofiles(user=request.user)
                audio_obj.audio_name = audiofile.name
                audio_obj.audio = audiofile
                audio_obj.save()
                localvar = 1
                latest_audio = Audiofiles.objects.last()
                print(latest_audio.audio)
                return render(request, "imom/upload_audio.html", context={'localvar': localvar, 'audiopath': latest_audio.audio})
        if 'generate_t' in request.POST:
            localvar = 3
            return render(request, "imom/upload_audio.html", context={'localvar': localvar, 'audiopath': global_audiopath})
        # if 'summarybtn' in request.POST:
        #     if global_audiopath:
        #         text1 = "Hello, people from the future! Welcome to Normalized Nerd! I love to create educational videos on Machine Learning and Creative Coding. Machine learning and Data Science have changed our world dramatically and will continue to do so. But how they exactly work?...Find out with me. If you like my videos please subscribe to my channel."
        #         print(summarize(text1, ratio=0.5))
        #         trans_summ_obj = transcript_summary(user=request.user, audio=global_audiopath)
        #         trans_summ_obj.summary = summarize(text1, ratio=0.5)
        #         trans_summ_obj.save()
        #     localvar = 3
        #     return render(request, "imom/upload_audio.html", context={'localvar': localvar, 'audiopath': global_audiopath})
    else:
        localvar = 0
        return render(request, "imom/upload_audio.html", context={'localvar': localvar})


class Forhistory:
    audio_name = ""
    number = 0
    def __init__(self, a,n):
        self.audio_name = a
        self.number = n


def history(request):
    if request.method == "POST":
            return render(request, "imom/history.html")
    else:
        global global_audiopath
        global_audiopath=""
        Audiofiles_obj = Audiofiles.objects.filter(user=request.user)
        Finallist = []
        n = 0
        for i in Audiofiles_obj:
            try:
                trans_summ_existed_or_not = transcript_summary.objects.get(user=request.user, audio=i.audio)
            except transcript_summary.DoesNotExist:
                trans_summ_existed_or_not = None
            if trans_summ_existed_or_not is None:
                n = 1
            else:
                if not trans_summ_existed_or_not.summary:
                    n = 2
                elif trans_summ_existed_or_not.summary:
                    n = 3
            # print(n)
            OBJ = Forhistory(i.audio_name, n)
            Finallist.append(OBJ)
        return render(request, "imom/history.html", context={'Audiofiles_obj': Finallist})


def preview(request, id=0, id1=1):
    if request.method == "GET":
        All_audio = Audiofiles.objects.filter(user=request.user)
        # print("id",id,"id1",id1)
        # print(All_audio[int(id)-1].audio_name)
        i = 0
        if int(id) == 0:
            i = len(All_audio)-1
        else:
            i = int(id)-1
        if int(id1) == 1:
            try:
                trans_Obj = transcript_summary.objects.get(user=request.user, audio=All_audio[i].audio)
            except transcript_summary.DoesNotExist:
                trans_Obj = None
            if trans_Obj is None:
                Trans_Obj = transcript_summary(user=request.user, audio=All_audio[i].audio)
                Trans_Obj.transcript = "dsajbaskjdb bdsakbdaskjdas dsbakjbadskjdsa hjksandsa"
                Trans_Obj.save()
                return render(request, "imom/preview.html", context={"identifier": id,'text_transcript': Trans_Obj.transcript,'text_summary': ""})
            return render(request, "imom/preview.html", context={"identifier": id,'text_transcript': trans_Obj.transcript,'text_summary': ""})
        elif int(id1) == 2:
            Trans_Obj = transcript_summary.objects.get(user=request.user, audio=All_audio[i].audio)
            buffer = io.BytesIO()
            # Create the PDF object, using the buffer as its "file."
            p = canvas.Canvas(buffer)
            p.setFont("Times-Roman", 15)
            p.setTitle("Transcript")
            p.drawCentredString(300, 785, All_audio[i].audio_name)
            p.drawString(100, 690, Trans_Obj.transcript)
            p.showPage()
            p.save()
            # FileResponse sets the Content-Disposition header so that browsers
            # present the option to save the file.
            buffer.seek(0)
            return FileResponse(buffer, as_attachment=True, filename='Transcript.pdf')
        elif int(id1) == 3:
            Trans_Obj = transcript_summary.objects.get(user=request.user, audio=All_audio[i].audio)
            Trans_Obj.summary = "adsbdsamn dshjkasd hdsakjhads hsdakjdsa"
            Trans_Obj.save()
            return render(request, "imom/preview.html", context={"identifier": id,'text_transcript': Trans_Obj.transcript, 'text_summary': Trans_Obj.summary})
        elif int(id1) == 4:
            Trans_Obj = transcript_summary.objects.get(user=request.user, audio=All_audio[i].audio)
            buffer = io.BytesIO()
            p = canvas.Canvas(buffer)
            p.setFont("Times-Roman", 15)
            p.setTitle("SUMMARY")
            p.drawCentredString(300, 785, All_audio[i].audio_name)
            p.drawString(100, 690, Trans_Obj.summary)
            p.showPage()
            p.save()
            buffer.seek(0)
            return FileResponse(buffer, as_attachment=True, filename='Summary.pdf')


def myaccount(request):
    if request.method == "GET":
        global global_audiopath
        global_audiopath=""
        return render(request, "imom/myaccount.html", context={'user_name':request.user.username})


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return HttpResponseRedirect(reverse('sign'))
