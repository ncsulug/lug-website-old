from django import template
from ..models import Fortune

import random

register = template.Library()


@register.simple_tag
def fortune():

    # We start by looking for "priority" fortunes, which include big deal
    # news announcements such as "Hack Day next week".
    important_fortunes = Fortune.objects.filter(priority=True).order_by("?")
    if important_fortunes:
        return important_fortunes[0].value
    
    # This tries to display any fortune in the DB, but gives a default error
    # if nothing is in there.
    try:
        return Fortune.objects.order_by("?")[0].value
    except:
        return "Segmentation Fault"

