import json,datetime, os
from django.db.models import Q
from django.core import serializers
from django.http import HttpResponse
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.template.defaulttags import register as r
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User as UserModel
from .forms import UserRegistrationForm, UpdateUserForm, UpdateProfileForm, MessageForm
from .models import chatMessages, UserProfile


        
# Create your views here.
@login_required
def home(request):
    User = get_user_model()
    
    users = User.objects.all()
    chats = {}
    if request.method == 'GET' and 'u' in request.GET:
        # chats = chatMessages.objects.filter(Q(user_from=request.user.id & user_to=request.GET['u']) | Q(user_from=request.GET['u'] & user_to=request.user.id))
        chats = chatMessages.objects.filter(Q(user_from=request.user.id, user_to=request.GET['u']) | Q(user_from=request.GET['u'], user_to=request.user.id))
        chats = chats.order_by('date_created')
    context = {
        "page":"home",
        "users":users,
        "chats":chats,
        "chat_id": int(request.GET['u'] if request.method == 'GET' and 'u' in request.GET else 0)
    }
    print(request.GET['u'] if request.method == 'GET' and 'u' in request.GET else 0)
    return render(request,"chat/home.html",context)

def register(request):
    if request.method == 'POST':
       
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            user = UserModel.objects.get(username=username)
            profile = UserProfile(user=user)
            profile.save()
            messages.success(request,f'Account successfully created!')
            return redirect('chat-login')
        context = {
            "page":"register",
            "form" : form
        }
    else:
        context = {
            "page":"register",
            "form" : UserRegistrationForm()
        }
    return render(request,"chat/register.html",context)

@login_required
def profile(request, username):
    if request.method == 'POST':
        userform = UpdateUserForm(request.POST, instance=request.user)
        profileform = UpdateProfileForm(request.POST, request.FILES, instance=request.user.user_profile)
        
        user = UserModel.objects.get(username=username)
        profile = user.user_profile
        
        
        if userform.is_valid() and profileform.is_valid():
            userform.save()
            profileform.save()
            return redirect(reverse('chat-profile', args=(userform.cleaned_data['username'],)))
        else:
            
            context = {
                "page":"profile",
                'profile': profile
               
            }
            messages.error(request,f'Username Already exist!.')
            return render(request,"chat/profile.html",context)

    else:
        user = UserModel.objects.get(username=username)
        profile = UserProfile.objects.get(user=user)
        context = {
            "page":"profile",
            'profile': profile
        
        }
        return render(request,"chat/profile.html",context)

def get_messages(request):
    chats = chatMessages.objects.filter(Q(id__gt=request.POST['last_id']),Q(user_from=request.user.id, user_to=request.POST['chat_id']) | Q(user_from=request.POST['chat_id'], user_to=request.user.id))
    new_msgs = []
    for chat in list(chats):
        data = {}
        data['id'] = chat.id
        data['user_from'] = chat.user_from.id
        data['sender_profile'] = chat.user_from.user_profile.image.url
        data['user_to'] = chat.user_to.id
        data['message'] = chat.message
        data['date_created'] = chat.date_created.strftime("%b-%d-%Y %H:%M")
        if chat.file:
            exten = chat.file.url[chat.file.url.index('.')+1:]
            if exten in ['jpeg', 'png', 'jpg', 'gif']:
                data['exten'] = 0
                data['file'] = chat.file.url
            elif exten in ['mp3', 'mpeg', 'ogg']:
                data['exten'] = 1
                data['file'] = chat.file.url
            elif exten in ['mp4']:
                data['exten'] = 2
                data['file'] = chat.file.url
            
        
        new_msgs.append(data)
        print(json.dumps(new_msgs))
    return HttpResponse(json.dumps(new_msgs), content_type="application/json")

def send_chat(request):
    
    resp = {}
    User = get_user_model()
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            print()
            form.save()
            resp['status'] = 'success'
        else:
            
            resp['status'] = 'failed'
            
    print(resp)
    return HttpResponse(json.dumps(resp), content_type="application/json")



@r.filter
def extenize(url):
    return url[url.index('.')+1:]