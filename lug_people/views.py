# -*- coding: utf-8 -*-
from .models import MemberProfile
from .forms import ProfileEditForm, BitFormSet
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views.generic.base import View, TemplateResponseMixin


class ProfileView(DetailView):
    model = MemberProfile
    slug_field = 'user__username'
    slug_url_kwarg = 'username'
    context_object_name = 'profile'


class ProfileEditView(View, TemplateResponseMixin):
    def get(self, request):
        profile = request.user.get_profile()
        form = ProfileEditForm(instance=profile)
        formset = BitFormSet(instance=profile)
        return self.render_to_response({'form': form, 'bit_forms': formset,
                                        'profile': profile})

    def post(self, request):
        profile = request.user.get_profile()
        form = ProfileEditForm(request.POST, instance=profile)
        formset = BitFormSet(request.POST, instance=profile)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, u"Your profile has been updated!")
            return HttpResponseRedirect(reverse('profile',
                                        kwargs={'username': profile.username}))
        return self.render_to_response({'form': form, 'bit_forms': formset,
                                        'profile': profile})

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileEditView, self).dispatch(*args, **kwargs)
