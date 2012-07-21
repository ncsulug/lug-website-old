from django import template
from django.contrib.auth.models import User

register = template.Library()

@register.inclusion_tag('profiles/link.html')
def profile_link(profile):
    if isinstance(profile, User):
        profile = profile.get_profile()
    return {'profile': profile}
