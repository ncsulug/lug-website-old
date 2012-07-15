# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.html import escape
from .models import BlogPost

class BlogPostAdmin(admin.ModelAdmin):
    date_hierarchy = 'pub_date'
    fields = ('title', 'slug', 'content', 'is_active', 'pub_date', 'author')
    list_display = ('title', 'is_active', 'pub_date', 'author')
    list_filter = ('is_active', 'author')
    ordering = ('-pub_date',)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'content')

    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        obj.save()


admin.site.register(BlogPost, BlogPostAdmin)
