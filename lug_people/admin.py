# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.html import escape
from .models import MemberProfile, AccountRequest, BitType, Bit

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
            'fields': ('title', 'ordering', 'role'),
        }),
        ('Profile Information', {
            'fields': ('is_protected', 'biography'),
        }),
    )
    inlines = (BitInline,)
    list_display = ('user', '__unicode__', 'role', 'title', 'ordering')
    list_display_links = ('user',)
    list_filter = ('role', 'user__is_active')
    ordering = ('user__username',)

admin.site.register(MemberProfile, ProfileAdmin)


class AccountRequestAdmin(admin.ModelAdmin):
    actions = ['approve_accounts', 'defer_accounts', 'destroy_accounts']
    fields = ('user', 'request_date', 'status', 'comments')
    date_hierarchy = 'request_date'
    list_display = ('username', 'names', 'email', 'comments', 'request_date',
                    'status')
    list_display_links = ('username',)
    list_filter = ('status', 'user__memberprofile__role')
    list_select_related = True
    ordering = ('user__username',)

    def email(self, account_request):
        email = escape(account_request.user.email)
        return "<a href=\"mailto:%s\">%s</a>" % (email, email)
    email.allow_tags = True

    def approve_accounts(self, request, queryset):
        for account_request in queryset:
            account_request.approve()
    approve_accounts.short_description = 'Approve the selected accounts'

    def defer_accounts(self, request, queryset):
        queryset.update(status=u"deferred")
    defer_accounts.short_description = 'Defer the selected account requests'

    def destroy_accounts(self, request, queryset):
        for account_request in queryset:
            account_request.destroy()
    destroy_accounts.short_description = ('Destroy the selected accounts '
                                          'and their requests')

admin.site.register(AccountRequest, AccountRequestAdmin)


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
