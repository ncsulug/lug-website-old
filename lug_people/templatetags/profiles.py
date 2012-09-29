from django import template
from django.contrib.auth.models import User

register = template.Library()

@register.inclusion_tag('profiles/link.html', takes_context=True)
def profile_link(context, profile):
    if isinstance(profile, User):
        profile = profile.get_profile()
    user_active = context['user'].is_active
    return {'profile': profile,
            'link': user_active and not profile.is_protected}
