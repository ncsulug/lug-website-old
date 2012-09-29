from __future__ import absolute_import
from django import template

register = template.Library()

@register.filter
def url_title(title):
    return title.replace(" ", "_")
