# -*- coding: utf-8 -*-
from .models import MemberProfile, AccountRequest
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
            return MemberProfile.objects.filter(user__is_active=True)
        else:
            return MemberProfile.objects.filter(user__is_active=True,
                                                is_protected=False)


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


class RegisterView(FormView):
    form_class = RegistrationForm

    def form_valid(self, form):
        data = form.cleaned_data

        username = MemberProfile.make_username(data['nickname'])
        user = User.objects.create_user(username, data['email'], data['password1'])
        user.is_active = False
        user.is_staff = False
        user.save()

        profile = form.save(commit=False)
        profile.user = user
        profile.save()

        account_request = AccountRequest(user=user, status=u"pending",
                                         comments=data['comments'])
        account_request.save()

        messages.success(self.request, u"You have registered for an account! "
                         "We will contact you when your account has been "
                         "approved. You can then log in as %s." % username)
        return HttpResponseRedirect('/')


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
