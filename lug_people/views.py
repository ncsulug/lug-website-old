# -*- coding: utf-8 -*-
from .models import MemberProfile
from .forms import ProfileEditForm, BitFormSet, RegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView
from django.views.generic.base import View, TemplateResponseMixin


class DirectoryView(ListView):
    model = MemberProfile
    context_object_name = 'members'

    def get_queryset(self):
        if self.request.user.is_active:
            return MemberProfile.objects.filter(user__is_active=True) \
                                        .order_by('-ordering', 'user__username')
        else:
            return MemberProfile.objects.filter(user__is_active=True,
                                                is_protected=False) \
                                        .order_by('-ordering', 'user__username')


class ProfileView(DetailView):
    model = MemberProfile
    slug_field = 'user__username'
    slug_url_kwarg = 'username'
    context_object_name = 'profile'

    def get(self, request, *args, **kwargs):
        profile = self.object = self.get_object()
        if profile.is_protected and not request.user.is_active:
            raise Http404()
        context = self.get_context_data(object=profile)
        return self.render_to_response(context)


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
