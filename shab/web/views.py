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
from itertools import zip_longest
from django.http import JsonResponse
from json import JSONEncoder
from django.contrib.sessions.models import Session


@login_required
def dashboard(request):
    context = {}
    activeuser = len(Session.objects.all())
    context['activeuser'] = activeuser
    return render(request, 'app/index4.html', context)

def index(request):
    context = {}
    posts = Post.objects.all()
    context['posts'] = posts
    banners = Post.objects.filter(id__in=Banner.objects.values('PostLink'))
    a = []
    for b in banners :
        a.append(b)
    if len(a) % 2 :
        a.append(a[0])
    it = iter(a);
    nested = [list(b) for b in zip_longest(it, it)]
    context['banners'] = nested
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
@csrf_exempt
def newpost(request) :
    if request.POST :
        title = request.POST['title']
        subtitle = request.POST['subtitle']
        about = ''
        if 'about' in request.POST:
            about = request.POST['about']

        if 'postimage' in request.FILES:
            postimage = request.FILES['postimage']
        else:
            postimage = ''
        category = request.POST['category']
        type = request.POST['type']
        text = request.POST['text']
        tags = request.POST['tags']

        if 'avatar' in request.FILES:
            avatar = request.FILES['avatar']
        else:
            avatar = ''
        context = {}
        context['message'] = 'با موفقیت ذخیره شد'
        currentDate = jdatetime.date.today()
        post = Post(Title=title, Category=category, SubTitle=subtitle, Type=type, Text=text, Avatar=avatar,
                    Date=currentDate, About=about,
                    PostImage=postimage)
        post.save()
        tags = tags.split(',')
        for tag in tags:
            post.tags.add(tag)
        post.save()
        return render(request, 'app/form.html', context)
    else :
        context = {}
        return render(request, 'app/form.html', context)
@login_required
def posts(request):
    posts = Post.objects.all()
    context = {}
    context['posts'] = posts
    return render(request, 'app/tables_dynamic.html', context)


def post(request , id) :
    post = Post.objects.get(id=id)
    context = {}
    if not request.session.exists(request.session.session_key):
        request.session.create()
    sesssionkey = Session.objects.get(session_key = request.session.session_key)
    context['post'] = post
    tags = post.tags.all()
    comments = Comment.objects.filter(RelPost=post , Valid = True)
    context['comments'] = comments
    context['tags'] =tags
    context['likesnumber'] = len(Like.objects.filter(RelPost = post))
    if len(Like.objects.filter( RelPost=post , User=sesssionkey ) ) == 0 :
        context['classattr'] = "far gray"
    else :
        context['classattr'] = "fa red"
    if post.Type == 'avatarbase' :
        return render(request, 'post.html', context)
    elif post.Type == 'thumbbase' :
        return render(request, 'post2.html', context)
    elif post.Type == 'bigimage' :
        return render(request, 'post23.html', context)

@csrf_exempt
@login_required
def banners(request):
    if 'delid' in request.POST :
        delid = request.POST['delid']
        banner = Banner.objects.get(PostLink__id=delid)
        banner.delete()
    if 'newbanner' in request.POST :
        newbanner = request.POST['newbanner']
        post = Post.objects.get(id=newbanner)
        banner = Banner(PostLink=post)
        banner.save()
    banners = Post.objects.filter(id__in=Banner.objects.values('PostLink'))
    anotherpost = Post.objects.exclude(pk__in=banners)
    context ={}
    context['banners'] = banners
    context['anotherpost'] = anotherpost
    return render(request, 'app/banners.html', context)

@csrf_exempt
def comment(request) :
    name = request.POST['name']
    email = request.POST['email']
    text = request.POST['text']
    postid = request.POST['postid']
    post = Post.objects.get(id=postid)
    currentDate = jdatetime.date.today()
    cm = Comment(Text=text , Author=name , Email=email, RelPost=post , Date=currentDate)
    cm.save()
    context = {}
    context['response'] = '200'
    context['message'] = 'نظر شما با موفقیت ثبت شد و پس تایید در سایت قرار خواهد گرفت'
    return JsonResponse(context, encoder=JSONEncoder)

@login_required
@csrf_exempt
def showcomments(request) :
    if 'cmid' in request.POST :
        cmid = request.POST['cmid']
        cm = Comment.objects.get(id=cmid)
        if cm.Valid:
            cm.Valid = False
        else:
            cm.Valid = True
        cm.save()
    cm = Comment.objects.all()
    context = {}
    context['comments'] = cm
    return render(request, 'app/comments.html', context)


@csrf_exempt
def like(request):
    if not request.session.exists(request.session.session_key):
        request.session.create()
    post = Post.objects.get(id=request.POST['postid'])
    context = {}
    sesssionkey = Session.objects.get(session_key = request.session.session_key)
    likeobj = Like.objects.filter(RelPost=post, User=sesssionkey)
    if len( likeobj) == 0 :
        l = Like( RelPost=post , User=sesssionkey )
        l.save()
        context['response'] = '200'
        context['message'] = 'لایک کردی'
        context['count'] =  len(Like.objects.filter(RelPost=post))
        return JsonResponse(context, encoder=JSONEncoder)
    else :
        Like.objects.filter(RelPost=post, User=sesssionkey).delete()
        context['response'] = '200'
        context['message'] = 'لایک کرده بودی قبلا'
        context['count'] =  len(Like.objects.filter(RelPost=post))
        return JsonResponse(context, encoder=JSONEncoder)


@login_required
def delpost(request , postid) :
    post = Post.objects.get(id = postid)
    post.delete()
    return posts(request)

@login_required
@csrf_exempt
def editpost(request , postid) :
    if request.POST :
        post = Post.objects.get(id=request.POST['postid'])
        title = request.POST['title']
        subtitle = request.POST['subtitle']
        if 'about' in request.POST:
            post.About = request.POST['about']
        if 'postimage' in request.FILES:
            post.PostImage = request.FILES['postimage']
        category = request.POST['category']
        text = request.POST['text']
        tags = request.POST['tags']
        if 'avatar' in request.FILES:
            post.Avatar = request.FILES['avatar']
        for tag in post.tags.all():
            post.tags.remove(tag)

        tags = tags.split(',')
        print(tags)
        for tag in tags :
            post.tags.add(tag)
        post.Title = title
        post.SubTitle = subtitle
        post.Category = category
        post.Text = text
        post.save()
        context = {}
        context['message'] = 'ویرایش با موفقیت انجام شد'
        posts = Post.objects.all()
        context['posts'] = posts
        return render(request, 'app/tables_dynamic.html', context)




    post = Post.objects.get(id = postid)
    tags = post.tags.all()
    context = {}
    context['post'] = post
    context['tags'] = list(tags)
    return render(request, 'app/editpost.html', context)

@csrf_exempt
def tag(request , tag) :
    tags = []
    tags.append(tag)
    posts = Post.objects.filter(tags__name__in=list(tags))
    context = {}
    context['posts'] = posts
    banners = Post.objects.filter(id__in=Banner.objects.values('PostLink'))
    a = []
    for b in banners:
        a.append(b)
    if len(a) % 2:
        a.append(a[0])
    it = iter(a);
    nested = [list(b) for b in zip_longest(it, it)]
    context['banners'] = nested
    return render(request, 'index.html', context)