from __future__ import absolute_import
from django import template
from ..models import NavbarLink

register = template.Library()

@register.filter
def url_title(title):
    return title.replace(" ", "_")


@register.assignment_tag
def get_navbar_links():
    return NavbarLink.objects.all()
