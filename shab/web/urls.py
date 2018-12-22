# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views
import django.views.defaults

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^dashboard', views.dashboard, name='dashboard'),
    url(r'^accounts/login/?$', views.login_view, name='login'),
    url(r'^form_advanced', views.form_advanced, name='form_advanced'),
    url(r'^newpost', views.newpost, name='newpost'),
    url(r'^posts', views.posts, name='posts'),
    url(r'^banners', views.banners, name='banners'),
    url(r'^related/([0-9]*)/$', views.related, name='related'),
    url(r'^comment', views.comment, name='comment'),
    url(r'^like', views.like, name='like'),
    url(r'^showcomments', views.showcomments, name='showcomments'),
    url(r'^post/([0-9]*)/$', views.post, name='post'),
    url(r'^tag/(.*)/$', views.tag, name='tag'),
    url(r'^search/$', views.search, name='search'),
    url(r'^delpost/([0-9]*)/$', views.delpost, name='delpost'),
    url(r'^editpost/([0-9]*)/$', views.editpost, name='editpost'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^.*/$', views.notfount, name='notfount'),


]

