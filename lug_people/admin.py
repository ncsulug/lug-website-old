# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import MemberProfile, BitType, Bit

class BitInline(admin.TabularInline):
    model = Bit
    fk_name = 'owner'
    fields = ('bit_type', 'data')
    extra = 1


class ProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('user',)
        }),
        ('Names', {
            'fields': ('nickname', 'real_name', 'preferred_name')
        }),
        ('LUG Organizational Stuff', {
            'fields': ('title', 'role'),
        })
    )
    inlines = (BitInline,)
    list_display = ('user', '__unicode__', 'role', 'title')
    list_display_links = ('user',)
    list_filter = ('role', 'user__is_active')
    ordering = ('user__username',)

admin.site.register(MemberProfile, ProfileAdmin)


class BitTypeAdmin(admin.ModelAdmin):
    fields = ('caption', 'slug', 'ordering', 'format', 'link_template',
              'instructions')
    list_display = ('caption', 'slug', 'ordering', 'format', 'link_template')
    list_display_links = ('caption',)
    list_editable = ('ordering',)
    list_filter = ('format',)
    prepopulated_fields = {'slug': ('caption',)}
    radio_fields = {'format': admin.HORIZONTAL}

admin.site.register(BitType, BitTypeAdmin)
