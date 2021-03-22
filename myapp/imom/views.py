from django.shortcuts import render
from imom.models import User, Userinfo, Audiofiles, transcript_summary, User_All_Details
from django.contrib.auth.models import auth
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from gensim.summarization.summarizer import summarize
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from textwrap import wrap
import spacy
from spacy.lang.en import English
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
import subprocess


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
        if request.user.is_authenticated:
            localvar = 0
            return render(request, "imom/upload_audio.html", context={'localvar': localvar})
        else:
            return HttpResponseRedirect(reverse("sign"))


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
        if request.user.is_authenticated:
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
        else:
            return HttpResponseRedirect(reverse("sign"))


# def generate_summary(text):
#     stopwords = list(STOP_WORDS)
#     nlp = spacy.load('en_core_web_sm')
#     doc = nlp(text)
#
#     word_frequencies = {}
#     for word in doc:
#         if word.text.lower() not in stopwords:
#             if word.text.lower() not in punctuation:
#                 if word.text not in word_frequencies.keys():
#                     word_frequencies[word.text] = 1
#                 else:
#                     word_frequencies[word.text] += 1
#
#     max_frequency = max(word_frequencies.values())
#     for word in word_frequencies.keys():
#         word_frequencies[word] = word_frequencies[word]/max_frequency
#
#     sentence_tokens = [sent for sent in doc.sents]
#     sentence_scores = {}
#     for sent in sentence_tokens:
#         for word in sent:
#             if word.text.lower() in word_frequencies.keys():
#                 if sent not in sentence_scores.keys():
#                     sentence_scores[sent] = word_frequencies[word.text.lower()]
#                 else:
#                     sentence_scores[sent] += word_frequencies[word.text.lower()]
#
#
#
#     select_length = int(len(sentence_tokens)*0.5)
#     summary = nlargest(select_length, sentence_scores, key=sentence_scores.get)
#     final_summary = [word.text for word in summary]
#     summary = ''.join(final_summary)
#     return summary

def preview(request, id=0, id1=1):
    if request.method == "GET":
        if request.user.is_authenticated:
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
                    print("here")
                    Trans_Obj = transcript_summary(user=request.user, audio=All_audio[i].audio)
                    Trans_Obj.transcript = "Hello, people from the future! Welcome to Normalized Nerd! I love to create educational videos on Machine Learning and Creative Coding. Machine learning and Data Science have changed our world dramatically and will continue to do so. But how they exactly work?...Find out with me. If you like my videos please subscribe to my channel."
                    Trans_Obj.save()
                    return render(request, "imom/preview.html", context={"identifier": id, 'audio_name': All_audio[i].audio_name, 'text_transcript': Trans_Obj.transcript,'text_summary': ""})
                return HttpResponseRedirect(reverse("upload_audio"))
            elif int(id1) == 2:
                Trans_Obj = transcript_summary.objects.get(user=request.user, audio=All_audio[i].audio)
                buffer = io.BytesIO()
                # Create the PDF object, using the buffer as its "file."
                p = canvas.Canvas(buffer)
                t = p.beginText(50,690)
                t.setFont("Times-Roman", 15)
                p.setTitle("Transcript")
                p.drawCentredString(300, 785, All_audio[i].audio_name)
                wraped_text = "\n".join(wrap(Trans_Obj.transcript, 80))
                #print(wraped_text)
                t.textLines(wraped_text)
                p.drawText(t)
                p.showPage()
                p.save()
                # FileResponse sets the Content-Disposition header so that browsers
                # present the option to save the file.
                buffer.seek(0)
                return FileResponse(buffer, as_attachment=True, filename='Transcript.pdf')
            elif int(id1) == 3:
                Trans_Obj = transcript_summary.objects.get(user=request.user, audio=All_audio[i].audio)
                Trans_Obj.summary = summarize(Trans_Obj.transcript, ratio=0.5)
                Trans_Obj.save()
                return render(request, "imom/preview.html", context={"identifier": id, 'audio_name': All_audio[i].audio_name, 'text_transcript': Trans_Obj.transcript, 'text_summary': Trans_Obj.summary})
            elif int(id1) == 4:
                Trans_Obj = transcript_summary.objects.get(user=request.user, audio=All_audio[i].audio)
                buffer = io.BytesIO()
                p = canvas.Canvas(buffer)
                t = p.beginText(50,690)
                t.setFont("Times-Roman", 15)
                p.setTitle("SUMMARY")
                print("Hello")
                p.drawCentredString(300, 785, All_audio[i].audio_name)
                wraped_text = "\n".join(wrap(Trans_Obj.summary, 80))
                #print(wraped_text)
                t.textLines(wraped_text)
                p.drawText(t)
                p.showPage()
                p.save()
                buffer.seek(0)
                return FileResponse(buffer, as_attachment=True, filename='Summary.pdf')
        else:
            return HttpResponseRedirect(reverse("sign"))


def myaccount(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            global global_audiopath
            global_audiopath=""
            try:
                user_obj = User_All_Details.objects.get(user=request.user)
            except User_All_Details.DoesNotExist:
                user_obj = None
            return render(request, "imom/myaccount.html", context={'user_name':request.user.username, 'user_obj':user_obj})
        else:
            return HttpResponseRedirect(reverse("sign"))
    elif request.method == "POST":
        try:
            user_obj = User_All_Details.objects.get(user=request.user)
        except User_All_Details.DoesNotExist:
            user_obj = None
        if user_obj is None:
            user_obj = User_All_Details(user=request.user)
        user_obj.first_name = request.POST.get('firstname')
        user_obj.second_name = request.POST.get('surname')
        user_obj.contact = request.POST.get('contactnumber')
        user_obj.save()
        return HttpResponseRedirect(reverse('upload_audio'))

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return HttpResponseRedirect(reverse('sign'))

def readtags(meetingid):
    p=Popen("imom/Transcript/speakerDiarization.py",shell=True,stdout=PIPE,stdin=PIPE) # create a child process
    raw = p.communicate(bytes(input, 'UTF-8'))[0]  # gives raw bytes
    tags = raw.decode()
     # write to the file
     # change name to imom/a.txt for trail
    with open("tags/{}".format(meetingid), 'w', encoding='utf-8') as f:
        f.write(tags)
        
     # read tags from file
     print_tags 
     with open("tags/{}".format(meetingid), 'w', encoding='utf-8') as f:
       print_tags= f.read()
     
    
    

