# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.html import escape
from .models import Fortune

admin.site.register(Fortune)
