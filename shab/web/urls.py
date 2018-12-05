# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^dashboard', views.dashboard, name='dashboard'),
    url(r'^accounts/login/?$', views.login_view, name='login'),
    url(r'^form_advanced', views.form_advanced, name='form_advanced'),
    url(r'^newpost', views.newpost, name='newpost'),
    url(r'^avatarbase', views.avatarbase, name='avatarbase'),
    url(r'^logout/$', views.logout_view, name='logout'),


]

