# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.html import escape
from .models import Page, Revision, NavbarLink

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'last_updated', 'last_updated_by',
                    'access_level')
    list_editable = ('access_level',)
    list_filter = ('access_level',)

admin.site.register(Page, PageAdmin)


class RevisionAdmin(admin.ModelAdmin):
    list_display = ('page', 'id', 'author', 'timestamp', 'change_note')
    list_filter = ('page', 'author')

admin.site.register(Revision, RevisionAdmin)


class NavbarLinkAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'text', 'target', 'ordering')
    list_editable = ('text', 'target', 'ordering')

admin.site.register(NavbarLink, NavbarLinkAdmin)
