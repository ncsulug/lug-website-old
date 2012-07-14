# -*- coding: utf-8 -*-
from .models import MemberProfile, Bit
from django import forms
from django.contrib.auth.models import User
from django.forms.models import ModelForm, inlineformset_factory

class ProfileEditForm(ModelForm):
    class Meta:
        model = MemberProfile
        fields = ('nickname', 'real_name', 'preferred_name', 'role')


class RegistrationForm(ModelForm):
    class Meta:
        model = MemberProfile
        fields = ('nickname', 'real_name', 'preferred_name', 'role')

    email       = forms.EmailField()
    comments    = forms.CharField(widget=forms.Textarea(),
                    help_text="Notes for the site administrators on "
                    "who you are and/or how to contact you.")
    password1   = forms.CharField(widget=forms.PasswordInput(render_value=False),
                                  label="Password")
    password2   = forms.CharField(widget=forms.PasswordInput(render_value=False),
                                  label="Repeat password")

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']
        username = MemberProfile.make_username(nickname)
        existing = User.objects.filter(username__iexact=username)
        if existing.exists():
            raise forms.ValidationError("A user with your login name (%s) "
                                        "already exists.")
        else:
            return self.cleaned_data['nickname']

    def clean(self):
        data = self.cleaned_data
        if 'password1' in data and 'password2' in data:
            if data['password1'] != data['password2']:
                raise forms.ValidationError("The two password fields didn't match.")
        return data


BitFormSet = inlineformset_factory(MemberProfile, Bit, fk_name="owner", extra=3)
