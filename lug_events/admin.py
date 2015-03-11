# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.html import escape
from .models import Event, EventKind

class EventKindAdmin(admin.ModelAdmin):
    list_display = ('singular', 'plural', 'description')
    fields = ('singular', 'plural', 'description')

admin.site.register(EventKind, EventKindAdmin)


class EventAdmin(admin.ModelAdmin):
    date_hierarchy = 'start_time'
    list_display = ('name', 'speaker', 'kind', 'start_time', 'end_time', 'location',
                    'advisory', 'on_website', 'on_billboard')
    list_display_links = ('name',)
    list_editable = ('on_website', 'on_billboard')
    list_filter = ('kind', 'on_website', 'on_billboard')
    search_fields = ('name', 'location', 'pitch')

    fields = ('name', 'speaker', 'kind', 'start_time', 'end_time',
              'location', 'pitch', 'custom_url',
              'advisory', 'on_website', 'on_billboard')

admin.site.register(Event, EventAdmin)

