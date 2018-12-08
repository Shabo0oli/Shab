# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import *
from django_summernote.admin import SummernoteModelAdmin
from django_jalali.admin.filters import JDateFieldListFilter
import django_jalali.admin as jadmin









class Postdate(SummernoteModelAdmin):
    list_filter = (
        ('Date', JDateFieldListFilter),
    )
    summernote_fields = ('Text','About')


class Commentdate(SummernoteModelAdmin):
    list_filter = (
        ('Date', JDateFieldListFilter),
    )
    summernote_fields = ('Text',)


admin.site.register(Post, Postdate)
admin.site.register(Comment, Commentdate)
admin.site.register(Like)
admin.site.register(Banner)

from django.contrib.sessions.models import Session

admin.site.register(Session)