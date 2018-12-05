from django.shortcuts import render

# Create your views here.
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import *
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
import jdatetime


@login_required
def dashboard(request):
    context = {}
    return render(request, 'app/index4.html', context)

def index(request):
    context = {}
    return render(request, 'index.html', context)

def form_advanced(request) :
    context = {}
    return render(request, 'app/form_advanced.html', context)


def login_view(request):
    if 'username' in request.POST and 'password' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None :
            login(request, user)
            context = {}
            context['user'] = user
            return render(request, 'app/index4.html', context)
        else:
            context = {}
            context['message'] ='نام کاربری یا پسورد وارد شده اشتباه میباشد'
            return render(request, 'app/login.html', context)
    else:
        context = {}
        return render(request, 'app/login.html', context)

def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def newpost(request) :
    if request.POST :
        pass
    else :
        context = {}
        return render(request, 'app/form.html', context)

@login_required
@csrf_exempt
def avatarbase(request):
    title =  request.POST['title']
    subtitle = request.POST['subtitle']
    category = request.POST['category']
    type = request.POST['type']
    text = request.POST['text']
    tags = []
    tags = request.POST['tags']
    avatar = request.FILES['avatar']
    context = {}
    context['message'] = 'با موفقیت ذخیره شد'
    currentDate = jdatetime.date.today()
    post = Post(Title=title , Category=category , SubTitle=subtitle , Type=type , Text=text , Avatar=avatar , Date=currentDate)
    post.save()
    return render(request, 'app/form.html', context)
